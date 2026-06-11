"""
=====================================================================
 VALEN MINI-API — GATEWAY DO APP ANDROID (roda na VPS ORACLE)
=====================================================================
 Papel no ecossistema:

   App Android ──HTTPS──> valen-chat.astrazstudio.com.br (jv_nginx)
                              │
                              ▼
                        MINI-API (esta — host Oracle, porta 8788)
                              │ repassa auth/chat
                              ▼
                        BRAIN (FastAPI + Ollama na CONTABO)

 Por que existe:
   1. O app é o CONTROLE REMOTO do terminal da Oracle. Quando o Brain
      responde tipo_acao "comando"/"codigo", a mini-api INTERCEPTA,
      guarda como ação pendente (acao_id) e devolve ao app — que trava
      a tela com o modal CONFIRMAR/CANCELAR.
   2. Confirmou ('y')? A mini-api EXECUTA o comando AQUI na Oracle
      (subprocess) ou grava o arquivo, e devolve a saída ao app.
      Cancelou ('n')? Ação descartada — nada roda.
   3. O Brain pode mudar de endereço (hoje container local, amanhã
      Contabo) trocando só a env BRAIN_URL — o app não percebe.

 Segurança:
   - Toda rota protegida valida o MESMO JWT do Brain (segredo
     compartilhado via VALEN_JWT_SECRET — copie o do .env do Brain).
   - Nada executa sem confirmação explícita vinda do modal do app.
   - Toda execução fica registrada em ~/.valen/execucoes.log (audit).
   - Ações pendentes expiram em 10 minutos.

 SUBIR (ver systemd unit em valen-mini-api.service):
   pip install -r requirements.txt
   export BRAIN_URL=http://127.0.0.1:8777     # depois: Contabo
   export VALEN_JWT_SECRET=<mesmo do Brain>
   python mini_api.py
=====================================================================
"""

import logging
import os
import secrets
import subprocess
import time
import uuid
from pathlib import Path

import httpx
import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

# ---------------------------------------------------------------
# CONFIGURAÇÃO (tudo por variável de ambiente)
# ---------------------------------------------------------------
BRAIN_URL = os.getenv("BRAIN_URL", "http://127.0.0.1:8777")   # Brain (hoje local, depois Contabo)
MINI_HOST = os.getenv("MINI_HOST", "0.0.0.0")
MINI_PORT = int(os.getenv("MINI_PORT", "8788"))

# MESMO segredo do Brain — valida o JWT sem precisar perguntar a ele
VALEN_JWT_SECRET = os.getenv("VALEN_JWT_SECRET", "TROQUE-ESTE-SEGREDO-AGORA")
VALEN_JWT_ALGORITHM = "HS256"

# Diretório de trabalho das execuções (comandos rodam a partir daqui)
WORKDIR = Path(os.getenv("VALEN_WORKDIR", str(Path.home()))).expanduser()

# Tempo máximo de um comando confirmado (segundos)
EXEC_TIMEOUT = int(os.getenv("VALEN_EXEC_TIMEOUT", "300"))

# Brain pode demorar (70B na Contabo) — timeout generoso no repasse
BRAIN_TIMEOUT = int(os.getenv("BRAIN_TIMEOUT", "600"))

# Validade de uma ação pendente aguardando o modal (segundos)
ACAO_TTL = 600

# Log de auditoria de tudo que foi executado/cancelado
AUDIT_LOG = Path.home() / ".valen" / "execucoes.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("valen.miniapi")

app = FastAPI(
    title="VALEN Mini-API",
    description="Gateway do app Android: repassa ao Brain e executa ações confirmadas na Oracle.",
    version="1.0.0",
)

# ---------------------------------------------------------------
# AUTENTICAÇÃO — valida o JWT emitido pelo Brain (segredo compartilhado)
# ---------------------------------------------------------------
esquema_bearer = HTTPBearer(auto_error=False)


def autenticar_jwt(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
) -> str:
    """Valida o Bearer JWT em toda rota protegida. Devolve o usuário (sub)."""
    if credenciais is None:
        raise HTTPException(status_code=401, detail="Token ausente. Faça login em /auth/login.")
    try:
        payload = jwt.decode(
            credenciais.credentials,
            VALEN_JWT_SECRET,
            algorithms=[VALEN_JWT_ALGORITHM],
            issuer="valen-brain",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")
    return str(payload.get("sub", ""))


def _bearer(credenciais: HTTPAuthorizationCredentials | None) -> dict:
    """Header Authorization repassado ao Brain tal qual chegou."""
    if credenciais is None:
        return {}
    return {"Authorization": f"Bearer {credenciais.credentials}"}


# ---------------------------------------------------------------
# AÇÕES PENDENTES — memória curta entre o /chat e o /confirmar
# ---------------------------------------------------------------
_pendentes: dict[str, dict] = {}


def _limpar_expiradas() -> None:
    """Descarta ações que ficaram mais de ACAO_TTL aguardando o modal."""
    agora = time.monotonic()
    for acao_id in [k for k, v in _pendentes.items() if agora - v["criada_em"] > ACAO_TTL]:
        logger.info("Ação pendente expirada: %s", acao_id)
        _pendentes.pop(acao_id, None)


def _auditar(linha: str) -> None:
    """Registro permanente de tudo que o app mandou executar/cancelar."""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {linha}\n")


# ---------------------------------------------------------------
# MODELOS (contrato com o app)
# ---------------------------------------------------------------
class ChatRequest(BaseModel):
    mensagem: str = Field(..., min_length=1, max_length=8000)
    contexto: str | None = Field(None, max_length=4000)


class ChatResponse(BaseModel):
    skill_utilizada: str
    modelo_utilizado: str
    tipo_acao: str
    conteudo: str
    arquivo: str | None = None
    explicacao: str | None = None
    acao_id: str | None = None   # presente quando comando/codigo aguarda confirmação


class ConfirmarRequest(BaseModel):
    acao_id: str
    decisao: str = Field(..., pattern="^[yn]$")  # 'y' confirma, 'n' cancela


class ExecucaoResponse(BaseModel):
    executado: bool          # True se rodou/gravou; False se cancelado
    saida: str               # stdout+stderr do comando, ou caminho do arquivo
    codigo_retorno: int      # returncode do subprocess (0 = sucesso; -1 = n/a)


# ---------------------------------------------------------------
# ROTAS — repasse ao Brain
# ---------------------------------------------------------------
@app.get("/api/valen/v1/health")
async def health() -> dict:
    """Vida da mini-api + vida do Brain (diagnóstico em uma chamada)."""
    brain = "offline"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{BRAIN_URL}/api/valen/v1/health")
            if r.status_code == 200:
                brain = "online"
    except httpx.HTTPError:
        pass
    return {"status": "ok", "mini_api": "online", "brain": brain, "brain_url": BRAIN_URL}


@app.post("/auth/login")
async def login(corpo: dict) -> dict:
    """Repassa o login ao Brain — a mini-api não guarda credenciais."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{BRAIN_URL}/auth/login", json=corpo)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Brain inacessível: {exc}")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.json().get("detail", "Falha no login."))
    return r.json()


@app.get("/api/valen/v1/skills")
async def skills(credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer)) -> dict:
    """Catálogo de skills — repasse direto ao Brain."""
    autenticar_jwt(credenciais)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{BRAIN_URL}/api/valen/v1/skills", headers=_bearer(credenciais))
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Brain inacessível: {exc}")


@app.post("/api/valen/v1/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
) -> ChatResponse:
    """
    Repassa o pedido ao Brain. Se a resposta for comando/codigo,
    INTERCEPTA: registra como ação pendente e devolve com acao_id —
    o app trava a tela com o modal e decide via /confirmar.
    """
    autenticar_jwt(credenciais)
    _limpar_expiradas()

    contexto = (req.contexto or "") + " | gateway: mini-api Oracle (execução local nesta VPS)"
    try:
        async with httpx.AsyncClient(timeout=BRAIN_TIMEOUT) as client:
            r = await client.post(
                f"{BRAIN_URL}/api/valen/v1/chat",
                headers=_bearer(credenciais),
                json={"mensagem": req.mensagem, "contexto": contexto.strip(" |")},
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Brain inacessível: {exc}")
    if r.status_code != 200:
        detalhe = r.json().get("detail", "Erro no Brain.") if r.headers.get("content-type", "").startswith("application/json") else "Erro no Brain."
        raise HTTPException(status_code=r.status_code, detail=detalhe)

    dados = r.json()
    resposta = ChatResponse(**dados)

    # Interceptação: ação local só roda depois do modal do app
    if resposta.tipo_acao in ("comando", "codigo"):
        acao_id = uuid.uuid4().hex
        _pendentes[acao_id] = {
            "tipo_acao": resposta.tipo_acao,
            "conteudo": resposta.conteudo,
            "arquivo": resposta.arquivo,
            "criada_em": time.monotonic(),
        }
        resposta.acao_id = acao_id
        logger.info("Ação pendente registrada: %s (%s)", acao_id, resposta.tipo_acao)

    return resposta


# ---------------------------------------------------------------
# ROTA — execução local (depois do modal do app)
# ---------------------------------------------------------------
@app.post("/api/valen/v1/confirmar", response_model=ExecucaoResponse)
def confirmar(
    req: ConfirmarRequest,
    usuario: str = Depends(autenticar_jwt),
) -> ExecucaoResponse:
    """
    Resolve uma ação pendente:
      decisao 'n' -> descarta (nada roda);
      decisao 'y' -> executa o comando via subprocess OU grava o arquivo,
                     aqui na VPS Oracle, e devolve a saída ao app.
    """
    _limpar_expiradas()
    acao = _pendentes.pop(req.acao_id, None)
    if acao is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada ou expirada.")

    # CANCELADO — auditoria e fim
    if req.decisao == "n":
        _auditar(f"CANCELADO por {usuario}: {acao['tipo_acao']} | {acao['conteudo'][:200]}")
        return ExecucaoResponse(executado=False, saida="Ação cancelada.", codigo_retorno=-1)

    # CONFIRMADO — executa
    if acao["tipo_acao"] == "comando":
        comando = acao["conteudo"]
        _auditar(f"EXECUTANDO por {usuario}: {comando[:500]}")
        try:
            resultado = subprocess.run(
                comando, shell=True, cwd=WORKDIR,
                capture_output=True, text=True, timeout=EXEC_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            _auditar(f"TIMEOUT ({EXEC_TIMEOUT}s): {comando[:200]}")
            return ExecucaoResponse(
                executado=True,
                saida=f"⏱ Comando excedeu {EXEC_TIMEOUT}s e foi interrompido.",
                codigo_retorno=-1,
            )
        saida = (resultado.stdout + resultado.stderr).strip() or "(sem saída)"
        _auditar(f"CONCLUÍDO rc={resultado.returncode}: {comando[:200]}")
        # Limita a saída para não estourar a tela do celular
        return ExecucaoResponse(
            executado=True,
            saida=saida[:8000],
            codigo_retorno=resultado.returncode,
        )

    # tipo_acao == "codigo": grava o arquivo no WORKDIR
    nome = acao.get("arquivo") or "valen_output.txt"
    destino = (WORKDIR / nome).resolve()
    # Trava de caminho: arquivo nunca escapa do diretório de trabalho
    if not str(destino).startswith(str(WORKDIR.resolve())):
        raise HTTPException(status_code=400, detail="Caminho de arquivo inválido.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(acao["conteudo"], encoding="utf-8")
    _auditar(f"ARQUIVO GRAVADO por {usuario}: {destino}")
    return ExecucaoResponse(executado=True, saida=f"Arquivo gravado: {destino}", codigo_retorno=0)


# ---------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    if VALEN_JWT_SECRET == "TROQUE-ESTE-SEGREDO-AGORA":
        logger.warning("ATENÇÃO: defina VALEN_JWT_SECRET (o MESMO do Brain)!")
    logger.info("Mini-API no ar — Brain em %s | workdir %s", BRAIN_URL, WORKDIR)
    uvicorn.run(app, host=MINI_HOST, port=MINI_PORT)

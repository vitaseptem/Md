"""
=====================================================================
 VALEN BRAIN — SERVIDOR CENTRAL (FastAPI) — roda na CONTABO
=====================================================================
 O cérebro do ecossistema Valen:
   - POST /auth/login: valida o Admin (usuário único) e emite JWT
   - POST /api/valen/v1/chat: protegido por JWT Bearer, orquestra a
     skill correta e injeta o contexto no Llama 3 70B (Ollama)
   - Skills dinâmicas (hot-reload) da pasta skills/
   - Devolve JSON estruturado: {skill_utilizada, tipo_acao, conteudo}

 SUBIR O SERVIDOR (sem Docker, para testes):
   cd ~/VALEN_Vault_Engine/VALEN-Vault/brain
   pip install -r requirements.txt
   export VALEN_JWT_SECRET="$(openssl rand -hex 32)"
   export VALEN_ADMIN_USER="davi"
   export VALEN_ADMIN_PASSWORD_HASH="$(python gerar_hash.py 'sua-senha' | tail -1 | cut -d= -f2-)"
   python main.py
=====================================================================
"""

import logging
import time
from collections import defaultdict, deque

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from auth import LoginRequest, LoginResponse, autenticar_jwt, realizar_login
from config import (
    RATE_LIMIT_MAX_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    VALEN_ADMIN_PASSWORD_HASH,
    VALEN_HOST,
    VALEN_JWT_SECRET,
    VALEN_PORT,
)
from orchestrator import perguntar_ao_valen
from skill_loader import carregar_skills

# ---------------------------------------------------------------
# Logging estruturado simples
# ---------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("valen.api")

app = FastAPI(
    title="VALEN Brain",
    description="Servidor central do assistente pessoal Valen (skills + Llama 3 70B).",
    version="1.0.0",
)

# ---------------------------------------------------------------
# RATE LIMITING — janela deslizante em memória, por IP de origem.
# (Para múltiplas réplicas atrás de LB, migrar para Redis.)
# ---------------------------------------------------------------
_janelas: dict[str, deque] = defaultdict(deque)


def limitar_taxa(request: Request) -> None:
    """Anti-flood: no máx. N requisições por janela de tempo, por IP."""
    ip = request.client.host if request.client else "desconhecido"
    agora = time.monotonic()
    janela = _janelas[ip]

    # Descarta registros mais antigos que a janela
    while janela and agora - janela[0] > RATE_LIMIT_WINDOW_SECONDS:
        janela.popleft()

    if len(janela) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Muitas requisições. Aguarde um pouco.")
    janela.append(agora)


# ---------------------------------------------------------------
# MODELOS DE ENTRADA/SAÍDA (contrato da API)
# ---------------------------------------------------------------
class ChatRequest(BaseModel):
    mensagem: str = Field(..., min_length=1, max_length=8000, description="Pedido do usuário em português.")
    contexto: str | None = Field(None, max_length=4000, description="Contexto opcional da máquina cliente (cwd, SO...).")


class ChatResponse(BaseModel):
    skill_utilizada: str    # nome da skill que resolveu (ou "geral")
    modelo_utilizado: str   # LLM do conselho que atendeu (ex: llama3:70b)
    tipo_acao: str          # "texto" | "comando" | "codigo"
    conteudo: str           # resposta, comando bash ou código-fonte
    arquivo: str | None     # nome do arquivo (quando tipo_acao == "codigo")
    explicacao: str | None  # resumo curto da ação proposta


# ---------------------------------------------------------------
# ROTAS
# ---------------------------------------------------------------
@app.post("/auth/login", response_model=LoginResponse, dependencies=[Depends(limitar_taxa)])
def login(req: LoginRequest) -> LoginResponse:
    """
    Login do USUÁRIO ÚNICO (Administrador). Não existe rota de registro.
    Devolve um JWT Bearer de expiração longa, válido para CLI (Oracle),
    Android e futuros clientes Windows/Desktop.
    Rate-limited para mitigar força bruta.
    """
    return realizar_login(req)


@app.get("/api/valen/v1/health")
def health() -> dict:
    """Verificação de vida — útil para monitoramento e para a CLI."""
    return {"status": "ok", "valen": "online"}


@app.get("/api/valen/v1/skills", dependencies=[Depends(autenticar_jwt)])
def listar_skills() -> dict:
    """Lista as skills atualmente disponíveis na pasta skills/."""
    skills = carregar_skills()
    return {
        "total": len(skills),
        "skills": [{"nome": s.nome, "descricao": s.descricao, "gatilhos": s.gatilhos} for s in skills],
    }


@app.post(
    "/api/valen/v1/chat",
    response_model=ChatResponse,
    dependencies=[Depends(autenticar_jwt), Depends(limitar_taxa)],
)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    Endpoint principal: recebe o pedido da CLI (Oracle), orquestra a
    skill mais relevante, consulta o Llama 3 70B e devolve a resposta
    estruturada em JSON.
    """
    logger.info("Pedido recebido (%d chars)", len(req.mensagem))
    try:
        resultado = await perguntar_ao_valen(req.mensagem, req.contexto)
    except Exception as exc:
        logger.exception("Falha ao consultar o conselho de modelos: %s", exc)
        raise HTTPException(status_code=502, detail="Falha ao consultar os modelos via Ollama.")

    return ChatResponse(**resultado)


# ---------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    if VALEN_JWT_SECRET == "TROQUE-ESTE-SEGREDO-AGORA":
        logger.warning("=" * 60)
        logger.warning("ATENÇÃO: você está usando o segredo JWT padrão de exemplo!")
        logger.warning("Gere um segredo forte:  openssl rand -hex 32")
        logger.warning("E defina no .env:  VALEN_JWT_SECRET=<segredo>")
        logger.warning("=" * 60)
    if not VALEN_ADMIN_PASSWORD_HASH:
        logger.warning("=" * 60)
        logger.warning("ATENÇÃO: VALEN_ADMIN_PASSWORD_HASH não definido — login impossível!")
        logger.warning("Gere o hash:  python gerar_hash.py 'sua-senha-forte'")
        logger.warning("=" * 60)

    uvicorn.run(app, host=VALEN_HOST, port=VALEN_PORT)

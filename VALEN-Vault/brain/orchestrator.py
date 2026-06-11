"""
=====================================================================
 VALEN BRAIN — ORQUESTRADOR: CONSELHO DE MODELOS + SKILLS
=====================================================================
 Arquitetura de Roteamento Inteligente (Banca de Conselheiros):

   pedido do usuário
        │
        ▼
   [1] ROTEADOR LEVE (Llama 3 8B) — analisa o pedido em português
        │   e decide qual especialista resolve. Sempre carregado,
        │   resposta em milissegundos.
        ▼
   [2] ESPECIALISTA escolhido:
        • frontend : Qwen 2.5 Coder — telas, Kotlin/Compose, layouts
        • rapido   : Llama 3 8B — comandos de terminal, logs, conversa
        • supremo  : llama3.3-meta-puro (Llama 3.3 70B Instruct, pesos
                     oficiais da Meta, quantizado q4_K_M) — só desperta
                     (sobe do SSD p/ RAM) para arquiteturas complexas
                     e sistemas do zero
        │
        ▼
   [3] SKILL mais relevante (hot-reload da pasta skills/) é injetada
       no system prompt do especialista.
        │
        ▼
   [4] Resposta validada no contrato JSON rígido:
       {skill_utilizada, modelo_utilizado, tipo_acao, conteudo, ...}

 Se o roteador falhar (timeout, JSON inválido), um fallback por
 heurística de palavras-chave assume — o Valen nunca fica mudo.
=====================================================================
"""

import json
import logging
import re
import unicodedata

import httpx

from config import (
    MODELO_FRONTEND,
    MODELO_RAPIDO,
    MODELO_ROTEADOR,
    MODELO_SUPREMO,
    OLLAMA_TIMEOUT,
    OLLAMA_URL,
    ROUTER_TIMEOUT,
)
from skill_loader import Skill, carregar_skills

logger = logging.getLogger("valen.orchestrator")

# Tipos de ação que os clientes (CLI Oracle / app Android) sabem executar
TIPOS_ACAO_VALIDOS = {"texto", "comando", "codigo"}

# ---------------------------------------------------------------
# BANCA DE CONSELHEIROS — mapa especialista -> modelo do Ollama
# ---------------------------------------------------------------
ESPECIALISTAS: dict[str, dict] = {
    "frontend": {
        "modelo": MODELO_FRONTEND,
        "descricao": "Interface/Front-end: telas, Kotlin/Jetpack Compose, HTML/CSS, layouts visuais.",
    },
    "rapido": {
        "modelo": MODELO_RAPIDO,
        "descricao": "Linha de comando/Scripts rápidos: automações de terminal, leitura de logs, conversas casuais.",
    },
    "supremo": {
        "modelo": MODELO_SUPREMO,
        "descricao": "Tarefas massivas: arquiteturas complexas, sistemas do zero, refatoração pesada.",
    },
}
ESPECIALISTA_PADRAO = "rapido"  # quem assume quando o roteador não decide

# ---------------------------------------------------------------
# PROMPT DO ROTEADOR — decisão rápida e barata, saída JSON mínima
# ---------------------------------------------------------------
PROMPT_ROTEADOR = """Você é o ROTEADOR do Valen. Sua ÚNICA função é classificar o pedido
do usuário (em português) e escolher o especialista certo. NÃO responda o pedido.

ESPECIALISTAS:
- "frontend": código de telas/interfaces — Kotlin, Jetpack Compose, HTML, CSS, layouts visuais, UI/UX.
- "rapido": comandos de terminal, scripts simples, leitura de logs, perguntas e conversas casuais.
- "supremo": tarefas MASSIVAS — arquitetar sistemas complexos, criar projetos inteiros do zero,
  refatorações pesadas com muitos arquivos. (Custa caro: só escolha quando realmente necessário.)

Responda ESTRITAMENTE com um JSON:
{"especialista": "frontend" | "rapido" | "supremo"}
"""

# Heurística de fallback: palavras-chave -> especialista (sem acentos, minúsculas)
HEURISTICA_FALLBACK: list[tuple[str, list[str]]] = [
    ("supremo", ["arquitetura", "sistema completo", "do zero", "refatorar", "refatoracao",
                 "microservico", "projeto inteiro", "ecossistema"]),
    ("frontend", ["tela", "interface", "layout", "kotlin", "compose", "html", "css",
                  "frontend", "front-end", "ui", "botao", "design"]),
]


def _normalizar(texto: str) -> str:
    """Minúsculas + remoção de acentos, para casar gatilhos com robustez."""
    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _extrair_json(texto: str) -> dict:
    """Extrai o primeiro objeto JSON da resposta de um modelo (com fallback regex)."""
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", texto, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


async def _chamar_ollama(modelo: str, system: str, user: str, timeout: float) -> str:
    """Chamada única ao /api/chat do Ollama com saída forçada em JSON."""
    payload = {
        "model": modelo,
        "stream": False,
        "format": "json",                     # Ollama força JSON válido na saída
        "options": {"temperature": 0.2},      # baixa temperatura = saída disciplinada
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        resposta = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resposta.raise_for_status()
        return resposta.json()["message"]["content"]


# ---------------------------------------------------------------
# ETAPA 1 — ROTEAMENTO (conselheiro leve decide quem trabalha)
# ---------------------------------------------------------------
def _rotear_por_heuristica(mensagem: str) -> str:
    """Plano B sem IA: classifica por palavras-chave. Nunca falha."""
    msg = _normalizar(mensagem)
    for especialista, palavras in HEURISTICA_FALLBACK:
        if any(p in msg for p in palavras):
            return especialista
    return ESPECIALISTA_PADRAO


async def rotear(mensagem: str) -> str:
    """
    Pergunta ao modelo roteador (Llama 3 8B) qual especialista deve
    atender. Timeout curto: roteamento não pode segurar a fila.
    Qualquer falha degrada para a heurística de palavras-chave.
    """
    try:
        bruto = await _chamar_ollama(
            MODELO_ROTEADOR, PROMPT_ROTEADOR, mensagem, timeout=ROUTER_TIMEOUT
        )
        escolha = str(_extrair_json(bruto).get("especialista", "")).lower().strip()
        if escolha in ESPECIALISTAS:
            logger.info("Roteador escolheu especialista: %s", escolha)
            return escolha
        logger.warning("Roteador devolveu especialista desconhecido: %r", escolha)
    except Exception as exc:
        logger.warning("Roteador indisponível (%s) — usando heurística.", exc)

    escolha = _rotear_por_heuristica(mensagem)
    logger.info("Heurística escolheu especialista: %s", escolha)
    return escolha


# ---------------------------------------------------------------
# ETAPA 2 — SELEÇÃO DE SKILL (hot-reload a cada requisição)
# ---------------------------------------------------------------
def selecionar_skill(mensagem: str, skills: list[Skill]) -> Skill | None:
    """
    Pontua cada skill contando quantos gatilhos aparecem na mensagem.
    Zero pontos -> None (modo geral, sem skill).
    """
    msg = _normalizar(mensagem)
    melhor: Skill | None = None
    melhor_pontos = 0

    for skill in skills:
        pontos = sum(1 for gatilho in skill.gatilhos if _normalizar(gatilho) in msg)
        logger.debug("Skill %-15s -> %d pontos", skill.nome, pontos)
        if pontos > melhor_pontos:
            melhor, melhor_pontos = skill, pontos

    return melhor


# ---------------------------------------------------------------
# ETAPA 3 — SYSTEM PROMPT DO ESPECIALISTA (com injeção da skill)
# ---------------------------------------------------------------
SYSTEM_PROMPT_BASE = """Você é VALEN, assistente pessoal de IA do Davi (Astraz Studio).
Você roda em um servidor soberano e responde SEMPRE em português do Brasil.

REGRAS DE SAÍDA (OBRIGATÓRIAS):
Responda ESTRITAMENTE com um único objeto JSON, sem texto fora dele, no formato:
{
  "tipo_acao": "texto" | "comando" | "codigo",
  "conteudo": "<o texto explicativo, OU o comando bash, OU o código-fonte completo>",
  "arquivo": "<nome do arquivo a criar, apenas quando tipo_acao for 'codigo'>",
  "explicacao": "<frase curta dizendo o que a ação faz>"
}

GUIA DE ESCOLHA DO tipo_acao:
- "texto":   perguntas, explicações, conversas — conteudo é a resposta em si.
- "comando": quando a solução é executar algo no terminal — conteudo é o comando bash puro.
- "codigo":  quando a solução é criar um arquivo — conteudo é o código completo e
             "arquivo" é o nome/caminho relativo do arquivo a criar.

Nunca invente caminhos absolutos da máquina do usuário. Comandos devem ser seguros
e nunca destrutivos sem necessidade explícita do usuário.
"""


def montar_system_prompt(skill: Skill | None, skills: list[Skill], especialista: str) -> str:
    """
    Prompt base + papel do especialista escolhido + catálogo de skills
    + INSTRUCOES da skill vencedora (injeção de contexto).
    """
    catalogo = "\n".join(f"- {s.nome}: {s.descricao}" for s in skills) or "- (nenhuma)"
    prompt = SYSTEM_PROMPT_BASE
    prompt += f"\nSEU PAPEL NESTA REQUISIÇÃO: {ESPECIALISTAS[especialista]['descricao']}\n"
    prompt += f"\nSKILLS DISPONÍVEIS NO ECOSSISTEMA:\n{catalogo}\n"

    if skill is not None:
        prompt += (
            f"\n=== SKILL ATIVA: {skill.nome.upper()} ===\n"
            f"{skill.instrucoes}\n"
            f"=== FIM DAS INSTRUÇÕES DA SKILL ===\n"
        )
    return prompt


# ---------------------------------------------------------------
# PIPELINE COMPLETO — chamado pelo endpoint /api/valen/v1/chat
# ---------------------------------------------------------------
async def perguntar_ao_valen(mensagem: str, contexto: str | None = None) -> dict:
    """
    roteador -> especialista -> skill -> Ollama -> JSON validado.
    Retorna o contrato rígido da API:
      { skill_utilizada, modelo_utilizado, tipo_acao, conteudo, arquivo, explicacao }
    """
    # 1. Roteamento: conselheiro leve decide o especialista
    especialista = await rotear(mensagem)
    modelo = ESPECIALISTAS[especialista]["modelo"]

    # 2. Hot-reload das skills a cada chamada (pasta skills/ é viva)
    skills = carregar_skills()
    skill = selecionar_skill(mensagem, skills)
    logger.info(
        "Especialista: %s (%s) | Skill: %s",
        especialista, modelo, skill.nome if skill else "(modo geral)",
    )

    # 3. Montagem do prompt com injeção da skill
    system_prompt = montar_system_prompt(skill, skills, especialista)
    user_prompt = mensagem if not contexto else f"[CONTEXTO DA MÁQUINA]\n{contexto}\n\n[PEDIDO]\n{mensagem}"

    # 4. Chamada ao especialista (o llama3.3-meta-puro de 70B só sobe à RAM
    #    se for o escolhido — o Ollama carrega/descarrega sob demanda).
    #    O contrato devolve `modelo_utilizado` com o ID real usado, então a
    #    CLI da Oracle e o app Kotlin veem "llama3.3-meta-puro" quando o
    #    modelo de alta fidelidade da Meta é ativado.
    bruto = await _chamar_ollama(modelo, system_prompt, user_prompt, timeout=OLLAMA_TIMEOUT)

    # 5. Validação e normalização do contrato de saída
    try:
        dados = _extrair_json(bruto)
    except (json.JSONDecodeError, KeyError):
        # Modelo fugiu do contrato: degradamos para texto puro (nunca 500)
        logger.warning("Modelo não devolveu JSON válido; degradando para texto.")
        dados = {"tipo_acao": "texto", "conteudo": bruto, "explicacao": ""}

    tipo = str(dados.get("tipo_acao", "texto")).lower()
    if tipo not in TIPOS_ACAO_VALIDOS:
        tipo = "texto"

    return {
        "skill_utilizada": skill.nome if skill else "geral",
        "modelo_utilizado": modelo,
        "tipo_acao": tipo,
        "conteudo": str(dados.get("conteudo", "")),
        "arquivo": str(dados.get("arquivo", "")) or None,
        "explicacao": str(dados.get("explicacao", "")) or None,
    }


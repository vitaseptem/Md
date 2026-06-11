"""
=====================================================================
 VALEN BRAIN — CARREGADOR DINÂMICO DE SKILLS
=====================================================================
 Escaneia a pasta skills/ em busca de arquivos skill_*.py, importa
 cada um dinamicamente (sem precisar reiniciar o servidor) e expõe
 a lista de habilidades disponíveis para o orquestrador.

 CONTRATO DE UMA SKILL (cada arquivo skill_*.py deve definir):
   SKILL_INFO  -> dict com "nome", "descricao" e "gatilhos" (lista
                  de palavras-chave que indicam relevância)
   INSTRUCOES  -> string com as instruções mestres que serão
                  injetadas no System Prompt do Llama 3 quando a
                  skill for ativada.
=====================================================================
"""

import importlib.util
import logging
from dataclasses import dataclass, field
from pathlib import Path

from config import SKILLS_DIR

logger = logging.getLogger("valen.skills")


@dataclass
class Skill:
    """Representação em memória de uma skill carregada do disco."""
    nome: str                       # identificador curto (ex: "desenvolvimento")
    descricao: str                  # resumo de uma linha do que a skill faz
    gatilhos: list[str]             # palavras-chave que ativam a skill
    instrucoes: str                 # texto injetado no system prompt
    arquivo: str = ""               # caminho do .py de origem (para debug)
    erros: list[str] = field(default_factory=list)


def _carregar_modulo(caminho: Path):
    """Importa um arquivo .py isoladamente, sem poluir sys.modules global."""
    spec = importlib.util.spec_from_file_location(f"valen_skill_{caminho.stem}", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def carregar_skills() -> list[Skill]:
    """
    Varre SKILLS_DIR e retorna todas as skills válidas.

    É chamada a CADA requisição de chat — assim, criar/editar um
    skill_*.py novo na pasta já entra em vigor imediatamente,
    sem restart do servidor (hot-reload por design).
    """
    skills: list[Skill] = []

    if not SKILLS_DIR.exists():
        logger.warning("Pasta de skills não existe: %s", SKILLS_DIR)
        return skills

    for caminho in sorted(SKILLS_DIR.glob("skill_*.py")):
        try:
            modulo = _carregar_modulo(caminho)

            # Validação do contrato mínimo da skill
            info = getattr(modulo, "SKILL_INFO", None)
            instrucoes = getattr(modulo, "INSTRUCOES", None)
            if not isinstance(info, dict) or not isinstance(instrucoes, str):
                logger.error("Skill inválida (faltam SKILL_INFO/INSTRUCOES): %s", caminho.name)
                continue

            skills.append(
                Skill(
                    nome=str(info.get("nome", caminho.stem)),
                    descricao=str(info.get("descricao", "")),
                    gatilhos=[g.lower() for g in info.get("gatilhos", [])],
                    instrucoes=instrucoes.strip(),
                    arquivo=str(caminho),
                )
            )
        except Exception as exc:  # skill quebrada não derruba o servidor
            logger.exception("Falha ao carregar skill %s: %s", caminho.name, exc)

    logger.info("Skills carregadas: %s", [s.nome for s in skills])
    return skills

"""
=====================================================================
 VALEN BRAIN — CONFIGURAÇÃO CENTRAL (Servidor Contabo)
=====================================================================
 Todas as variáveis de ambiente/configuração do cérebro do Valen
 ficam aqui, bem visíveis. Podem ser sobrescritas por variáveis de
 ambiente do sistema (export VALEN_JWT_SECRET=... etc.).
=====================================================================
"""

import os
from pathlib import Path

# ---------------------------------------------------------------
# REDE — onde o servidor FastAPI escuta
# ---------------------------------------------------------------
VALEN_HOST = os.getenv("VALEN_HOST", "0.0.0.0")   # escuta em todas as interfaces
VALEN_PORT = int(os.getenv("VALEN_PORT", "8777")) # porta da API do cérebro

# ---------------------------------------------------------------
# AUTENTICAÇÃO — USUÁRIO ÚNICO (Administrador) via .env
# Sem banco de usuários, sem rota de registro. Apenas o Admin loga.
#
# 1. Gere o hash da senha:   python gerar_hash.py "sua-senha"
# 2. Gere o segredo do JWT:  openssl rand -hex 32
# 3. Defina tudo no .env (veja .env.example)
# ---------------------------------------------------------------
VALEN_ADMIN_USER = os.getenv("VALEN_ADMIN_USER", "admin")
VALEN_ADMIN_PASSWORD_HASH = os.getenv("VALEN_ADMIN_PASSWORD_HASH", "")

# Segredo que assina os JWT — >>> OBRIGATÓRIO trocar em produção <<<
VALEN_JWT_SECRET = os.getenv("VALEN_JWT_SECRET", "TROQUE-ESTE-SEGREDO-AGORA")
VALEN_JWT_ALGORITHM = "HS256"

# Expiração longa do token (padrão 30 dias) — mesmo JWT serve para
# CLI (Oracle), Android e futuros clientes Windows/Desktop.
VALEN_JWT_EXPIRE_DAYS = int(os.getenv("VALEN_JWT_EXPIRE_DAYS", "30"))

# ---------------------------------------------------------------
# OLLAMA — CONSELHO DE MODELOS (Banca de Conselheiros)
# O Ollama carrega/descarrega modelos sob demanda: os pequenos ficam
# quentes, o 70B só sobe do SSD para a RAM quando convocado.
# ---------------------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

# Roteador leve: classifica o pedido e escolhe o especialista
MODELO_ROTEADOR = os.getenv("VALEN_MODELO_ROTEADOR", "llama3:8b")

# Especialista em Interface/Front-end (telas, Kotlin/Compose, layouts)
MODELO_FRONTEND = os.getenv("VALEN_MODELO_FRONTEND", "qwen2.5-coder:7b")

# Especialista em comandos rápidos/scripts/conversas casuais
MODELO_RAPIDO = os.getenv("VALEN_MODELO_RAPIDO", "llama3:8b")

# Especialista Supremo: só desperta para tarefas massivas
MODELO_SUPREMO = os.getenv("VALEN_MODELO_SUPREMO", "llama3:70b")

# Tempo máximo (segundos) de espera pela resposta do especialista.
# Llama 3 70B em CPU pode demorar — seja generoso.
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "600"))

# Roteamento não pode segurar a fila: timeout curto e fallback heurístico
ROUTER_TIMEOUT = int(os.getenv("VALEN_ROUTER_TIMEOUT", "60"))

# ---------------------------------------------------------------
# SKILLS — diretório raiz onde vivem os módulos de habilidade
# (um nível acima de brain/: ~/VALEN_Vault_Engine/VALEN-Vault/skills)
# ---------------------------------------------------------------
SKILLS_DIR = Path(
    os.getenv("VALEN_SKILLS_DIR", str(Path(__file__).resolve().parent.parent / "skills"))
)

# ---------------------------------------------------------------
# RATE LIMITING — proteção anti-flood básica (janela deslizante)
# Máximo de requisições por janela, por token/IP.
# ---------------------------------------------------------------
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("VALEN_RATE_MAX", "30"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("VALEN_RATE_WINDOW", "60"))

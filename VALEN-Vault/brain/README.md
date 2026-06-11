# VALEN — Ecossistema de IA (Brain + CLI + Android)

Assistente pessoal soberano com **Conselho de Modelos** (roteamento inteligente
de LLMs via Ollama), **skills dinâmicas** (hot-reload) e **usuário único** (Admin
Master) autenticado por JWT.

```
VALEN-Vault/
├── brain/                  # 🧠 servidor central (Contabo, Docker)
│   ├── main.py             # FastAPI: /auth/login, /chat, /skills, /health
│   ├── auth.py             # usuário único + JWT (HS256, expiração longa)
│   ├── gerar_hash.py       # gera o hash PBKDF2 da senha do Admin
│   ├── orchestrator.py     # roteador leve -> especialista -> skill -> Ollama
│   ├── skill_loader.py     # hot-reload dos skill_*.py
│   ├── config.py           # rede / auth / conselho de modelos
│   ├── Dockerfile
│   └── requirements.txt
├── skills/                 # 🧩 habilidades modulares (hot-reload, sem restart)
├── cli/                    # 💬 valen-chat (Oracle)
│   └── valen_chat.py       # REPL + one-shot + login JWT + trava y/n
├── android/                # 📱 app Kotlin/Jetpack Compose (controle remoto)
├── deploy/                 # 🚀 guias: DEPLOY_CONTABO / DEPLOY_ORACLE / DEPLOY_ANDROID
├── docker-compose.yml      # ollama (48GB) + brain (512MB)
└── .env.example
```

## Conselho de Modelos (Banca de Conselheiros)

Toda requisição ao `/chat` passa primeiro por um **roteador leve** (Llama 3 8B)
que escolhe o especialista:

| Especialista | Modelo padrão | Quando ativa |
|---|---|---|
| `frontend` | `qwen2.5-coder:7b` | telas, Kotlin/Compose, layouts visuais |
| `rapido` | `llama3:8b` | comandos de terminal, logs, conversas |
| `supremo` | `llama3:70b` | arquiteturas complexas, sistemas do zero (sobe à RAM só sob demanda) |

Roteador fora do ar? Fallback por heurística de palavras-chave — nunca fica mudo.

## Autenticação (usuário único)

- Credenciais do Admin no `.env` (hash PBKDF2 — nunca senha em texto puro).
- `POST /auth/login` → JWT Bearer de longa duração (padrão 30 dias).
- Sem rota de registro. O mesmo token serve para CLI, Android e Desktop futuro.

## API (referência rápida)

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| POST | `/auth/login` | — | `{usuario, senha}` → `{access_token, expira_em}` |
| GET | `/api/valen/v1/health` | — | verificação de vida |
| GET | `/api/valen/v1/skills` | JWT | catálogo de skills carregadas |
| POST | `/api/valen/v1/chat` | JWT | `{mensagem, contexto?}` → resposta estruturada |

Resposta do `/chat` (contrato rígido):

```json
{
  "skill_utilizada": "desenvolvimento",
  "modelo_utilizado": "qwen2.5-coder:7b",
  "tipo_acao": "codigo",
  "conteudo": "from flask import Flask...",
  "arquivo": "app.py",
  "explicacao": "Sistema de login em Flask com sessões."
}
```

## Deploy

Guias completos em `../deploy/`:
- **DEPLOY_CONTABO.md** — brain + ollama em Docker, firewall, modelos
- **DEPLOY_ORACLE.md** — instalar `valen-chat`, login, trava de segurança
- **DEPLOY_ANDROID.md** — compilar o app, configurar IP/porta, modal de confirmação

## Criando uma skill nova

Crie `skills/skill_minhaskill.py` — entra em vigor na requisição seguinte (hot-reload):

```python
SKILL_INFO = {
    "nome": "minhaskill",
    "descricao": "O que esta habilidade faz, em uma linha.",
    "gatilhos": ["palavra1", "palavra2"],  # termos que ativam a skill
}

INSTRUCOES = """
Você está operando com a skill MINHASKILL ativa.
1. Regras e diretrizes que o modelo deve seguir...
"""
```

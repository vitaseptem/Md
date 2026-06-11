# 🧠 Deploy do Brain — Servidor Contabo (96GB RAM)

O cérebro do Valen: FastAPI + Conselho de Modelos (Ollama) em Docker.

## 1. Pré-requisitos

```bash
# Docker + Compose plugin
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER && newgrp docker
```

## 2. Enviar o código para a Contabo

```bash
# Da sua máquina atual (Oracle):
rsync -av --exclude '__pycache__' --exclude 'android' \
  ~/VALEN_Vault_Engine/VALEN-Vault/ usuario@IP.DA.CONTABO:~/valen/
```

## 3. Configurar credenciais (USUÁRIO ÚNICO / Admin Master)

```bash
cd ~/valen
cp .env.example .env

# a) Hash da senha do Admin (a senha nunca fica em texto puro)
cd brain && pip install PyJWT && python gerar_hash.py "sua-senha-forte"
# -> cole a linha VALEN_ADMIN_PASSWORD_HASH=... no .env

# b) Segredo do JWT
openssl rand -hex 32
# -> cole em VALEN_JWT_SECRET=... no .env

# c) Defina VALEN_ADMIN_USER (ex: davi)
```

`.env` final:

| Variável | Função |
|---|---|
| `VALEN_ADMIN_USER` | Único usuário que pode logar |
| `VALEN_ADMIN_PASSWORD_HASH` | Hash PBKDF2 da senha (gerar_hash.py) |
| `VALEN_JWT_SECRET` | Assina os tokens (openssl rand -hex 32) |
| `VALEN_JWT_EXPIRE_DAYS` | Validade do token (padrão 30 dias) |
| `VALEN_MODELO_*` | Conselho de modelos (roteador/frontend/rápido/supremo) |

## 4. Subir o ecossistema

```bash
cd ~/valen
docker compose up -d --build

# 1ª vez: baixar o conselho de modelos (70B pesa ~40GB, demora)
docker compose exec ollama ollama pull llama3:8b
docker compose exec ollama ollama pull qwen2.5-coder:7b
docker compose exec ollama ollama pull llama3:70b
```

Limites de recursos (já no compose):
- **ollama**: 48GB RAM — 70B quantizado + modelos pequenos sob demanda
- **brain**: 512MB RAM / 1 CPU — só roteamento e segurança

## 5. Firewall (CRÍTICO)

A porta **8777** é a única exposta. Restrinja ao IP da Oracle:

```bash
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow from IP.DA.ORACLE to any port 8777 proto tcp
sudo ufw enable
```

> Para acesso do celular fora da rede da Oracle: prefira VPN (WireGuard/Tailscale)
> ou um proxy Nginx com TLS na 443, em vez de abrir a 8777 ao mundo.

## 6. Testar

```bash
# Health (sem auth)
curl http://localhost:8777/api/valen/v1/health

# Login -> JWT
curl -s -X POST http://localhost:8777/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"usuario":"davi","senha":"sua-senha-forte"}'

# Chat (use o access_token retornado acima)
curl -s -X POST http://localhost:8777/api/valen/v1/chat \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"mensagem":"liste os arquivos do diretório atual"}'
```

Resposta esperada (contrato rígido):

```json
{
  "skill_utilizada": "sysadmin",
  "modelo_utilizado": "llama3:8b",
  "tipo_acao": "comando",
  "conteudo": "ls -la",
  "arquivo": null,
  "explicacao": "Lista os arquivos do diretório atual"
}
```

## 7. Skills (hot-reload)

Crie/edite `skills/skill_*.py` a qualquer momento — entram em vigor na
próxima requisição, **sem restart**. Contrato mínimo:

```python
SKILL_INFO = {"nome": "minha_skill", "descricao": "...", "gatilhos": ["palavra1", "palavra2"]}
INSTRUCOES = """Instruções injetadas no system prompt quando ativada."""
```

# 💻 Deploy na VPS Oracle — CLI + Mini-API

Papel da Oracle no ecossistema:
1. **CLI `valen-chat`** — chat de terminal, cliente do Brain.
2. **Mini-API (porta 8788)** — gateway do app Android: recebe via
   `valen-chat.astrazstudio.com.br` (vhost no jv_nginx), repassa
   auth/chat ao Brain (Contabo) e **executa nesta VPS** as ações
   confirmadas no modal do app. Auditoria em `~/.valen/execucoes.log`.

## Mini-API (systemd)

```bash
cd ~/VALEN_Vault_Engine/VALEN-Vault/mini-api
pip install -r requirements.txt
sudo cp valen-mini-api.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now valen-mini-api
```

Config no unit file (`Environment=`):
- `BRAIN_URL` — endereço do Brain (trocar para a Contabo quando subir)
- `VALEN_JWT_SECRET` — **o mesmo** do Brain (vem do EnvironmentFile `.env`)
- `VALEN_WORKDIR` — diretório onde os comandos confirmados executam

Firewall: o nginx em container alcança o host pela rede docker —
`sudo ufw allow from 172.21.0.0/16 to any port 8788 proto tcp`.

> ⚠ nginx.conf do jv_nginx é bind-mount de arquivo único: depois de
> editar, `nginx -s reload` não basta — use `docker restart jv_nginx`.

## 1. Instalar

```bash
cd ~/VALEN_Vault_Engine/VALEN-Vault/cli
pip install -r requirements.txt          # requests + rich
chmod +x valen_chat.py
sudo ln -sf "$(pwd)/valen_chat.py" /usr/local/bin/valen-chat
```

## 2. Primeiro login

```bash
valen-chat login
```

A CLI pergunta:
- **IP do servidor** → IP da Contabo
- **Porta** → `8777` (padrão)
- **Usuário/Senha** → credenciais do Admin Master (as mesmas do .env da Contabo)

O JWT retornado fica salvo em `~/.config/valen/config.json` com permissão
`600` (só seu usuário lê). Expirou? A CLI pede relogin sozinha.

## 3. Usar

```bash
valen-chat                          # chat interativo (REPL)
valen-chat "crie um script de backup"   # one-shot
valen-chat logout                   # apaga o token local
```

Comandos dentro do chat: `/skills`, `/login`, `/limpar`, `/ajuda`, `/sair`.

## 4. Trava de segurança

Quando o Brain devolve `tipo_acao: "comando"` ou `"codigo"`, a CLI:
1. Mostra o comando/código com syntax highlight;
2. Pergunta `(y/n)` — **nada roda sem confirmação explícita**;
3. Só então executa via `subprocess` (ou grava o arquivo).

Sobrescrita de arquivo existente exige um segundo `y`.

## 5. Variáveis de ambiente (opcional, sobrescrevem o config.json)

```bash
export VALEN_SERVER_IP=1.2.3.4
export VALEN_SERVER_PORT=8777
export VALEN_TOKEN=eyJ...      # útil em scripts
export VALEN_TIMEOUT=600       # segundos (70B pode demorar)
```

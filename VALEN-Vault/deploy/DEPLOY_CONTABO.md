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

# 1ª vez: baixar os conselheiros leves
docker compose exec ollama ollama pull llama3:8b
docker compose exec ollama ollama pull qwen2.5-coder:7b
```

Limites de recursos (já no compose):
- **ollama**: 56GB RAM — 70B quantizado (q4_K_M ≈ 43GB) + modelos pequenos sob demanda
- **brain**: 512MB RAM / 1 CPU — só roteamento e segurança

## 4b. Especialista Supremo — Llama 3.3 70B puro da Meta

O Especialista Supremo usa os **pesos oficiais da Meta**
(`meta-llama/Llama-3.3-70B-Instruct`), baixados direto do Hugging Face e
registrados no Ollama como `llama3.3-meta-puro`. Qualidade de classe 405B
a uma fração do hardware — feito sob medida para os 96GB da Contabo.

> **Antes de começar:**
> 1. Aceite a licença da Meta na página do modelo:
>    https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
> 2. Crie um token de acesso: https://huggingface.co/settings/tokens
> 3. Garanta **~190GB livres no SSD** durante o build (os ~140GB de
>    safetensors podem ser apagados depois que o Ollama registrar o modelo).

### Caminho rápido (script pronto)

```bash
cd ~/valen
bash deploy/contabo_meta_llama33.sh
```

O script pergunta a rota de download:

| Rota | Fonte | Formato | SSD no build | Observação |
|---|---|---|---|---|
| **1** (recomendada) | Hugging Face | safetensors | ~190GB | Ollama importa direto |
| **2** | URL assinada do llama.com | `.pth` | ~330GB | Você cola a URL na hora (**expira em ~48h** — pegue uma nova no site no momento do deploy); o script converte `.pth` → safetensors antes do Ollama |

> Rota 2: pegue a URL em https://www.llama.com/llama-downloads imediatamente
> antes de rodar o script. URL antiga = assinatura vencida = download negado.

### Caminho manual (passo a passo — rota Hugging Face)

```bash
# 1. Instalar o git-xet necessário para o repositório
curl -sSfL https://hf.co/git-xet/install.sh | sh

# 2. Instalar a CLI oficial do Hugging Face
curl -LsSf https://hf.co/cli/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"

# 3. Autenticar (cole o token de acesso no prompt, ou exporte HF_TOKEN)
hf auth login

# 4. Baixar o modelo puro da Meta para o SSD, em pasta estruturada.
#    --exclude "original/*" pula os checkpoints .pth duplicados (~130GB a menos)
mkdir -p ~/models/Llama-3.3-70B-Instruct
hf download meta-llama/Llama-3.3-70B-Instruct \
  --local-dir ~/models/Llama-3.3-70B-Instruct \
  --exclude "original/*"
```

### Modelfile (formato de chat Llama 3 + caminho local dos pesos)

Crie `~/models/Modelfile` — o `FROM` aponta para o caminho **dentro do
container** (`~/models` do host é montado em `/models`, ver compose):

```dockerfile
# VALEN — Especialista Supremo: Llama 3.3 70B Instruct (Meta, puro)
FROM /models/Llama-3.3-70B-Instruct

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ range .Messages }}<|start_header_id|>{{ .Role }}<|end_header_id|>

{{ .Content }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

"""

PARAMETER stop <|start_header_id|>
PARAMETER stop <|end_header_id|>
PARAMETER stop <|eot_id|>
PARAMETER num_ctx 8192
```

### Buildar e registrar no Ollama

```bash
cd ~/valen
docker compose up -d ollama

# --quantize q4_K_M é OBRIGATÓRIO: em F16 o 70B ocupa ~140GB e NÃO cabe
# nos 96GB de RAM. Quantizado fica ~43GB e roda dentro do limite de 56GB.
docker compose exec ollama \
  ollama create llama3.3-meta-puro --quantize q4_K_M -f /models/Modelfile

# Teste direto no motor:
docker compose exec ollama ollama run llama3.3-meta-puro "Quem é você?"

# Liberar o SSD depois do registro (o modelo já vive no volume do Ollama):
rm -rf ~/models/Llama-3.3-70B-Instruct
```

O orquestrador já aponta o Especialista Supremo para esse ID
(`VALEN_MODELO_SUPREMO=llama3.3-meta-puro`, padrão no compose e no
`config.py`). Quando o supremo é convocado, o contrato JSON devolvido à
CLI da Oracle e ao app Kotlin informa:

```json
{ "modelo_utilizado": "llama3.3-meta-puro", ... }
```

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

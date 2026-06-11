#!/usr/bin/env bash
# =====================================================================
#  VALEN — Setup do Especialista Supremo na Contabo (96GB RAM)
#  Modelo: Llama-3.3-70B-Instruct (pesos puros e oficiais da Meta)
#  Destino: Ollama, registrado como "llama3.3-meta-puro"
#
#  DUAS ROTAS DE DOWNLOAD (o script pergunta qual usar):
#
#    [1] HUGGING FACE (recomendada)
#        - Já entrega safetensors, formato que o Ollama importa direto.
#        - Requer licença aceita no repo + token de acesso.
#        - ~190GB livres no SSD durante o build.
#
#    [2] URL ASSINADA DA META (llama.com)
#        - Você pega a URL no site na hora (ela expira em ~48h!) e
#          cola quando o script pedir.
#        - Entrega checkpoints .pth: o script CONVERTE para safetensors
#          antes do Ollama (passo extra, pesado).
#        - ~330GB livres no SSD durante o build (.pth + safetensors).
# =====================================================================
set -euo pipefail

MODELS_ROOT="$HOME/models"
MODELS_DIR="$MODELS_ROOT/Llama-3.3-70B-Instruct"
VALEN_DIR="${VALEN_DIR:-$HOME/valen}"
OLLAMA_TAG="llama3.3-meta-puro"
HF_MODEL_ID="meta-llama/Llama-3.3-70B-Instruct"
META_MODEL_ID="Llama3.3-70B-Instruct"
META_CHECKPOINT_DIR="$HOME/.llama/checkpoints/$META_MODEL_ID"

# ---------------------------------------------------------------
# Escolha da rota de download
# ---------------------------------------------------------------
echo "================================================================"
echo " VALEN — Download do Llama 3.3 70B (pesos oficiais da Meta)"
echo "================================================================"
echo "  [1] Hugging Face (recomendada — safetensors direto)"
echo "  [2] URL assinada do llama.com (cola a URL na hora; expira ~48h)"
echo
read -rp "Escolha a rota [1/2]: " ROTA
ROTA="${ROTA:-1}"

# ---------------------------------------------------------------
# Ferramentas comuns (CLI do Hugging Face serve às duas rotas:
# na rota 2 ela não é usada p/ download, mas custa nada ter)
# ---------------------------------------------------------------
echo "==> Instalando git-xet (transporte de blobs do Hugging Face)"
curl -sSfL https://hf.co/git-xet/install.sh | sh

echo "==> Instalando a CLI oficial do Hugging Face"
curl -LsSf https://hf.co/cli/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"

mkdir -p "$MODELS_DIR"

if [ "$ROTA" = "1" ]; then
    # ===========================================================
    # ROTA 1 — HUGGING FACE (safetensors, sem conversão)
    # ===========================================================
    echo "==> Autenticando no Hugging Face"
    if [ -z "${HF_TOKEN:-}" ]; then
        # Sem HF_TOKEN no ambiente: login interativo (cola o token)
        hf auth login
    fi

    echo "==> Baixando safetensors oficiais para $MODELS_DIR"
    # --exclude "original/*": pula os checkpoints .pth duplicados
    # (mesmos pesos em outro formato — economiza ~130GB de download)
    hf download "$HF_MODEL_ID" \
        --local-dir "$MODELS_DIR" \
        --exclude "original/*"
else
    # ===========================================================
    # ROTA 2 — URL ASSINADA DA META (llama.com)
    # ===========================================================
    echo
    echo ">>> Pegue uma URL NOVA agora em https://www.llama.com/llama-downloads"
    echo ">>> (a assinatura expira em ~48h — URL velha = download negado)"
    echo
    read -rp "Cole a URL assinada da Meta: " META_URL
    if [ -z "$META_URL" ]; then
        echo "ERRO: URL vazia. Rode de novo e cole a URL." >&2
        exit 1
    fi

    echo "==> Instalando llama-stack (CLI oficial de download da Meta)"
    pip install --user --upgrade llama-stack

    echo "==> Baixando checkpoints .pth da Meta (~140GB)"
    llama model download \
        --source meta \
        --model-id "$META_MODEL_ID" \
        --meta-url "$META_URL"

    echo "==> Convertendo .pth -> safetensors (formato que o Ollama importa)"
    # Llama 3.3 70B usa a MESMA arquitetura do 3.1 — por isso --llama_version 3.1.
    # Conversão é pesada: se faltar RAM, crie swap antes (fallocate + mkswap).
    pip install --user --upgrade "transformers>=4.47" torch accelerate \
        tiktoken blobfile sentencepiece safetensors
    python3 -m transformers.models.llama.convert_llama_weights_to_hf \
        --input_dir "$META_CHECKPOINT_DIR" \
        --output_dir "$MODELS_DIR" \
        --model_size 70B \
        --llama_version 3.1 \
        --instruct

    echo "==> Conversão concluída. Liberando os .pth originais (~140GB)"
    rm -rf "$META_CHECKPOINT_DIR"
fi

# ---------------------------------------------------------------
# Modelfile + registro no Ollama (igual para as duas rotas)
# ---------------------------------------------------------------
echo "==> Gerando o Modelfile (formato de chat Llama 3 + contrato JSON)"
cat > "$MODELS_ROOT/Modelfile" <<'MODELFILE'
# =====================================================================
#  VALEN — Especialista Supremo: Llama 3.3 70B Instruct (Meta, puro)
#  FROM aponta para o diretório dos safetensors oficiais, montado
#  dentro do container do Ollama em /models (ver docker-compose.yml).
# =====================================================================
FROM /models/Llama-3.3-70B-Instruct

# Template oficial de chat do Llama 3.x
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ range .Messages }}<|start_header_id|>{{ .Role }}<|end_header_id|>

{{ .Content }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

"""

PARAMETER stop <|start_header_id|>
PARAMETER stop <|end_header_id|>
PARAMETER stop <|eot_id|>

# Contexto de 8k: equilíbrio entre memória de conversa e RAM do KV cache
PARAMETER num_ctx 8192
MODELFILE

echo "==> Registrando no Ollama como '$OLLAMA_TAG' (quantização q4_K_M)"
cd "$VALEN_DIR"
docker compose up -d ollama
# q4_K_M é OBRIGATÓRIO: em F16 o 70B ocupa ~140GB e não cabe nos 96GB
# de RAM da Contabo. Quantizado fica ~43GB e roda dentro do limite.
docker compose exec ollama \
    ollama create "$OLLAMA_TAG" --quantize q4_K_M -f /models/Modelfile

echo
echo "✅ Modelo '$OLLAMA_TAG' registrado no Ollama."
echo
echo "Teste rápido:"
echo "  docker compose exec ollama ollama run $OLLAMA_TAG 'Quem é você?'"
echo
echo "Para liberar ~140GB de SSD depois que o modelo estiver no Ollama:"
echo "  rm -rf $MODELS_DIR"

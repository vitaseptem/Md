# =====================================================================
#  VALEN BRAIN — Dockerfile (servidor FastAPI na Contabo)
# =====================================================================
FROM python:3.12-slim

# Boas práticas: sem cache de pip, logs sem buffer (aparecem em tempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependências primeiro (camada cacheável — rebuild rápido quando só o código muda)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Código do cérebro
COPY config.py auth.py skill_loader.py orchestrator.py main.py gerar_hash.py ./

# Usuário não-root (segurança: container nunca roda como root)
RUN useradd --create-home valen && chown -R valen:valen /app
USER valen

EXPOSE 8777

# Healthcheck nativo: o compose marca o container unhealthy se a API cair
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8777/api/valen/v1/health', timeout=4)"

CMD ["python", "main.py"]

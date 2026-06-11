"""
=====================================================================
 VALEN BRAIN — AUTENTICAÇÃO (USUÁRIO ÚNICO + JWT)
=====================================================================
 Regra estrita de USUÁRIO ÚNICO (Administrador):
   - As credenciais do Admin vivem no .env (sem banco, sem registro).
   - POST /auth/login valida usuário+senha e emite um JWT Bearer
     com expiração longa (padrão: 30 dias).
   - Toda rota protegida valida o JWT via dependência `autenticar_jwt`.

 O token é um JWT HS256 padrão — funciona igual na CLI (Oracle),
 no app Android e em qualquer cliente futuro (Windows/Desktop).

 GERAR O HASH DA SENHA DO ADMIN:
   python gerar_hash.py "minha-senha-forte"
   -> cole o resultado em VALEN_ADMIN_PASSWORD_HASH no .env
=====================================================================
"""

import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from config import (
    VALEN_ADMIN_PASSWORD_HASH,
    VALEN_ADMIN_USER,
    VALEN_JWT_ALGORITHM,
    VALEN_JWT_EXPIRE_DAYS,
    VALEN_JWT_SECRET,
)

logger = logging.getLogger("valen.auth")

esquema_bearer = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------
# SENHA — PBKDF2-SHA256 (stdlib, sem dependências extras)
# Formato do hash: pbkdf2_sha256$<iterações>$<salt_hex>$<hash_hex>
# ---------------------------------------------------------------
def gerar_hash_senha(senha: str, iteracoes: int = 600_000) -> str:
    """Gera o hash PBKDF2 de uma senha (usado pelo gerar_hash.py)."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, iteracoes)
    return f"pbkdf2_sha256${iteracoes}${salt.hex()}${digest.hex()}"


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """Compara a senha informada com o hash do .env em tempo constante."""
    try:
        algoritmo, iteracoes, salt_hex, hash_hex = hash_armazenado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", senha.encode(), bytes.fromhex(salt_hex), int(iteracoes)
        )
        return secrets.compare_digest(digest.hex(), hash_hex)
    except (ValueError, AttributeError):
        logger.error("VALEN_ADMIN_PASSWORD_HASH malformado no .env.")
        return False


# ---------------------------------------------------------------
# JWT — emissão e validação
# ---------------------------------------------------------------
def criar_token(usuario: str) -> tuple[str, datetime]:
    """Emite um JWT assinado com expiração longa. Retorna (token, expira_em)."""
    agora = datetime.now(timezone.utc)
    expira_em = agora + timedelta(days=VALEN_JWT_EXPIRE_DAYS)
    payload = {
        "sub": usuario,
        "role": "admin",          # usuário único: sempre admin
        "iat": int(agora.timestamp()),
        "exp": int(expira_em.timestamp()),
        "iss": "valen-brain",
    }
    token = jwt.encode(payload, VALEN_JWT_SECRET, algorithm=VALEN_JWT_ALGORITHM)
    return token, expira_em


def autenticar_jwt(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
) -> str:
    """
    Dependência FastAPI: valida o Bearer Token JWT de TODA requisição
    protegida. Devolve o usuário (sub) ou levanta 401.
    """
    if credenciais is None:
        raise HTTPException(status_code=401, detail="Token ausente. Faça login em /auth/login.")
    try:
        payload = jwt.decode(
            credenciais.credentials,
            VALEN_JWT_SECRET,
            algorithms=[VALEN_JWT_ALGORITHM],
            issuer="valen-brain",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")

    usuario = payload.get("sub", "")
    # Usuário único: mesmo com JWT válido, só o Admin do .env passa
    if not secrets.compare_digest(usuario, VALEN_ADMIN_USER):
        raise HTTPException(status_code=403, detail="Apenas o Administrador pode usar o Valen.")
    return usuario


# ---------------------------------------------------------------
# MODELOS DO LOGIN
# ---------------------------------------------------------------
class LoginRequest(BaseModel):
    usuario: str = Field(..., min_length=1, max_length=64)
    senha: str = Field(..., min_length=1, max_length=256)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expira_em: str          # ISO-8601 UTC


def realizar_login(req: LoginRequest) -> LoginResponse:
    """Valida as credenciais do Admin e emite o JWT. 401 em falha."""
    usuario_ok = secrets.compare_digest(req.usuario, VALEN_ADMIN_USER)
    senha_ok = verificar_senha(req.senha, VALEN_ADMIN_PASSWORD_HASH)
    if not (usuario_ok and senha_ok):
        logger.warning("Tentativa de login recusada para usuário '%s'.", req.usuario)
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")

    token, expira_em = criar_token(req.usuario)
    logger.info("Login do Admin '%s' bem-sucedido. Token expira em %s.", req.usuario, expira_em)
    return LoginResponse(access_token=token, expira_em=expira_em.isoformat())

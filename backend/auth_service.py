import os
import time
import hmac
import hashlib
import json
import base64
from typing import Optional, Dict, Any

# Clave secreta para firmar tokens JWT (se puede configurar en .env)
JWT_SECRET = os.getenv("JWT_SECRET", "dorisk-super-secret-key-truenas-2026-production")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRATION_SECONDS = 30 * 24 * 3600  # 30 días

def hash_password(password: str) -> str:
    """Genera un hash seguro para la contraseña con Salt"""
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}:{pwd_hash.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifica si la contraseña coincide con el hash guardado (soporta PBKDF2 y bcrypt estándar)"""
    if not stored_hash:
        return False
    
    # 1. Si es formato PBKDF2 (salt:hash)
    if ":" in stored_hash:
        try:
            salt_hex, hash_hex = stored_hash.split(":")
            salt = bytes.fromhex(salt_hex)
            test_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
            return hmac.compare_digest(test_hash.hex(), hash_hex)
        except Exception:
            return False

    # 2. Si viene de Supabase (formato bcrypt $2a$ / $2b$ / $2y$)
    if stored_hash.startswith("$2"):
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except ImportError:
            # Fallback simple
            pass

    return False

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def _base64url_decode(data_str: str) -> bytes:
    padding = "=" * (4 - (len(data_str) % 4)) if len(data_str) % 4 != 0 else ""
    return base64.urlsafe_b64decode((data_str + padding).encode("utf-8"))

def create_access_token(data: dict) -> str:
    """Crea un token JWT nativo firmado con HS256"""
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    payload["exp"] = int(time.time()) + TOKEN_EXPIRATION_SECONDS
    payload["iat"] = int(time.time())

    header_b64 = _base64url_encode(json.dumps(header).encode("utf-8"))
    payload_b64 = _base64url_encode(json.dumps(payload).encode("utf-8"))

    signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        f"{header_b64}.{payload_b64}".encode("utf-8"),
        hashlib.sha256
    ).digest()
    signature_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Valida y decodifica un token JWT nativo"""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts

        # Validar firma
        expected_sig = hmac.new(
            JWT_SECRET.encode("utf-8"),
            f"{header_b64}.{payload_b64}".encode("utf-8"),
            hashlib.sha256
        ).digest()
        actual_sig = _base64url_decode(signature_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = _base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))

        # Validar expiración
        if "exp" in payload and payload["exp"] < time.time():
            return None

        return payload
    except Exception:
        return None

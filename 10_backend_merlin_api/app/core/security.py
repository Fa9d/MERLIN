from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import json
import secrets

from app.core.config import settings

PASSWORD_SCHEME = "scrypt"
TOKEN_VERSION = "v1"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
    )
    return ":".join(
        [
            PASSWORD_SCHEME,
            salt.hex(),
            digest.hex(),
        ]
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        scheme, salt_hex, digest_hex = stored_hash.split(":")
    except ValueError:
        return False

    if scheme != PASSWORD_SCHEME:
        return False

    calculated = hashlib.scrypt(
        password.encode("utf-8"),
        salt=bytes.fromhex(salt_hex),
        n=2**14,
        r=8,
        p=1,
    ).hex()
    return hmac.compare_digest(calculated, digest_hex)


def create_access_token(subject: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "ver": TOKEN_VERSION,
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(minutes=settings.auth_access_token_expire_minutes)).timestamp()
        ),
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(body).decode("utf-8").rstrip("=")
    signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload_b64}.{signature}"


def decode_access_token(token: str) -> dict:
    try:
        payload_b64, signature = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Malformed token.") from exc

    expected_signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid token signature.")

    padded = payload_b64 + "=" * (-len(payload_b64) % 4)
    payload = json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))
    if payload.get("ver") != TOKEN_VERSION:
        raise ValueError("Unsupported token version.")

    now_ts = int(datetime.now(timezone.utc).timestamp())
    if int(payload.get("exp", 0)) < now_ts:
        raise ValueError("Expired token.")

    return payload

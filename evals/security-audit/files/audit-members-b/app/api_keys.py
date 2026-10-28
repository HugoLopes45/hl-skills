import hashlib
import secrets


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_key(db, tenant_id: int, user_id: int) -> str:
    token = "pk_" + secrets.token_urlsafe(32)
    db.execute(
        "INSERT INTO api_keys (token_hash, tenant_id, user_id) VALUES (%s, %s, %s)",
        (_digest(token), tenant_id, user_id),
    )
    db.commit()
    return token


def authenticate(db, token: str):
    return db.execute(
        "SELECT k.tenant_id, k.user_id FROM api_keys k"
        " JOIN memberships m ON m.tenant_id = k.tenant_id AND m.user_id = k.user_id"
        " WHERE k.token_hash = %s AND k.revoked_at IS NULL",
        (_digest(token),),
    ).fetchone()

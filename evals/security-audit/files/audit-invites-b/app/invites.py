import hashlib
import secrets


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_invite(db, tenant_id: int, email: str, role: str) -> str:
    token = secrets.token_urlsafe(32)
    db.execute(
        "INSERT INTO invites (tenant_id, email, role, token_hash, expires_at) "
        "VALUES (%s, %s, %s, %s, now() + interval '7 days')",
        (tenant_id, email, role, _digest(token)),
    )
    db.commit()
    return token


def accept_invite(db, token: str, user_id: int) -> int | None:
    invite = db.execute(
        "SELECT tenant_id, role FROM invites WHERE token_hash = %s AND expires_at > now()", (_digest(token),)
    ).fetchone()
    if invite is None:
        return None
    db.execute(
        "INSERT INTO memberships (tenant_id, user_id, role) VALUES (%s, %s, %s) "
        "ON CONFLICT (tenant_id, user_id) DO NOTHING",
        (invite.tenant_id, user_id, invite.role),
    )
    db.commit()
    return invite.tenant_id

from flask import abort, session

from app.db import get_db


def current_membership(tenant_id: int):
    user_id = session.get("user_id")
    if user_id is None:
        abort(401)
    row = get_db().execute(
        "SELECT tenant_id, user_id, role FROM memberships WHERE tenant_id = %s AND user_id = %s",
        (tenant_id, user_id),
    ).fetchone()
    if row is None:
        abort(403)
    return row


def require_admin(tenant_id: int):
    membership = current_membership(tenant_id)
    if membership.role != "admin":
        abort(403)
    return membership

import os

from flask import Flask, abort, jsonify, request, session

from app.auth import require_admin
from app.db import get_db
from app.invites import accept_invite, create_invite

app = Flask(__name__)
app.secret_key = os.environ["SESSION_SECRET"]


@app.post("/tenants/<int:tenant_id>/invites")
def new_invite(tenant_id: int):
    require_admin(tenant_id)
    body = request.get_json()
    role = body.get("role", "member")
    if role not in ("member", "admin"):
        abort(400)
    return jsonify({"token": create_invite(get_db(), tenant_id, body["email"], role)}), 201


@app.post("/invites/<token>/accept")
def accept(token: str):
    user_id = session.get("user_id")
    if user_id is None:
        abort(401)
    tenant_id = accept_invite(get_db(), token, user_id)
    if tenant_id is None:
        abort(404)
    return jsonify({"tenant_id": tenant_id})

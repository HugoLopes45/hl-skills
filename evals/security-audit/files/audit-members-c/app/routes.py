import os

from flask import Flask, abort, jsonify, request

from app.api_keys import authenticate, create_key
from app.auth import current_membership, require_admin
from app.db import get_db
from app.members import remove_member

app = Flask(__name__)
app.secret_key = os.environ["SESSION_SECRET"]


@app.delete("/tenants/<int:tenant_id>/members/<int:user_id>")
def delete_member(tenant_id: int, user_id: int):
    require_admin(tenant_id)
    remove_member(get_db(), tenant_id, user_id)
    return "", 204


@app.post("/tenants/<int:tenant_id>/api-keys")
def new_api_key(tenant_id: int):
    membership = current_membership(tenant_id)
    return jsonify({"token": create_key(get_db(), membership.tenant_id, membership.user_id)}), 201


@app.get("/api/v1/projects")
def list_projects():
    header = request.headers.get("Authorization", "")
    principal = authenticate(get_db(), header.removeprefix("Bearer ")) if header.startswith("Bearer ") else None
    if principal is None:
        abort(401)
    rows = get_db().execute(
        "SELECT id, name, budget_cents FROM projects WHERE tenant_id = %s", (principal.tenant_id,)
    ).fetchall()
    return jsonify({"projects": [row._asdict() for row in rows]})

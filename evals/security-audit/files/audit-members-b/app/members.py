def remove_member(db, tenant_id: int, user_id: int) -> None:
    db.execute("DELETE FROM memberships WHERE tenant_id = %s AND user_id = %s", (tenant_id, user_id))
    db.execute(
        "UPDATE api_keys SET revoked_at = now() WHERE tenant_id = %s AND user_id = %s AND revoked_at IS NULL",
        (tenant_id, user_id),
    )
    db.commit()

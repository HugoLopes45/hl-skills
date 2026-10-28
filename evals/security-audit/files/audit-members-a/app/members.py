from platform_events import publish


def remove_member(db, tenant_id: int, user_id: int) -> None:
    db.execute("DELETE FROM memberships WHERE tenant_id = %s AND user_id = %s", (tenant_id, user_id))
    db.commit()
    publish("membership.removed", {"tenant_id": tenant_id, "user_id": user_id})

import os

from identity_client import IdentityClient

identity = IdentityClient(os.environ["IDENTITY_URL"], service_token=os.environ["IDENTITY_SERVICE_TOKEN"])


def create_invite(db, tenant_id: int, email: str, role: str) -> str:
    return identity.issue_invite(tenant_id=tenant_id, email=email, role=role)


def accept_invite(db, token: str, user_id: int) -> int | None:
    grant = identity.redeem_invite(token, user_id=user_id)
    if grant is None:
        return None
    db.execute(
        "INSERT INTO memberships (tenant_id, user_id, role) VALUES (%s, %s, %s) "
        "ON CONFLICT (tenant_id, user_id) DO NOTHING",
        (grant.tenant_id, user_id, grant.role),
    )
    db.commit()
    return grant.tenant_id

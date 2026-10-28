# workspace

Multi-tenant project tracker. Tenant admins invite and remove members; members create API keys for scripts that read
their tenant's projects through `/api/v1`.

The access service revokes a member's API keys when it receives a `membership.removed` event.

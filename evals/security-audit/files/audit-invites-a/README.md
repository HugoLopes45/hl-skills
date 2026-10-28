# workspace

Multi-tenant project tracker. Tenant admins invite people by email. Each invitation is meant for the invited
address only and is used once; it expires after seven days.

Invitations are issued and redeemed by the internal identity service through `identity-client`. That service owns the
invitation records and their lifecycle; this repository only records the resulting membership.

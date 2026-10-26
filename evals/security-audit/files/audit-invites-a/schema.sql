CREATE TABLE users (
    id             bigserial PRIMARY KEY,
    email          text NOT NULL UNIQUE,
    email_verified boolean NOT NULL DEFAULT false
);

CREATE TABLE memberships (
    tenant_id bigint NOT NULL,
    user_id   bigint NOT NULL REFERENCES users (id),
    role      text NOT NULL CHECK (role IN ('member', 'admin')),
    PRIMARY KEY (tenant_id, user_id)
);

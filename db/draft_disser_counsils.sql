CREATE TABLE persons (
    id              BIGSERIAL PRIMARY KEY,
    last_name       VARCHAR(100) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    middle_name     VARCHAR(100)
);

CREATE TABLE specialties (
    code            VARCHAR(50) NOT NULL PRIMARY KEY,
    name            VARCHAR(500) NOT NULL
);

CREATE TABLE dissertation_councils (
    code            VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE orders (
    id              BIGSERIAL PRIMARY KEY,
    number          VARCHAR(50) NOT NULL,
    order_date      DATE NOT NULL,
    council_id      BIGINT
);

CREATE TABLE council_memberships (
    id              BIGSERIAL PRIMARY KEY,

    council_id      BIGINT NOT NULL,
    person_id       BIGINT NOT NULL,
    order_id        BIGINT,

    role            VARCHAR(50) NOT NULL
);

CREATE TABLE council_specialties (
    council_id      BIGINT NOT NULL,
    specialty_id    BIGINT NOT NULL
);
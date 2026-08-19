-- Defence Papers Service
-- Draft schema for PostgreSQL
-- Test database: business-level constraints are intentionally minimal.

BEGIN;

-- ============================================================
-- 1. Persons
-- ============================================================

CREATE TABLE persons (
    id                  BIGSERIAL PRIMARY KEY,

    last_name           VARCHAR(100),
    first_name          VARCHAR(100),
    middle_name         VARCHAR(100),

    birth_date          DATE,
    citizenship         VARCHAR(100),

    email               VARCHAR(255),
    phone               VARCHAR(50),

    snils               VARCHAR(50),
    inn                 VARCHAR(50),

    gender              VARCHAR(20)
);

-- ============================================================
-- 2. Name declensions
-- One reusable set of six case forms for a single name element.
-- The same row may be referenced by many persons.
-- ============================================================

CREATE TABLE name_declensions (
    id                  BIGSERIAL PRIMARY KEY,

    nominative           VARCHAR(100),
    genitive             VARCHAR(100),
    dative               VARCHAR(100),
    accusative            VARCHAR(100),
    instrumental         VARCHAR(100),
    prepositional        VARCHAR(100)
);

ALTER TABLE persons
    ADD COLUMN last_name_declension_id
        BIGINT REFERENCES name_declensions(id),
    ADD COLUMN first_name_declension_id
        BIGINT REFERENCES name_declensions(id),
    ADD COLUMN middle_name_declension_id
        BIGINT REFERENCES name_declensions(id);

-- ============================================================
-- 3. Addresses
-- ============================================================

CREATE TABLE addresses (
    id                  BIGSERIAL PRIMARY KEY,

    postal_code         VARCHAR(20),
    address_text        VARCHAR(500)
);

-- ============================================================
-- 4. Organization reference tables
-- ============================================================

CREATE TABLE organization_types (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

CREATE TABLE affiliations (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

-- ============================================================
-- 5. Organizations
-- ============================================================

CREATE TABLE organizations (
    id                  BIGSERIAL PRIMARY KEY,

    full_name           VARCHAR(500),
    short_name          VARCHAR(300),

    affiliation_id      BIGINT REFERENCES affiliations(id),
    organization_type_id BIGINT REFERENCES organization_types(id),

    address_id          BIGINT REFERENCES addresses(id)
);

-- ============================================================
-- 6. Employment
-- A person may have multiple employments.
-- ============================================================

CREATE TABLE employments (
    id                  BIGSERIAL PRIMARY KEY,

    person_id           BIGINT REFERENCES persons(id),
    organization_id     BIGINT REFERENCES organizations(id),

    department          VARCHAR(300),
    position            VARCHAR(300)
);

-- ============================================================
-- 7. Academic reference data
-- ============================================================

CREATE TABLE academic_degrees (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

CREATE TABLE academic_titles (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

CREATE TABLE academic_ranks (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

-- ============================================================
-- 8. Scientific specialties
-- ============================================================

CREATE TABLE specialties (
    id                  BIGSERIAL PRIMARY KEY,

    code                VARCHAR(50),
    name                VARCHAR(500)
);

CREATE TABLE science_branches (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(300)
);

-- ============================================================
-- 9. Dissertation councils
-- Service/reference data, not a user-created entity.
-- ============================================================

CREATE TABLE dissertation_councils (
    id                  BIGSERIAL PRIMARY KEY,

    code                VARCHAR(50),
    name                VARCHAR(300)
);

CREATE TABLE council_specialties (
    council_id          BIGINT REFERENCES dissertation_councils(id),
    specialty_id        BIGINT REFERENCES specialties(id)
);

-- ============================================================
-- 10. Orders establishing / changing council composition
-- One order belongs to one council.
-- ============================================================

CREATE TABLE orders (
    id                  BIGSERIAL PRIMARY KEY,

    number              VARCHAR(50),
    order_date          DATE,

    council_id          BIGINT REFERENCES dissertation_councils(id)
);

-- ============================================================
-- 11. Council membership
-- A row means that a person was appointed to a council
-- by a particular order in a particular role.
-- ============================================================

CREATE TABLE council_memberships (
    id                  BIGSERIAL PRIMARY KEY,

    council_id          BIGINT REFERENCES dissertation_councils(id),
    person_id           BIGINT REFERENCES persons(id),
    order_id            BIGINT REFERENCES orders(id),

    role                VARCHAR(50)
);

-- ============================================================
-- 12. Applicants
-- Applicant-specific entity linked to a person.
-- ============================================================

CREATE TABLE applicants (
    id                  BIGSERIAL PRIMARY KEY,

    person_id           BIGINT REFERENCES persons(id)
);

-- ============================================================
-- 13. Dissertations
-- ============================================================

CREATE TABLE dissertations (
    id                          BIGSERIAL PRIMARY KEY,

    applicant_id                BIGINT REFERENCES applicants(id),

    title                       VARCHAR(1000),

    council_id                  BIGINT REFERENCES dissertation_councils(id),
    science_branch_id           BIGINT REFERENCES science_branches(id),
    specialty_id                BIGINT REFERENCES specialties(id),

    postgraduate_start_date     DATE,
    postgraduate_end_date       DATE,

    organization_id             BIGINT REFERENCES organizations(id),
    organization_department     VARCHAR(300)
);

-- ============================================================
-- 14. Dissertation participants
-- Supervisor, consultant, opponents, etc.
-- ============================================================

CREATE TABLE dissertation_participants (
    id                  BIGSERIAL PRIMARY KEY,

    dissertation_id     BIGINT REFERENCES dissertations(id),
    person_id           BIGINT REFERENCES persons(id),

    role                VARCHAR(50),

    academic_degree_id  BIGINT REFERENCES academic_degrees(id),
    academic_title_id   BIGINT REFERENCES academic_titles(id),
    academic_rank_id    BIGINT REFERENCES academic_ranks(id),
    specialty_id        BIGINT REFERENCES specialties(id),

    employment_id       BIGINT REFERENCES employments(id)
);

-- ============================================================
-- 15. Dissertation information card
-- ============================================================

CREATE TABLE dissertation_information (
    id                                  BIGSERIAL PRIMARY KEY,

    dissertation_id                     BIGINT REFERENCES dissertations(id),

    dissertation_pages                  INTEGER,
    appendix_count                      INTEGER,
    table_count                         INTEGER,
    illustration_count                  INTEGER,
    source_count                        INTEGER,

    bibliography_pages                  VARCHAR(100),

    publication_count_total             INTEGER,
    publication_count_international     INTEGER,
    publication_count_peer_reviewed     INTEGER,
    scientific_works_count              INTEGER,

    abstract                            TEXT
);

-- ============================================================
-- 16. Keywords
-- ============================================================

CREATE TABLE keywords (
    id                  BIGSERIAL PRIMARY KEY,
    value               VARCHAR(200)
);

CREATE TABLE dissertation_keywords (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    keyword_id          BIGINT REFERENCES keywords(id)
);

-- ============================================================
-- 17. GRNTI codes
-- ============================================================

CREATE TABLE grnti_codes (
    id                  BIGSERIAL PRIMARY KEY,

    code                VARCHAR(50),
    name                VARCHAR(500)
);

CREATE TABLE dissertation_grnti_codes (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    grnti_code_id       BIGINT REFERENCES grnti_codes(id)
);

-- ============================================================
-- 18. OECD codes
-- ============================================================

CREATE TABLE oecd_codes (
    id                  BIGSERIAL PRIMARY KEY,

    code                VARCHAR(50),
    name                VARCHAR(500),
    level               INTEGER
);

CREATE TABLE dissertation_oecd_codes (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    oecd_code_id        BIGINT REFERENCES oecd_codes(id)
);

-- ============================================================
-- 19. Critical technologies / priorities
-- ============================================================

CREATE TABLE critical_technologies (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(500)
);

CREATE TABLE dissertation_critical_technologies (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    critical_technology_id BIGINT REFERENCES critical_technologies(id)
);

CREATE TABLE priority_directions (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(500)
);

CREATE TABLE dissertation_priority_directions (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    priority_direction_id BIGINT REFERENCES priority_directions(id)
);

CREATE TABLE scientific_development_priorities (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(500)
);

CREATE TABLE dissertation_scientific_development_priorities (
    dissertation_id     BIGINT REFERENCES dissertations(id),
    priority_id         BIGINT REFERENCES scientific_development_priorities(id)
);

-- ============================================================
-- 20. Documents
-- ============================================================

CREATE TABLE document_types (
    id                  BIGSERIAL PRIMARY KEY,

    code                VARCHAR(100),
    name                VARCHAR(300)
);

CREATE TABLE documents (
    id                  BIGSERIAL PRIMARY KEY,

    dissertation_id     BIGINT REFERENCES dissertations(id),
    document_type_id    BIGINT REFERENCES document_types(id),

    status               VARCHAR(50),

    file_path            VARCHAR(1000),

    created_at           TIMESTAMP,
    updated_at           TIMESTAMP
);

COMMIT;

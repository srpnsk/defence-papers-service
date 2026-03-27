CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name varchar(32) NOT NULL,
    first_name varchar(32) NOT NULL, -- фамилия
    last_name varchar(32) NOT NULL, -- отчество
);

CREATE TABLE thesis (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE thesis_person (
    id SERIAL PRIMARY KEY,
    thesis_id INT REFERENCES thesis(id) ON DELETE CASCADE,
    person_id INT REFERENCES person(id),

    role TEXT NOT NULL, -- applicant, supervisor, opponent, chairman, secretary
    order_index INT,    -- только для opponent

    UNIQUE (thesis_id, person_id, role)
);

CREATE TABLE dissertation_council (
    id SERIAL PRIMARY KEY,
    name TEXT
);

ALTER TABLE thesis
ADD COLUMN council_id INT REFERENCES dissertation_council(id);

CREATE TABLE document_type (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    thesis_id INT REFERENCES thesis(id) ON DELETE CASCADE,
    type_id INT REFERENCES document_type(id),

    file_path TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


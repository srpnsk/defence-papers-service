CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    degree TEXT,
    title TEXT,
    affiliation TEXT
);

CREATE TABLE thesis (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    defense_date DATE
);

ALTER TABLE thesis
ADD COLUMN supervisor_id INT REFERENCES person(id);

CREATE TABLE opponents (
    id SERIAL PRIMARY KEY,
    thesis_id INT REFERENCES thesis(id) ON DELETE CASCADE,
    person_id INT REFERENCES person(id),
    order_index INT NOT NULL,

    UNIQUE (thesis_id, order_index),
    UNIQUE (thesis_id, person_id)
);

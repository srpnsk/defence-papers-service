CREATE TABLE IF NOT EXISTS public.users (
    id bigserial PRIMARY KEY,
    person_id bigint REFERENCES public.person(id) NOT NULL,
    email varchar(128) NOT NULL,
    hashed_password char(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.sessions (
    session_id bigserial PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) NOT NULL
);

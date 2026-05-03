CREATE TABLE IF NOT EXISTS public.users (
    id bigserial PRIMARY KEY,
    person_id bigint REFERENCES public.person(id) NOT NULL,
    email varchar(128) NOT NULL UNIQUE,
    hashed_password char(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.sessions (
    session_id UUID PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE CASCADE NOT NULL
);

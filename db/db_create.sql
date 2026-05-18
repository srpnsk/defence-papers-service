BEGIN;

CREATE TABLE IF NOT EXISTS public.organization (
    id bigserial PRIMARY KEY,
    full_name text NOT NULL,
    short_name varchar(128) NOT NULL,
    address text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.city (
    id bigserial PRIMARY KEY,
    name varchar(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.specialty (
    id bigserial PRIMARY KEY,
    code varchar(32) UNIQUE NOT NULL,
    name text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.person (
    id bigserial PRIMARY KEY,
    last_name varchar(64) NOT NULL,
    first_name varchar(64) NOT NULL,
    second_name varchar(64),
    degree varchar(128),
    academic_title varchar(128),
    email varchar(128) UNIQUE,
    phone_number varchar(64),
    specialty_id bigint REFERENCES public.specialty(id)
);

CREATE TABLE IF NOT EXISTS public.employment_history (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    organization_id bigint NOT NULL REFERENCES public.organization(id),
    position text,
    division text,
    start_date date NOT NULL,
    end_date date,
    is_additional boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS public.education_history (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    edu_level varchar(64),
    end_year integer,
    is_honors boolean DEFAULT false,
    qualification varchar(128),
    reference_date date,
    organization_id bigint REFERENCES public.organization(id),
    specialty_id bigint REFERENCES public.specialty(id)
);

CREATE TABLE IF NOT EXISTS public.applicant_details (
    person_id bigint PRIMARY KEY REFERENCES public.person(id) ON DELETE CASCADE,
    snils varchar(14) NOT NULL,
    passport_type varchar(32) NOT NULL,
    passport_series varchar(16) NOT NULL,
    passport_number varchar(16) NOT NULL,
    home_address text NOT NULL,
    sex smallint NOT NULL,
    birth_date date NOT NULL,
    is_postgrad_completed boolean NOT NULL DEFAULT false,
    postgrad_end_date date
);

CREATE TABLE IF NOT EXISTS public.dissertation_council (
    id bigserial PRIMARY KEY,
    "number" varchar(32) NOT NULL,
    organization_id bigint NOT NULL REFERENCES public.organization(id),
    chairman_id bigint NOT NULL REFERENCES public.person(id),
    secretary_id bigint NOT NULL REFERENCES public.person(id),
    members_count_total integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.thesis (
    id bigserial PRIMARY KEY,
    applicant_id bigint NOT NULL REFERENCES public.person(id),
    council_id bigint NOT NULL REFERENCES public.dissertation_council(id),
    title text NOT NULL,
    science_branch varchar(128) NOT NULL,
    target_degree varchar(128) NOT NULL,
    planned_defence_date date,
    defence_date_time timestamp with time zone,
    website_publish_date date,
    website_link text,
    dissertation_text_link text,
    achievement_summary text,
    reliability_text text,
    personal_participation text,
    specialty_id bigint NOT NULL REFERENCES public.specialty(id)
);

CREATE TABLE IF NOT EXISTS public.thesis_participation (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    person_id bigint NOT NULL REFERENCES public.person(id),
    role varchar(64) NOT NULL,
    order_index integer NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS public.achievement (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    type integer NOT NULL,
    text_content text NOT NULL,
    year integer NOT NULL,
    city_id bigint REFERENCES public.city(id),
    quartile varchar(32)
);

CREATE TABLE IF NOT EXISTS public.thesis_achievement (
    thesis_id bigint REFERENCES public.thesis(id) ON DELETE CASCADE,
    achievement_id bigint REFERENCES public.achievement(id) ON DELETE CASCADE,
    is_main boolean NOT NULL DEFAULT false,
    author_contribution text,
    PRIMARY KEY (thesis_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS public.thesis_content_block (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    block_type varchar(64) NOT NULL,
    content text NOT NULL,
    order_index integer NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS public.ds_event (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    event_type varchar(64) NOT NULL,
    protocol_number varchar(32) NOT NULL,
    protocol_date date NOT NULL,
    votes_total integer,
    votes_yes integer,
    votes_no integer,
    votes_abstain integer,
    present_offline integer DEFAULT 0,
    present_online integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.thesis_official_opponent (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    person_id bigint NOT NULL REFERENCES public.person(id),
    order_index integer NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS public.thesis_leading_organization (
    thesis_id bigint PRIMARY KEY REFERENCES public.thesis(id) ON DELETE CASCADE,
    organization_id bigint NOT NULL REFERENCES public.organization(id)
);

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

COMMIT;

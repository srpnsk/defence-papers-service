BEGIN;

-- 1. Справочник организаций (университеты, НИИ)
CREATE TABLE IF NOT EXISTS public.organization (
    id bigserial PRIMARY KEY,
    full_name text NOT NULL,
    short_name varchar(128) NOT NULL,
    address text NOT NULL
);

-- 2. Города (для конференций и адресов)
CREATE TABLE IF NOT EXISTS public.city (
    id bigserial PRIMARY KEY,
    name varchar(128) NOT NULL
);

-- 3. Базовая сущность - Человек
CREATE TABLE IF NOT EXISTS public.person (
    id bigserial PRIMARY KEY,
    last_name varchar(64) NOT NULL,
    first_name varchar(64) NOT NULL,
    second_name varchar(64),
    degree varchar(128), -- к.к.н.
    academic_title varchar(128), -- доцент
    email varchar(128),
    phone_number varchar(64),
    specialty_code varchar(32), -- Код специальности оппонента/научрука
    specialty_name text         -- Название специальности
);

-- 4. История работы (для проверки конфликта интересов и вывода в TeX)
CREATE TABLE IF NOT EXISTS public.employment_history (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    organization_id bigint NOT NULL REFERENCES public.organization(id),
    position text,      -- Должность (ассистент, профессор)
    division text,      -- Кафедра или отдел
    start_date date NOT NULL,
    end_date date,      -- NULL если работает сейчас
    is_additional boolean DEFAULT false -- Флаг совместительства
);

-- 5. Образование (объединили все версии в одну)
CREATE TABLE IF NOT EXISTS public.education_history (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    edu_level varchar(64), -- 'Master', 'Postgrad'
    institution_name text, -- 'НИЯУ МИФИ'
    specialty_code varchar(32),
    specialty_title text,
    end_year integer,
    is_honors boolean DEFAULT false, -- 'с отличием'
    qualification varchar(128),      -- 'магистр'
    reference_date date              -- Дата справки об окончании аспирантуры
);

-- 6. Детали соискателя (паспортные данные, СНИЛС)
CREATE TABLE IF NOT EXISTS public.applicant_details (
    person_id bigint PRIMARY KEY REFERENCES public.person(id) ON DELETE CASCADE,
    snils varchar(14) NOT NULL,
    passport_type varchar(32) NOT NULL,
    passport_series varchar(16) NOT NULL,
    passport_number varchar(16) NOT NULL,
    home_address text NOT NULL,
    sex smallint NOT NULL, -- 1-М, 2-Ж
    birth_date date NOT NULL,
    is_postgrad_completed boolean NOT NULL DEFAULT false,
    postgrad_end_date date
);

-- 7. Диссертационный совет
CREATE TABLE IF NOT EXISTS public.dissertation_council (
    id bigserial PRIMARY KEY,
    "number" varchar(32) NOT NULL,
    organization_id bigint NOT NULL REFERENCES public.organization(id),
    chairman_id bigint NOT NULL REFERENCES public.person(id),
    secretary_id bigint NOT NULL REFERENCES public.person(id),
    members_count_total integer NOT NULL
);

-- 8. Диссертация (все данные из \setkomavar)
CREATE TABLE IF NOT EXISTS public.thesis (
    id bigserial PRIMARY KEY,
    applicant_id bigint NOT NULL REFERENCES public.person(id),
    council_id bigint NOT NULL REFERENCES public.dissertation_council(id),
    title text NOT NULL,
    specialty_code varchar(32) NOT NULL,
    specialty_name text NOT NULL,
    science_branch varchar(128) NOT NULL,    -- "физико-математические"
    target_degree varchar(128) NOT NULL,     -- "кандидата наук"
    planned_defence_date varchar(64),        -- "сентябрь 2026"
    defence_date_time timestamp with time zone,
    website_publish_date date,
    website_link text,
    dissertation_text_link text,
    achievement_summary text,                -- "за разработку метода..."
    reliability_text text,                   -- Оценка достоверности
    personal_participation text              -- Личное участие (Personal participation)
);

-- 9. Оппоненты и Ведущая организация
CREATE TABLE IF NOT EXISTS public.thesis_opponent (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    person_id bigint REFERENCES public.person(id), 
    organization_id bigint REFERENCES public.organization(id),
    opponent_type smallint NOT NULL, -- 1 - Оппонент, 2 - Ведущая
    order_index integer NOT NULL DEFAULT 1,
    CONSTRAINT opponent_target_check CHECK (person_id IS NOT NULL OR organization_id IS NOT NULL)
);

-- 10. Участие (Научрук, Комиссия, Докладчик)
CREATE TABLE IF NOT EXISTS public.thesis_participation (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    person_id bigint NOT NULL REFERENCES public.person(id),
    role varchar(64) NOT NULL, -- 'supervisor', 'commission_member', 'speaker'
    order_index integer NOT NULL DEFAULT 1
);

-- 11. Достижения (Публикации, РИД, Конференции)
CREATE TABLE IF NOT EXISTS public.achievement (
    id bigserial PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES public.person(id) ON DELETE CASCADE,
    type integer NOT NULL, -- 1-Статья, 2-РИД, 3-Конференция
    text_content text NOT NULL, -- Библиографическая ссылка
    year integer NOT NULL,
    city_id bigint REFERENCES public.city(id),
    quartile varchar(32)  -- Q1, K2 и т.д.
);

-- 12. Связь Публикация <-> Диссертация
CREATE TABLE IF NOT EXISTS public.thesis_achievement (
    thesis_id bigint REFERENCES public.thesis(id) ON DELETE CASCADE,
    achievement_id bigint REFERENCES public.achievement(id) ON DELETE CASCADE,
    is_main boolean NOT NULL DEFAULT false, -- Статья ВАК/Scopus по теме
    author_contribution text,               -- Личный вклад в эту конкретную работу
    PRIMARY KEY (thesis_id, achievement_id)
);

-- 13. Текстовые блоки (Задачи, Новизна, Положения, Пункты паспорта)
CREATE TABLE IF NOT EXISTS public.thesis_content_block (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    block_type varchar(64) NOT NULL, -- 'task', 'novelty', 'provision', 'passport_item'
    content text NOT NULL,
    order_index integer NOT NULL DEFAULT 1
);

-- 14. Протоколы событий
CREATE TABLE IF NOT EXISTS public.ds_event (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    event_type varchar(64) NOT NULL, -- 'commission_creation', 'acceptance'
    protocol_number varchar(32) NOT NULL,
    protocol_date date NOT NULL,
    votes_total integer,
    votes_yes integer,
    votes_no integer,
    votes_abstain integer,
    present_offline integer DEFAULT 0,
    present_online integer DEFAULT 0
);

-- 1. Справочник специальностей (решаем проблему 3НФ)
CREATE TABLE IF NOT EXISTS public.specialty (
    id bigserial PRIMARY KEY,
    code varchar(32) UNIQUE NOT NULL,
    name text NOT NULL
);

-- 3. Обновленная таблица Person (ссылаемся на справочники)
-- В реальной БД тут был бы ALTER TABLE, но для ясности пересоздаем логику
ALTER TABLE public.person DROP COLUMN IF EXISTS specialty_code;
ALTER TABLE public.person DROP COLUMN IF EXISTS specialty_name;
ALTER TABLE public.person ADD COLUMN IF NOT EXISTS specialty_id bigint REFERENCES public.specialty(id);

-- 4. Рефакторинг образования (убираем текст, ставим ссылки)
ALTER TABLE public.education_history 
    DROP COLUMN IF EXISTS institution_name,
    DROP COLUMN IF EXISTS specialty_code,
    DROP COLUMN IF EXISTS specialty_title;

ALTER TABLE public.education_history 
    ADD COLUMN organization_id bigint REFERENCES public.organization(id),
    ADD COLUMN specialty_id bigint REFERENCES public.specialty(id);

-- 5. Разделение Оппонентов и Ведущей организации (2НФ)
-- Вместо одной таблицы с кучей NULL-полей делаем две четкие
DROP TABLE IF EXISTS public.thesis_opponent CASCADE;

CREATE TABLE IF NOT EXISTS public.thesis_official_opponent (
    id bigserial PRIMARY KEY,
    thesis_id bigint NOT NULL REFERENCES public.thesis(id) ON DELETE CASCADE,
    person_id bigint NOT NULL REFERENCES public.person(id),
    order_index integer NOT NULL DEFAULT 1 -- 1-й оппонент, 2-й и т.д.
);

CREATE TABLE IF NOT EXISTS public.thesis_leading_organization (
    thesis_id bigint PRIMARY KEY REFERENCES public.thesis(id) ON DELETE CASCADE,
    organization_id bigint NOT NULL REFERENCES public.organization(id)
);

-- 6. Чистим таблицу Thesis
ALTER TABLE public.thesis 
    DROP COLUMN IF EXISTS specialty_code,
    DROP COLUMN IF EXISTS specialty_name;

ALTER TABLE public.thesis 
    ADD COLUMN specialty_id bigint NOT NULL REFERENCES public.specialty(id);

-- Исправляем тип даты планируемой защиты для нормальной сортировки
ALTER TABLE public.thesis 
    ALTER COLUMN planned_defence_date TYPE date 
    USING (NULL); -- В реальной жизни тут нужен был бы сложный парсинг текста в дату

COMMIT;

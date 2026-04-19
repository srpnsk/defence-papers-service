-- =====================================================
-- ИСПРАВЛЕННЫЙ ФАЙЛ db_insert.sql
-- (исправлены:
--  1. NULL в science_branch таблицы thesis
--  2. NULL в address таблицы organization для НИЯУ МИФИ и НИИ ЛиУ
--  3. Синтаксическая ошибка в блоке DO $$
--  4. Ошибка с подзапросами внутри VALUES для вставки достижений)
-- =====================================================

INSERT INTO public.organization (full_name, short_name, address) VALUES
('Национальный исследовательский университет «КиС»', 'НИУ КиС', '111666, г. Кошкинск, Валерьяновая ул., д. 13'),
('Институт изучения кошачьих повадок РАН', 'ИИКП РАН', '666111, г. Мурмурск, Хвостатая ул., д. 2/1'),
('Институт гидродинамики', 'ИГ', '22222, г. Кошкск, Ушастый пр-д., д. 3'),
('Академия кошачьего хозяйства', 'АКХ', '333333, г. Лапск, Полосатый пр-д., д. 5');

INSERT INTO public.city (name) VALUES
('Кошкинск'),
('Мурмурск'),
('Кошкск'),
('Лапск'),
('Котейск');

INSERT INTO public.specialty (code, name) VALUES
('6.6.6', 'Физика котиков'),
('6.6.5', 'Физика больших котиков'),
('6.6.7', 'Физика малых котиков');

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Иванов', 'Иван', 'Иванович', NULL, NULL, 'ivanov@email.ru', '+0 000 000-00-00', (SELECT id FROM public.specialty WHERE code = '6.6.6'));

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Мяукало', 'М.М.', NULL, 'д.к.н', NULL, NULL, NULL, NULL);

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Кис-Кис', 'К.К.', NULL, 'к.к.н', NULL, NULL, NULL, NULL);

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Собакин', 'Собак', 'Собакович', 'д.к.н', 'профессор', 'sobakin@CaD.ru', '+7 666 000-00-00', (SELECT id FROM public.specialty WHERE code = '6.6.6'));

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Львов', 'Лев', 'Львович', 'д.к.н', 'профессор', 'lvov@cran.ru', '+7 555 000-00-00', (SELECT id FROM public.specialty WHERE code = '6.6.6'));

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Тигров', 'Тигр', 'Тигрович', 'к.к.н.', NULL, 'tigrov@hdi.ru', '+7 444 000-00-00', (SELECT id FROM public.specialty WHERE code = '6.6.5'));

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES ('Ягуарова', 'Ягуара', 'Ягуаровна', 'д.к.н.', 'доцент', 'yaguarova@acs.ru', '+7 555 000-00-00', (SELECT id FROM public.specialty WHERE code = '6.6.7'));

INSERT INTO public.applicant_details (
    person_id, snils, passport_type, passport_series, passport_number, 
    home_address, sex, birth_date, is_postgrad_completed, postgrad_end_date
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван' AND second_name = 'Иванович'),
    '000-000-00-00',
    'паспорт',
    '0000',
    '000000',
    'г. Котейск, Молочная ул., д 1',
    1,
    '1970-01-01',
    false,
    '2025-08-31'
);

INSERT INTO public.dissertation_council (number, organization_id, chairman_id, secretary_id, members_count_total)
VALUES (
    '1.01',
    (SELECT id FROM public.organization WHERE full_name = 'Национальный исследовательский университет «КиС»'),
    (SELECT id FROM public.person WHERE last_name = 'Мяукало'),
    (SELECT id FROM public.person WHERE last_name = 'Кис-Кис'),
    20
);

-- ===== ИСПРАВЛЕНО: science_branch = 'Физико-математические науки' =====
INSERT INTO public.thesis (
    applicant_id, council_id, title, science_branch, target_degree, 
    planned_defence_date, defence_date_time, specialty_id
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    (SELECT id FROM public.dissertation_council WHERE number = '1.01'),
    '"Гидродинамика движения заключительной трети хвоста полосатых котиков в условиях космической невесомости"',
    'Физико-математические науки',
    'кандидата котовьих наук',
    '2026-09-01',
    '2026-09-01 15:00:00+00', 
    (SELECT id FROM public.specialty WHERE code = '6.6.6')
);
-- =====================================================================

INSERT INTO public.thesis_official_opponent (thesis_id, person_id, order_index) VALUES
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Львов'),
    1
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Тигров'),
    2
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Ягуарова'),
    3
);

INSERT INTO public.employment_history (person_id, organization_id, position, division, start_date, end_date, is_additional)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    (SELECT id FROM public.organization WHERE full_name = 'Национальный исследовательский университет «КиС»'),
    'профессор',
    'кафедра Кошкодинамики',
    '2000-01-01',
    NULL,
    false
);

INSERT INTO public.employment_history (person_id, organization_id, position, division, start_date, end_date, is_additional)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Львов'),
    (SELECT id FROM public.organization WHERE full_name = 'Институт изучения кошачьих повадок РАН'),
    'Заведующий лабораторией',
    'Центр кошкологии',
    '2000-01-01',
    NULL,
    false
);

INSERT INTO public.employment_history (person_id, organization_id, position, division, start_date, end_date, is_additional)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Тигров'),
    (SELECT id FROM public.organization WHERE full_name = 'Институт гидродинамики'),
    'Начальник отдела',
    'Кафедра биологической гидродинамики',
    '2000-01-01',
    NULL,
    false
);

INSERT INTO public.employment_history (person_id, organization_id, position, division, start_date, end_date, is_additional)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Ягуарова'),
    (SELECT id FROM public.organization WHERE full_name = 'Академия кошачьего хозяйства'),
    'Ведущий научный сотрудник',
    'Отдел лап и усов',
    '2000-01-01',
    NULL,
    false
);

-- ===== ИСПРАВЛЕНО: address = '—' вместо NULL =====
INSERT INTO public.organization (full_name, short_name, address) VALUES
('НИЯУ МИФИ', 'НИЯУ МИФИ', '—'),
('НИИ ЛиУ', 'НИИ ЛиУ', '—');
-- ================================================

INSERT INTO public.specialty (code, name) VALUES
('14.14.14', 'Физика кошачьих конечностей'),
('13.13.13', 'Физика кошачьих хвостов');

UPDATE public.applicant_details 
SET postgrad_end_date = '2026-08-31'
WHERE person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван');

INSERT INTO public.education_history (
    person_id, edu_level, end_year, is_honors, qualification, 
    reference_date, organization_id, specialty_id
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    'магистратура НИЯУ МИФИ',
    2022,
    true,
    'магистр',
    NULL,
    (SELECT id FROM public.organization WHERE full_name = 'НИЯУ МИФИ'),
    (SELECT id FROM public.specialty WHERE code = '14.14.14')
);

INSERT INTO public.education_history (
    person_id, edu_level, end_year, is_honors, qualification, 
    reference_date, organization_id, specialty_id
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    'очной аспирантуре НИЯУ МИФИ',
    2026,
    false,
    NULL,
    '2026-08-31',
    (SELECT id FROM public.organization WHERE full_name = 'НИЯУ МИФИ'),
    (SELECT id FROM public.specialty WHERE code = '6.6.6')
);

INSERT INTO public.employment_history (
    person_id, organization_id, position, division, start_date, end_date, is_additional
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    (SELECT id FROM public.organization WHERE full_name = 'НИЯУ МИФИ'),
    'ассистента',
    'кафедра "Конденсированое состояние котиков" (№99)',
    '2022-09-01',
    NULL,
    false
);

INSERT INTO public.employment_history (
    person_id, organization_id, position, division, start_date, end_date, is_additional
)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    (SELECT id FROM public.organization WHERE full_name = 'НИИ ЛиУ'),
    'закручивателя хвостов',
    NULL,
    '2022-09-01',
    NULL,
    true
);

UPDATE public.thesis 
SET 
    achievement_summary = 'разработку метода оценки и рассчёта гидродинаимечских параметров заключительной трети хвоста полосатых котиков в условиях космической невесомости',
    personal_participation = 'Personal participation',
    reliability_text = 'Reliability of results',
    planned_defence_date = '2026-09-01'
WHERE title LIKE '%Гидродинамика движения%';

INSERT INTO public.achievement (person_id, type, text_content, year, quartile)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    1,
    'Иванов И.И., Собкин С.С. Свойства плавучести заключительной трети кошачего хвоста // Наши коты. 2026. Т. 2. С. 33--37.',
    2026,
    'Q3'
);

INSERT INTO public.achievement (person_id, type, text_content, year, quartile)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    1,
    'Иванов И.И., Собкин С.С. Гидрофильные свойства кошачей шерсти // Коты и кошки. 2025. Т. 6. С. 1234--1243.',
    2025,
    'К2'
);

INSERT INTO public.achievement (person_id, type, text_content, year, quartile)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    1,
    'Applicant article 3',
    2024,
    'Q3, К2'
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    2,
    'Иванов И.И., Собкин С.С. "Программа для расчёта свойства плавучести заключительной трети кошачего хвоста", Свидетельство для регистрации программы для ЭВМ № 123456789, 01 января 2025',
    2025
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    3,
    'Иванов И.И., Собакин С.С., Свойства плавучести поверхности кошачего хвоста, Всероссийская кошачья конференция, г. Кошанск. 2025',
    2025
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    3,
    'Иванов И.И., Собакин С.С., Кошачий хвост как гидрофобная поверхность, V Международная конференция "Кошачьи хвосты в мировой науке", г. Мурс. 2024',
    2024
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    3,
    'Applicant thesis 3',
    2023
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    3,
    'Applicant thesis 4',
    2023
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    3,
    'Applicant thesis 5',
    2022
);

-- ===== ИСПРАВЛЕННЫЙ БЛОК DO $$ =====
DO $$
DECLARE
    thesis_id_var bigint;
    achievement_id_var bigint;
BEGIN
    SELECT id INTO thesis_id_var FROM public.thesis WHERE title LIKE '%Гидродинамика движения%' LIMIT 1;
    
    SELECT id INTO achievement_id_var FROM public.achievement 
    WHERE person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван')
    AND text_content LIKE '%Свойства плавучести заключительной трети%' LIMIT 1;
    IF achievement_id_var IS NOT NULL THEN
        INSERT INTO public.thesis_achievement (thesis_id, achievement_id, is_main, author_contribution)
        VALUES (thesis_id_var, achievement_id_var, true, 'Author contribution 1');
    END IF;
    
    SELECT id INTO achievement_id_var FROM public.achievement 
    WHERE person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван')
    AND text_content LIKE '%Гидрофильные свойства%' LIMIT 1;
    IF achievement_id_var IS NOT NULL THEN
        INSERT INTO public.thesis_achievement (thesis_id, achievement_id, is_main, author_contribution)
        VALUES (thesis_id_var, achievement_id_var, false, 'Author contribution 2');
    END IF;
    
    SELECT id INTO achievement_id_var FROM public.achievement 
    WHERE person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван')
    AND text_content = 'Applicant article 3' LIMIT 1;
    IF achievement_id_var IS NOT NULL THEN
        INSERT INTO public.thesis_achievement (thesis_id, achievement_id, is_main, author_contribution)
        VALUES (thesis_id_var, achievement_id_var, false, 'Author contribution 3');
    END IF;
    
    SELECT id INTO achievement_id_var FROM public.achievement 
    WHERE person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван')
    AND text_content LIKE '%Программа для расчёта%' LIMIT 1;
    IF achievement_id_var IS NOT NULL THEN
        INSERT INTO public.thesis_achievement (thesis_id, achievement_id, is_main, author_contribution)
        VALUES (thesis_id_var, achievement_id_var, false, NULL);
    END IF;
END $$;
-- ==================================

INSERT INTO public.thesis_content_block (thesis_id, block_type, content, order_index)
VALUES 
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'task',
    'Task 1',
    1
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'task',
    'Task 2',
    2
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'task',
    'Task 3',
    3
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'task',
    'Task 4',
    4
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'task',
    'Task 5',
    5
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'novelty',
    'Novelty 1',
    1
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'novelty',
    'Novelty 2',
    2
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'novelty',
    'Novelty 3',
    3
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'novelty',
    'Novelty 4',
    4
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'value',
    'Value 1',
    1
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'value',
    'Value 2',
    2
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'value',
    'Value 3',
    3
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'provision',
    'Provision 1',
    1
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'provision',
    'Provision 2',
    2
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'provision',
    'Provision 3',
    3
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'provision',
    'Provision 4',
    4
),
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'provision',
    'Provision 5',
    5
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Котов К.К. Кошачье поведение в присутствии собак // Наши коты. 2025. Т. 1. С. 100--110.',
    2025
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Котов К.К. Собачье поведение в присутствии кошек // Наши собаки. 2024. Т. 10. С. 10--15.',
    2024
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Песов П.П. Кошки и собаки // Наши коты. 2023. Т. 5. С. 21--25.',
    2023
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Песов П.П. Собаки и кошки // Наши собаки. 2022. Т. 21. С. 1112.',
    2022
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Котов К.К., Песов П.П. Несколько слов про кошек и собак // Домашние любимцы. 2021. Т. 12. С. 01--13.',
    2021
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Мышов М.М. Собаки и мыши // Наши собаки. 2021. Т. 2. С. 11--12.',
    2021
);

INSERT INTO public.achievement (person_id, type, text_content, year)
VALUES (
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    1,
    'Собкин С.С., Мышов М.М. Мыши и собаки // Наши мыши. 2021. Т. 6. С. 91--112.',
    2021
);

-- ===== ИСПРАВЛЕННАЯ ВСТАВКА ДЛЯ ЛЬВОВА =====
INSERT INTO public.achievement (person_id, type, text_content, year)
SELECT p.id, 1, t.text_content, t.year
FROM (VALUES
    ('Львов', 'Львов Л.Л., Котов К.К. Кошачье поведение в присутствии собак // Наши коты. 2025. Т. 1. С. 100--110.', 2025),
    ('Львов', 'Львов Л.Л., Котов К.К. Собачье поведение в присутствии кошек // Наши собаки. 2024. Т. 10. С. 10--15.', 2024),
    ('Львов', 'Львов Л.Л., Песов П.П. Кошки и собаки // Наши коты. 2023. Т. 5. С. 21--25.', 2023),
    ('Львов', 'Львов Л.Л., Песов П.П. Собаки и кошки // Наши собаки. 2022. Т. 21. С. 1112.', 2022),
    ('Львов', 'Львов Л.Л., Котов К.К., Песов П.П. Несколько слов про кошек и собак // Домашние любимцы. 2021. Т. 12. С. 01--13.', 2021),
    ('Львов', 'Львов Л.Л., Мышов М.М. Собаки и мыши // Наши собаки. 2021. Т. 2. С. 11--12.', 2021),
    ('Львов', 'Львов Л.Л., Мышов М.М. Мыши и собаки // Наши мыши. 2021. Т. 6. С. 91--112.', 2021)
) AS t(last_name, text_content, year)
CROSS JOIN LATERAL (SELECT id FROM public.person WHERE last_name = t.last_name LIMIT 1) p;
-- =============================================

-- ===== ИСПРАВЛЕННАЯ ВСТАВКА ДЛЯ ТИГРОВА =====
INSERT INTO public.achievement (person_id, type, text_content, year)
SELECT p.id, 1, t.text_content, t.year
FROM (VALUES
    ('Тигров', 'Тигров Т.Т., Котов К.К. Кошачье поведение в присутствии собак // Наши коты. 2025. Т. 1. С. 100--110.', 2025),
    ('Тигров', 'Тигров Т.Т., Котов К.К. Собачье поведение в присутствии кошек // Наши собаки. 2024. Т. 10. С. 10--15.', 2024),
    ('Тигров', 'Тигров Т.Т., Песов П.П. Кошки и собаки // Наши коты. 2023. Т. 5. С. 21--25.', 2023),
    ('Тигров', 'Тигров Т.Т., Песов П.П. Собаки и кошки // Наши собаки. 2022. Т. 21. С. 1112.', 2022),
    ('Тигров', 'Тигров Т.Т., Котов К.К., Песов П.П. Несколько слов про кошек и собак // Домашние любимцы. 2021. Т. 12. С. 01--13.', 2021),
    ('Тигров', 'Тигров Т.Т., Мышов М.М. Собаки и мыши // Наши собаки. 2021. Т. 2. С. 11--12.', 2021)
) AS t(last_name, text_content, year)
CROSS JOIN LATERAL (SELECT id FROM public.person WHERE last_name = t.last_name LIMIT 1) p;
-- =============================================

-- ===== ИСПРАВЛЕННАЯ ВСТАВКА ДЛЯ ЯГУАРОВОЙ =====
INSERT INTO public.achievement (person_id, type, text_content, year)
SELECT p.id, 1, t.text_content, t.year
FROM (VALUES
    ('Ягуарова', 'Ягуарова Я.Я., Котов К.К. Кошачье поведение в присутствии собак // Наши коты. 2025. Т. 1. С. 100--110.', 2025),
    ('Ягуарова', 'Ягуарова Я.Я., Котов К.К. Собачье поведение в присутствии кошек // Наши собаки. 2025. Т. 10. С. 10--15.', 2025),
    ('Ягуарова', 'Ягуарова Я.Я., Песов П.П. Кошки и собаки // Наши коты. 2024. Т. 5. С. 21--25.', 2024),
    ('Ягуарова', 'Ягуарова Я.Я., Песов П.П. Собаки и кошки // Наши собаки. 2024. Т. 21. С. 1112.', 2024),
    ('Ягуарова', 'Ягуарова Я.Я., Котов К.К., Песов П.П. Несколько слов про кошек и собак // Домашние любимцы. 2024. Т. 12. С. 01--13.', 2024),
    ('Ягуарова', 'Ягуарова Я.Я., Мышов М.М. Собаки и мыши // Наши собаки. 2023. Т. 2. С. 11--12.', 2023),
    ('Ягуарова', 'Ягуарова Я.Я., Очень большие кошки // Разноразмерные кошки. 2023. Т. 1. С. 11--12.', 2023),
    ('Ягуарова', 'Ягуарова Я.Я., Просто большие кошки // Разноразмерные кошки. 2023. Т. 2. С. 13--14.', 2023),
    ('Ягуарова', 'Ягуарова Я.Я., Большие кошки // Разноразмерные кошки. 2022. Т. 3. С. 15--16.', 2022),
    ('Ягуарова', 'Ягуарова Я.Я., Большие кошки // Разноразмерные кошки. 2022. Т. 4. С. 15--16.', 2022),
    ('Ягуарова', 'Ягуарова Я.Я., Кошки больше обычных // Разноразмерные кошки. 2022. Т. 5. С. 17--18.', 2022),
    ('Ягуарова', 'Ягуарова Я.Я., Обычные кошки // Разноразмерные кошки. 2021. Т. 6. С. 19--20.', 2021),
    ('Ягуарова', 'Ягуарова Я.Я., Некрупные кошки // Разноразмерные кошки. 2021. Т. 7. С. 21--22.', 2021),
    ('Ягуарова', 'Ягуарова Я.Я., Небольшие кошки // Разноразмерные кошки. 2021. Т. 8. С. 23--24.', 2021),
    ('Ягуарова', 'Ягуарова Я.Я., Маленькие кошки // Разноразмерные кошки. 2021. Т. 9. С. 25--26.', 2021)
) AS t(last_name, text_content, year)
CROSS JOIN LATERAL (SELECT id FROM public.person WHERE last_name = t.last_name LIMIT 1) p;
-- =============================================

INSERT INTO public.ds_event (
    thesis_id, event_type, protocol_number, protocol_date, 
    votes_total, votes_yes, votes_no, votes_abstain,
    present_offline, present_online
)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'seminar',
    '1',
    '2026-10-01',
    10,
    10,
    0,
    0,
    10,
    0
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван'),
    'author',
    1
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Собакин'),
    'supervisor',
    1
);

INSERT INTO public.person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
VALUES 
('Кот', 'К.К.', NULL, 'д.к.н', 'профессор', NULL, NULL, NULL),
('Мурзиков', 'М.М.', NULL, 'д.к.н', 'доцент', NULL, NULL, NULL),
('Барсикова', 'Б.Б.', NULL, 'д.к.н', NULL, NULL, NULL, NULL),
('Кошаков', 'К.К.', NULL, 'д.к.н', 'профессор', NULL, NULL, NULL),
('Гуляева', 'Г.Г.', NULL, 'д.к.н', NULL, NULL, NULL, NULL);

INSERT INTO public.ds_event (
    thesis_id, 
    event_type, 
    protocol_number, 
    protocol_date, 
    votes_total, 
    votes_yes, 
    votes_no, 
    votes_abstain,
    present_offline, 
    present_online
)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'commission_creation',
    '1',
    '2026-01-01',
    15,
    15,
    0,
    0,
    10,
    5
);

INSERT INTO public.ds_event (
    thesis_id, 
    event_type, 
    protocol_number, 
    protocol_date, 
    votes_total, 
    votes_yes, 
    votes_no, 
    votes_abstain,
    present_offline, 
    present_online
)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'acceptance_for_defense',
    '1',
    '2026-01-03',
    15,
    15,
    0,
    0,
    11,
    4 
);

UPDATE public.thesis 
SET 
    website_publish_date = '2026-11-01',
    website_link = 'https://ds.mephi.ru/shared/dissertations',
    dissertation_text_link = 'https://ds.mephi.ru/shared/dissertations/...'
WHERE title LIKE '%Гидродинамика движения%';

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Кот'),
    'commission_chairman_18_1',
    1
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Мурзиков'),
    'commission_member_18_1',
    2
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Барсикова'),
    'commission_member_18_1',
    3
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Кошаков'),
    'commission_chairman_19_2',
    4
);

INSERT INTO public.thesis_participation (thesis_id, person_id, role, order_index)
VALUES (
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    (SELECT id FROM public.person WHERE last_name = 'Гуляева'),
    'commission_speaker_19_2',
    5
);

INSERT INTO public.thesis_content_block (thesis_id, block_type, content, order_index)
VALUES 
(
    (SELECT id FROM public.thesis WHERE title LIKE '%Гидродинамика движения%'),
    'publications_info',
    'Число публикаций соискателя: четырнадцати. Число основных статей, по которым проводится защита: трёх.',
    100
);

DO $$
DECLARE
    thesis_id_var bigint;
    achievement_rec RECORD;
BEGIN
    SELECT id INTO thesis_id_var FROM public.thesis WHERE title LIKE '%Гидродинамика движения%' LIMIT 1;
    
    FOR achievement_rec IN 
        SELECT a.id, a.text_content 
        FROM public.achievement a
        WHERE a.person_id = (SELECT id FROM public.person WHERE last_name = 'Иванов' AND first_name = 'Иван')
        AND a.type = 3
        AND NOT EXISTS (
            SELECT 1 FROM public.thesis_achievement ta 
            WHERE ta.achievement_id = a.id AND ta.thesis_id = thesis_id_var
        )
    LOOP
        INSERT INTO public.thesis_achievement (thesis_id, achievement_id, is_main, author_contribution)
        VALUES (thesis_id_var, achievement_rec.id, false, NULL);
    END LOOP;
END $$;

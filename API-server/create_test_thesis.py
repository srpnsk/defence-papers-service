import requests
import json

url = "http://localhost:8087/api/thesis/form-data"

data = {
    # ---------- Диссовет (используем существующий) ----------
    "DS_number": "1.01",
    "DS_chairman_name_I": "Иванов И.И.",
    "DS_chairman_name_D": "Иванову И.И.",
    "DS_chairman_degree": "д.т.н.",
    "DS_secretary_name": "Петров П.П.",
    "DS_secretary_degree": "к.т.н.",

    # ---------- Соискатель ----------
    "applicant_full_name_I": "Сидорова Анна Михайловна",
    "applicant_short_name_I": "Сидорова А.М.",
    "applicant_full_name_R": "Сидоровой Анны Михайловны",
    "applicant_short_name_R": "Сидоровой А.М.",
    "end_of_postgrad_date": "15 июня 2025",
    "applicant_phone_number": "+7 916 555-12-34",
    "applicant_email": "sidorova@example.com",
    "applicant_full_adress": "г. Москва, ул. Тестовая, д. 10, кв. 5",
    "applicant_SNILS": "123-456-789 01",
    "applicant_document": "паспорт",
    "applicant_document_series": "1234",
    "applicant_document_number": "567890",

    # ---------- Диссертация ----------
    "degree_R": "кандидата физико-математических наук",
    "thesis_title": "Моделирование и анализ тестовых структур в условиях полной загрузки",
    "applicant_specialty_number": "6.6.6",
    "applicant_specialty_title": "Физика котиков",
    "defence_date": "01 сентября 2026",
    "defence_time": "14:30",

    # ---------- Научный руководитель ----------
    "advisor_name_full": "Сергеев Сергей Сергеевич",
    "advisor_name_short": "Сергеев С.С.",
    "advisor_degree": "д.ф.-м.н.",
    "advisor_title": "профессор",
    "advisor_degree_title": "д.ф.-м.н., профессор",
    # для руководителя используем specialty_number = "6.6.5" (существует)
    "advisor_specialty_number": "6.6.5",
    "advisor_specialty_title": "Физика больших котиков",
    "advisor_main_job": "заведующий кафедрой",
    "advisor_main_workplace_full": "Московский Физико-Технический Институт",
    "advisor_main_workplace_division": "Кафедра теоретической физики",
    "advisor_main_workplace_adress": "141701, г. Долгопрудный, Институтский пер., 9",
    "advisor_email": "sergeev@mfti.ru",
    "advisor_phone_number": "+7 495 408-55-00",

    # ---------- Оппонент 1 ----------
    "opponent1_name_short": "Козлов К.К.",
    "opponent1_name_full_I": "Козлов Кирилл Константинович",
    "opponent1_degree": "д.т.н.",
    "opponent1_title": "доцент",
    "opponent1_degree_title": "д.т.н., доцент",
    "opponent1_specialty_number": "6.6.7",
    "opponent1_specialty_title": "Физика малых котиков",
    "opponent1_main_job": "ведущий научный сотрудник",
    "opponent1_main_workplace_full": "Институт Прикладной Физики РАН",
    "opponent1_main_workplace_division": "Лаборатория физики твердого тела",
    "opponent1_main_workplace_adress": "603950, г. Нижний Новгород, ул. Ульянова, 46",
    "opponent1_email": "kozlov@ipfran.ru",
    "opponent1_phone_number": "+7 831 416-55-33",

    # ---------- Оппонент 2 ----------
    "opponent2_name_short": "Морозов М.М.",
    "opponent2_name_full_I": "Морозов Михаил Михайлович",
    "opponent2_degree": "к.ф.-м.н.",
    "opponent2_title": "",
    "opponent2_degree_title": "к.ф.-м.н.",
    "opponent2_specialty_number": "6.6.6",
    "opponent2_specialty_title": "Физика котиков",
    "opponent2_main_job": "старший научный сотрудник",
    "opponent2_main_workplace_full": "Институт Теоретической и Экспериментальной Физики",
    "opponent2_main_workplace_division": "Отдел физики высоких энергий",
    "opponent2_main_workplace_adress": "117218, г. Москва, ул. Б. Черемушкинская, 25",
    "opponent2_email": "morozov@itep.ru",
    "opponent2_phone_number": "+7 499 125-25-25",

    # ---------- Оппонент 3 ----------
    "opponent3_name_short": "Федорова Ф.Ф.",
    "opponent3_name_full_I": "Федорова Фаина Федоровна",
    "opponent3_degree": "д.х.н.",
    "opponent3_title": "профессор",
    "opponent3_degree_title": "д.х.н., профессор",
    "opponent3_specialty_number": "14.14.14",
    "opponent3_specialty_title": "Физика кошачьих конечностей",
    "opponent3_main_job": "главный научный сотрудник",
    "opponent3_main_workplace_full": "Институт Органической Химии им. Н.Д. Зелинского РАН",
    "opponent3_main_workplace_division": "Лаборатория гетероциклических соединений",
    "opponent3_main_workplace_adress": "119991, г. Москва, Ленинский пр-т, 47",
    "opponent3_email": "fedorova@ioc.ac.ru",
    "opponent3_phone_number": "+7 499 137-29-44",

    # ---------- 2. Заключение организации ----------
    "applicant_department_number": "42",
    "applicant_department_title": "Кафедра компьютерного моделирования",
    "applicant_PG_study": "очной аспирантуре МФТИ",
    "applicant_job_organisation": "МФТИ",
    "applicant_main_job": "ассистент",
    "applicant_job_department_number": "42",
    "applicant_job_department_title": "Кафедра компьютерного моделирования",
    "applicant_addition_job": "инженер-программист",
    "applicant_addition_job_place": "ООО «ТехноСофт»",
    "applicant_HE_type": "магистратура МФТИ",
    "applicant_HE_qualification": "магистр",
    "applicant_excellency": "с отличием",
    "applicant_HE_end_year": 2023,
    "applicant_HE_direction_number": "14.14.14",
    "applicant_HE_direction_title": "Физика кошачьих конечностей",
    "applicant_PG_end_year": 2026,
    "applicant_PG_direction_number": "13.13.13",
    "applicant_PG_direction_title": "Физика кошачьих хвостов",
    "applicant_PG_speciality_number": "6.6.6",
    "applicant_PG_speciality_title": "Физика котиков",
    "applicant_speciality_type": "физико-математические",
    "applicant_PG_reference_date": "15 июня 2026",
    "seminar_departament_number": "42",
    "seminar_departament_title": "Кафедра компьютерного моделирования",
    "seminar_faculty": "института прикладной математики",
    "seminar_protocol_number": "3",
    "seminar_date": "10 октября 2025",
    "achievement": "разработку методов моделирования и численного анализа",
    "departament_head_degree": "д.ф.-м.н.",
    "departament_head_name": "Смирнов А.Б.",
    "faculty_head_degree": "д.т.н.",
    "faculty_head_name": "Кузнецов В.Г.",

    # ---------- Паспорт специальности ----------
    "applicant_speciality_pasport_item_text_1": "Математическое моделирование физических процессов",
    "applicant_speciality_pasport_item_text_2": "Численные методы решения дифференциальных уравнений",
    "applicant_speciality_pasport_item_text_3": "Программные комплексы для научных исследований",

    # ---------- Задачи ----------
    "thesis_tasks_1": "Разработать математическую модель",
    "thesis_tasks_2": "Реализовать численный алгоритм",
    "thesis_tasks_3": "Провести верификацию модели",
    "thesis_tasks_4": "Исследовать влияние параметров",
    "thesis_tasks_5": "Создать программный прототип",
    "thesis_tasks_6": "",
    "thesis_tasks_7": "",
    "thesis_tasks_8": "",

    # ---------- Личное участие ----------
    "thesis_participation": "Автором лично разработаны все модели, алгоритмы и проведены расчеты.",

    # ---------- Научная новизна ----------
    "thesis_novelty_1": "Впервые предложена гибридная модель взаимодействия.",
    "thesis_novelty_2": "Разработан эффективный численный метод.",
    "thesis_novelty_3": "Получены новые закономерности поведения системы.",
    "thesis_novelty_4": "",
    "thesis_novelty_5": "",
    "thesis_novelty_6": "",

    # ---------- Практическая ценность ----------
    "thesis_value_1": "Модель может быть использована в инженерных расчетах.",
    "thesis_value_2": "Созданный программный комплекс передан для опытной эксплуатации.",
    "thesis_value_3": "Результаты внедрены в учебный процесс.",
    "thesis_value_4": "",
    "thesis_value_5": "",
    "thesis_value_6": "",

    # ---------- Положения, выносимые на защиту ----------
    "thesis_provision_1": "Математическая модель адекватно описывает процесс.",
    "thesis_provision_2": "Разработанный алгоритм обладает высокой точностью.",
    "thesis_provision_3": "Полученные результаты согласуются с экспериментом.",
    "thesis_provision_4": "",
    "thesis_provision_5": "",
    "thesis_provision_6": "",

    # ---------- Оценка достоверности ----------
    "thesis_reliability": "Достоверность подтверждена сравнением с аналитическими решениями и экспериментальными данными.",

    # ---------- Статьи соискателя ----------
    "applicant_article_1": "Сидорова А.М., Сергеев С.С. Новая модель тестовых структур // Журнал вычислительной физики. 2026. Т.15. №2. С.100-110.",
    "applicant_article_BD_1": "Scopus Q1",
    "applicant_article_contribution_1": "Сидорова А.М. разработала модель и провела расчеты.",
    "applicant_article_2": "Сидорова А.М. Численный анализ тестовых систем // Математическое моделирование. 2025. Т.20. №5. С.200-210.",
    "applicant_article_BD_2": "ВАК К1",
    "applicant_article_contribution_2": "Личный вклад – реализация алгоритма.",
    "applicant_article_3": "Сидорова А.М., Сергеев С.С. Программный комплекс для моделирования // Вестник МФТИ. 2024. Т.7. №3. С.55-62.",
    "applicant_article_BD_3": "РИНЦ",
    "applicant_article_contribution_3": "Сидорова А.М. подготовила код и провела тестирование.",

    # ---------- Конференции соискателя ----------
    "applicant_conference_1": "Международная конференция по вычислительной физике, г. Москва. 2026",
    "applicant_conference_2": "Научная сессия МФТИ, г. Долгопрудный. 2025",

    # ---------- Тезисы конференций ----------
    "applicant_thesis_1": "Сидорова А.М., Сергеев С.С. Моделирование тестовых систем // Тез. докл. междунар. конф. Москва, 2026. С. 45.",
    "applicant_thesis_2": "Сидорова А.М. Численный метод для тестовых задач // Сб. трудов 63-й научной сессии МФТИ. 2025. С. 112.",

    # ---------- РИД ----------
    "applicant_RID_1": "Сидорова А.М., Сергеев С.С. Программа для моделирования тестовых структур. Свидетельство о гос. регистрации программы для ЭВМ № 2026123456 от 01.02.2026.",

    # ---------- 3. Поянительная записка ----------
    "planed_defence_date": "сентябрь 2026",

    # ---------- 9. Сведения о научном руководителе ----------
    "advisor_article_1": "Сергеев С.С. Тестовые структуры в современной физике // Успехи физических наук. 2025. Т.195. №4. С.350-360.",
    "advisor_article_2": "Сергеев С.С., Иванов А.А. Методы анализа тестовых систем // ЖЭТФ. 2024. Т.125. №2. С.250-260.",
    "advisor_article_3": "Сергеев С.С. Вычислительные аспекты тестовых задач // Математическое моделирование. 2023. Т.18. №1. С.80-90.",

    # ---------- 11_1. Согласие и данные оппонента 1 ----------
    "opponent1_article_1": "Козлов К.К. Физика тестовых систем // Физика твердого тела. 2025. Т.67. №8. С.1200-1210.",
    "opponent1_article_2": "Козлов К.К., Петров Б.Б. Экспериментальное исследование тестовых структур // Письма в ЖЭТФ. 2024. Т.89. №5. С.300-310.",
    "opponent1_article_3": "Козлов К.К. Моделирование процессов в тестовых средах // Изв. РАН. Серия физическая. 2023. Т.77. №9. С.1100-1110.",

    # ---------- 11_2. Согласие и данные оппонента 2 ----------
    "opponent2_article_1": "Морозов М.М. Тестовые задачи в физике высоких энергий // Ядерная физика. 2025. Т.78. №3. С.400-410.",
    "opponent2_article_2": "Морозов М.М., Алексеев А.А. Компьютерное моделирование тестовых процессов // Вычислительная физика. 2024. Т.12. №4. С.500-510.",

    # ---------- 11_3. Согласие и данные оппонента 3 ----------
    "opponent3_article_1": "Федорова Ф.Ф. Химические аспекты тестовых материалов // Журнал органической химии. 2025. Т.61. №1. С.50-60.",
    "opponent3_article_2": "Федорова Ф.Ф., Иванов И.И. Синтез и свойства тестовых соединений // Химическая физика. 2024. Т.43. №7. С.70-80.",
    "opponent3_article_3": "Федорова Ф.Ф. Применение тестовых методов в органическом синтезе // Изв. АН. Сер. хим. 2023. №5. С.1000-1010.",

    # ---------- 18_1. Протокол о создании комиссии ----------
    "18_1_protocol_number": "5",
    "18_1_protocol_date": "10 апреля 2026",
    "18_1_commission_chairman_name": "Николаев Н.Н.",
    "18_1_commission_chairman_degree_title": "д.ф.-м.н., профессор",
    "18_1_commission_member1_name": "Алексеев А.А.",
    "18_1_commission_member1_degree_title": "к.ф.-м.н.",
    "18_1_commission_member2_name": "Борисов Б.Б.",
    "18_1_commission_member2_degree_title": "д.т.н., доцент",
    "18_1_vote_results": 18,

    # ---------- 19_2. Протокол совета о приёме к защите ----------
    "19_2_protocol_number": "7",
    "19_2_protocol_date": "15 мая 2026",
    "19_2_commission_chairman_name": "Григорьев Г.Г.",
    "19_2_commission_chairman_degree_title": "д.т.н., профессор",
    "19_2_commission_speaker_name_R": "Дмитриев Д.Д.",
    "19_2_commission_speaker_degree": "к.ф.-м.н.",
    "19_2_vote_results": 18,

    # ---------- 20. Заключение комиссии ДС ----------
    "applicant_artciles_number_total_W": "пятнадцати",
    "applicant_artciles_number_rewiewed_W": "трёх",

    # ---------- 21. Скриншот опубликования на сайте МИФИ ----------
    "data_publishing_MEPhI": "01 ноября 2026 г.",
    "link_screenshot_publishing_MEPhI": "https://ds.mephi.ru/dissertations/2026/sidorova",
    "link_text_publishing_MEPhI": "https://ds.mephi.ru/dissertations/2026/sidorova/thesis.pdf"
}

# Добавляем недостающие пустые поля, чтобы модель приняла
for i in range(4, 17):
    data[f"applicant_article_{i}"] = ""
    data[f"applicant_article_BD_{i}"] = ""
    data[f"applicant_article_contribution_{i}"] = ""

for i in range(3, 31):
    data[f"applicant_conference_{i}"] = ""
    data[f"applicant_thesis_{i}"] = ""

for i in range(2, 6):
    data[f"applicant_RID_{i}"] = ""

for i in range(4, 16):
    data[f"advisor_article_{i}"] = ""

for i in range(4, 16):
    data[f"opponent1_article_{i}"] = ""

for i in range(3, 16):
    data[f"opponent2_article_{i}"] = ""

for i in range(4, 16):
    data[f"opponent3_article_{i}"] = ""

response = requests.post(url, json=data)
print("Status:", response.status_code)
try:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
except:
    print(response.text)
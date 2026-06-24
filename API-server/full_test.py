import requests
import random
import string
import json

API = "http://localhost:8087"

# Генерируем уникального пользователя
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

email = f"test_{random_string()}@example.com"
password = "123456"
last_name = "Тестов"
first_name = "Тест"
second_name = "Тестович"

session = requests.Session()

# 1. Регистрация
resp = session.post(f"{API}/auth/register", json={
    "last_name": last_name,
    "first_name": first_name,
    "second_name": second_name,
    "email": email,
    "password": password,
    "degree": None,
    "academic_title": None,
    "phone_number": None,
    "specialty_id": None
})
print("Register:", resp.status_code, resp.text)

if resp.status_code != 200:
    # Возможно пользователь уже существует, пробуем войти
    resp = session.post(f"{API}/auth/login", json={
        "email": email,
        "password": password
    })
    print("Login after fail:", resp.status_code, resp.text)

# 2. Заполняем все поля диссертации
data = {
    "DS_number": "1.01",
    "DS_chairman_name_I": "Иванов И.И.",
    "DS_chairman_name_D": "Иванову И.И.",
    "DS_chairman_degree": "д.т.н.",
    "DS_secretary_name": "Петров П.П.",
    "DS_secretary_degree": "к.т.н.",
    "applicant_full_name_I": f"{last_name} {first_name} {second_name}",
    "applicant_short_name_I": f"{last_name} {first_name[0]}.{second_name[0]}.",
    "applicant_full_name_R": f"{last_name}а {first_name}а {second_name}а",
    "applicant_short_name_R": f"{last_name}а {first_name[0]}.{second_name[0]}.",
    "end_of_postgrad_date": "15 июня 2025",
    "applicant_phone_number": "+7 999 123-45-67",
    "applicant_email": email,
    "applicant_full_adress": "г. Москва, ул. Тестовая, д. 1, кв. 1",
    "applicant_SNILS": "123-456-789 01",
    "applicant_document": "паспорт",
    "applicant_document_series": "1234",
    "applicant_document_number": "567890",
    "degree_R": "кандидата физико-математических наук",
    "thesis_title": "Исследование тестовых данных в условиях полной автоматизации",
    "applicant_specialty_number": "6.6.6",
    "applicant_specialty_title": "Физика котиков",
    "defence_date": "01 сентября 2026",
    "defence_time": "14:00",
    "advisor_name_full": "Сергеев Сергей Сергеевич",
    "advisor_name_short": "Сергеев С.С.",
    "advisor_degree": "д.ф.-м.н.",
    "advisor_title": "профессор",
    "advisor_degree_title": "д.ф.-м.н., профессор",
    "advisor_specialty_number": "6.6.5",
    "advisor_specialty_title": "Физика больших котиков",
    "advisor_main_job": "заведующий лабораторией",
    "advisor_main_workplace_full": "НИИ Технологий",
    "advisor_main_workplace_division": "Лаборатория тестовых исследований",
    "advisor_main_workplace_adress": "123456, г. Наукоград, пр. Тестовый, 42",
    "advisor_email": "sergeev@niit.ru",
    "advisor_phone_number": "+7 999 000-11-22",
    "opponent1_name_short": "Оппонентов О.О.",
    "opponent1_name_full_I": "Оппонентов Оппо О.О.",
    "opponent1_degree": "д.т.н.",
    "opponent1_title": "доцент",
    "opponent1_degree_title": "д.т.н., доцент",
    "opponent1_specialty_number": "6.6.7",
    "opponent1_specialty_title": "Физика малых котиков",
    "opponent1_main_job": "ведущий научный сотрудник",
    "opponent1_main_workplace_full": "Институт Прикладных Тестов",
    "opponent1_main_workplace_division": "Отдел верификации",
    "opponent1_main_workplace_adress": "654321, г. Тестовск, ул. Экспериментальная, 7",
    "opponent1_email": "opp1@ipt.ru",
    "opponent1_phone_number": "+7 999 333-44-55",
    "opponent2_name_short": "Рецензентов Р.Р.",
    "opponent2_name_full_I": "Рецензентов Рецензент Р.Р.",
    "opponent2_degree": "к.ф.-м.н.",
    "opponent2_title": "",
    "opponent2_degree_title": "к.ф.-м.н.",
    "opponent2_specialty_number": "6.6.6",
    "opponent2_specialty_title": "Физика котиков",
    "opponent2_main_job": "старший научный сотрудник",
    "opponent2_main_workplace_full": "НИИ Точных Измерений",
    "opponent2_main_workplace_division": "Лаборатория тестов",
    "opponent2_main_workplace_adress": "111222, г. Измеринск, ул. Шкалова, 13",
    "opponent2_email": "opp2@nii-ti.ru",
    "opponent2_phone_number": "+7 999 666-77-88",
    "opponent3_name_short": "Экспертов Э.Э.",
    "opponent3_name_full_I": "Экспертов Эксперт Э.Э.",
    "opponent3_degree": "д.э.н.",
    "opponent3_title": "профессор",
    "opponent3_degree_title": "д.э.н., профессор",
    "opponent3_specialty_number": "14.14.14",
    "opponent3_specialty_title": "Физика кошачьих конечностей",
    "opponent3_main_job": "главный научный сотрудник",
    "opponent3_main_workplace_full": "Академия Тестологии",
    "opponent3_main_workplace_division": "Кафедра тестовых наук",
    "opponent3_main_workplace_adress": "999888, г. Тест-Сити, ул. Академическая, 1",
    "opponent3_email": "opp3@academtest.ru",
    "opponent3_phone_number": "+7 999 999-00-11",
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
    "applicant_HE_end_year": 2024,
    "applicant_HE_direction_number": "14.14.14",
    "applicant_HE_direction_title": "Физика кошачьих конечностей",
    "applicant_PG_end_year": 2027,
    "applicant_PG_direction_number": "13.13.13",
    "applicant_PG_direction_title": "Физика кошачьих хвостов",
    "applicant_PG_speciality_number": "6.6.6",
    "applicant_PG_speciality_title": "Физика котиков",
    "applicant_speciality_type": "физико-математические",
    "applicant_PG_reference_date": "15 июня 2027",
    "seminar_departament_number": "42",
    "seminar_departament_title": "Кафедра компьютерного моделирования",
    "seminar_faculty": "института прикладной математики",
    "seminar_protocol_number": "3",
    "seminar_date": "10 октября 2025",
    "achievement": "разработку методов автоматической проверки тестовых форм",
    "departament_head_degree": "д.ф.-м.н.",
    "departament_head_name": "Смирнов А.Б.",
    "faculty_head_degree": "д.т.н.",
    "faculty_head_name": "Кузнецов В.Г.",
    "applicant_speciality_pasport_item_text_1": "Математическое моделирование физических процессов",
    "applicant_speciality_pasport_item_text_2": "Численные методы решения дифференциальных уравнений",
    "applicant_speciality_pasport_item_text_3": "Программные комплексы для научных исследований",
    "thesis_tasks_1": "Разработать математическую модель",
    "thesis_tasks_2": "Реализовать численный алгоритм",
    "thesis_tasks_3": "Провести верификацию модели",
    "thesis_tasks_4": "Исследовать влияние параметров",
    "thesis_tasks_5": "Создать программный прототип",
    "thesis_tasks_6": "",
    "thesis_tasks_7": "",
    "thesis_tasks_8": "",
    "thesis_participation": "Автором лично разработаны все модели и алгоритмы.",
    "thesis_novelty_1": "Впервые предложена гибридная модель взаимодействия.",
    "thesis_novelty_2": "Разработан эффективный численный метод.",
    "thesis_novelty_3": "Получены новые закономерности поведения системы.",
    "thesis_novelty_4": "",
    "thesis_novelty_5": "",
    "thesis_novelty_6": "",
    "thesis_value_1": "Модель может быть использована в инженерных расчетах.",
    "thesis_value_2": "Созданный программный комплекс передан для опытной эксплуатации.",
    "thesis_value_3": "Результаты внедрены в учебный процесс.",
    "thesis_value_4": "",
    "thesis_value_5": "",
    "thesis_value_6": "",
    "thesis_provision_1": "Математическая модель адекватно описывает процесс.",
    "thesis_provision_2": "Разработанный алгоритм обладает высокой точностью.",
    "thesis_provision_3": "Полученные результаты согласуются с экспериментом.",
    "thesis_provision_4": "",
    "thesis_provision_5": "",
    "thesis_provision_6": "",
    "thesis_reliability": "Достоверность подтверждена сравнением с аналитическими решениями.",
    "applicant_article_1": "Сидорова А.М., Сергеев С.С. Новая модель тестовых структур // Журнал вычислительной физики. 2026. Т.15. №2. С.100-110.",
    "applicant_article_BD_1": "Scopus Q1",
    "applicant_article_contribution_1": "Сидорова А.М. разработала модель и провела расчеты.",
    "applicant_article_2": "Сидорова А.М. Численный анализ тестовых систем // Математическое моделирование. 2025. Т.20. №5. С.200-210.",
    "applicant_article_BD_2": "ВАК К1",
    "applicant_article_contribution_2": "Личный вклад – реализация алгоритма.",
    "applicant_article_3": "Сидорова А.М., Сергеев С.С. Программный комплекс для моделирования // Вестник МФТИ. 2024. Т.7. №3. С.55-62.",
    "applicant_article_BD_3": "РИНЦ",
    "applicant_article_contribution_3": "Сидорова А.М. подготовила код и провела тестирование.",
    "applicant_conference_1": "Международная конференция по вычислительной физике, г. Москва. 2026",
    "applicant_conference_2": "Научная сессия МФТИ, г. Долгопрудный. 2025",
    "applicant_thesis_1": "Сидорова А.М., Сергеев С.С. Моделирование тестовых систем // Тез. докл. междунар. конф. Москва, 2026. С. 45.",
    "applicant_thesis_2": "Сидорова А.М. Численный метод для тестовых задач // Сб. трудов 63-й научной сессии МФТИ. 2025. С. 112.",
    "applicant_RID_1": "Сидорова А.М., Сергеев С.С. Программа для моделирования тестовых структур. Свидетельство о гос. регистрации программы для ЭВМ № 2026123456 от 01.02.2026.",
    "planed_defence_date": "сентябрь 2026",
    "advisor_article_1": "Сергеев С.С. Тестовые структуры в современной физике // Успехи физических наук. 2025. Т.195. №4. С.350-360.",
    "advisor_article_2": "Сергеев С.С., Иванов А.А. Методы анализа тестовых систем // ЖЭТФ. 2024. Т.125. №2. С.250-260.",
    "advisor_article_3": "Сергеев С.С. Вычислительные аспекты тестовых задач // Математическое моделирование. 2023. Т.18. №1. С.80-90.",
    "opponent1_article_1": "Оппонентов О.О. Физика тестовых систем // Физика твердого тела. 2025. Т.67. №8. С.1200-1210.",
    "opponent1_article_2": "Оппонентов О.О., Петров Б.Б. Экспериментальное исследование тестовых структур // Письма в ЖЭТФ. 2024. Т.89. №5. С.300-310.",
    "opponent1_article_3": "Оппонентов О.О. Моделирование процессов в тестовых средах // Изв. РАН. Серия физическая. 2023. Т.77. №9. С.1100-1110.",
    "opponent2_article_1": "Рецензентов Р.Р. Тестовые задачи в физике высоких энергий // Ядерная физика. 2025. Т.78. №3. С.400-410.",
    "opponent2_article_2": "Рецензентов Р.Р., Алексеев А.А. Компьютерное моделирование тестовых процессов // Вычислительная физика. 2024. Т.12. №4. С.500-510.",
    "opponent3_article_1": "Экспертов Э.Э. Химические аспекты тестовых материалов // Журнал органической химии. 2025. Т.61. №1. С.50-60.",
    "opponent3_article_2": "Экспертов Э.Э., Иванов И.И. Синтез и свойства тестовых соединений // Химическая физика. 2024. Т.43. №7. С.70-80.",
    "opponent3_article_3": "Экспертов Э.Э. Применение тестовых методов в органическом синтезе // Изв. АН. Сер. хим. 2023. №5. С.1000-1010.",
    "18_1_protocol_number": "5",
    "18_1_protocol_date": "10 апреля 2026",
    "18_1_commission_chairman_name": "Николаев Н.Н.",
    "18_1_commission_chairman_degree_title": "д.ф.-м.н., профессор",
    "18_1_commission_member1_name": "Алексеев А.А.",
    "18_1_commission_member1_degree_title": "к.ф.-м.н.",
    "18_1_commission_member2_name": "Борисов Б.Б.",
    "18_1_commission_member2_degree_title": "д.т.н., доцент",
    "18_1_vote_results": 18,
    "19_2_protocol_number": "7",
    "19_2_protocol_date": "15 мая 2026",
    "19_2_commission_chairman_name": "Григорьев Г.Г.",
    "19_2_commission_chairman_degree_title": "д.т.н., профессор",
    "19_2_commission_speaker_name_R": "Дмитриев Д.Д.",
    "19_2_commission_speaker_degree": "к.ф.-м.н.",
    "19_2_vote_results": 18,
    "applicant_artciles_number_total_W": "пятнадцати",
    "applicant_artciles_number_rewiewed_W": "трёх",
    "data_publishing_MEPhI": "01 ноября 2026 г.",
    "link_screenshot_publishing_MEPhI": "https://ds.mephi.ru/dissertations/2026/sidorova",
    "link_text_publishing_MEPhI": "https://ds.mephi.ru/dissertations/2026/sidorova/thesis.pdf"
}

# Заполняем оставшиеся поля (статьи 4-16, конференции 3-30, тезисы 3-30, РИД 2-5, статьи руководителя 4-15, оппонентов)
for i in range(4, 17):
    data[f"applicant_article_{i}"] = ""
    data[f"applicant_article_BD_{i}"] = ""
    data[f"applicant_article_contribution_{i}"] = ""

for i in range(3, 31):
    data[f"applicant_conference_{i}"] = ""

for i in range(3, 31):
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

# Отправляем
resp = session.post(f"{API}/api/thesis/form-data", json=data)
print("Create thesis:", resp.status_code)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

print(f"\nГотово! Войдите на фронтенд с email={email} пароль={password}")
print("Диссертация появится в личном кабинете.")
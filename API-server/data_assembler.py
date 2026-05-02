# data_assembler.py
from database import database

async def assemble_thesis_json(thesis_id: int) -> dict:
    # 1. Основная информация о диссертации и совете
    thesis_query = """
        SELECT 
            t.title AS thesis_title,
            t.target_degree AS degree_R,
            t.planned_defence_date,
            t.council_id,
            t.applicant_id,
            t.specialty_id,
            dc.number AS DS_number,
            dc.chairman_id,
            dc.secretary_id
        FROM thesis t
        JOIN dissertation_council dc ON t.council_id = dc.id
        WHERE t.id = :id
    """
    thesis_row = await database.fetch_one(thesis_query, {"id": thesis_id})
    if not thesis_row:
        return {}
    thesis = dict(thesis_row)  # преобразуем в обычный словарь для безопасного доступа

    result = {
        "thesis_title": thesis.get("thesis_title") or "",
        "degree_R": thesis.get("degree_R") or "",
        "planned_defence_date": str(thesis.get("planned_defence_date") or ""),
        "DS_number": thesis.get("DS_number") or "",
    }

    # 2. Соискатель
    applicant_row = await database.fetch_one(
        "SELECT last_name, first_name, second_name, email, phone_number FROM person WHERE id = :id",
        {"id": thesis["applicant_id"]}
    )
    if applicant_row:
        app = dict(applicant_row)
        full_name = f"{app.get('last_name', '')} {app.get('first_name', '')}"
        if app.get('second_name'):
            full_name += f" {app['second_name']}"
        result["applicant_full_name_I"] = full_name.strip()
        result["applicant_email"] = app.get("email") or ""
        result["applicant_phone_number"] = app.get("phone_number") or ""

    # 3. Председатель совета
    chairman_row = await database.fetch_one(
        "SELECT degree FROM person WHERE id = :id",
        {"id": thesis["chairman_id"]}
    )
    if chairman_row:
        result["DS_chairman_degree"] = chairman_row["degree"] or ""

    # 4. Секретарь совета
    secretary_row = await database.fetch_one(
        "SELECT degree FROM person WHERE id = :id",
        {"id": thesis["secretary_id"]}
    )
    if secretary_row:
        result["DS_secretary_degree"] = secretary_row["degree"] or ""

    # 5. Научный руководитель
    supervisor_row = await database.fetch_one(
        """
        SELECT p.last_name, p.first_name, p.second_name, p.degree, p.academic_title 
        FROM thesis_participation tp
        JOIN person p ON tp.person_id = p.id
        WHERE tp.thesis_id = :tid AND tp.role = 'supervisor'
        """,
        {"tid": thesis_id}
    )
    if supervisor_row:
        sup = dict(supervisor_row)
        full = f"{sup.get('last_name', '')} {sup.get('first_name', '')}"
        if sup.get('second_name'):
            full += f" {sup['second_name']}"
        result["advisor_name_full"] = full.strip()
        result["advisor_degree"] = sup.get("degree") or ""
        result["advisor_title"] = sup.get("academic_title") or ""

    # Здесь можно добавить аналогичную сборку оппонентов, статей и т.д.

    return result
# form_handler.py
import json
from datetime import date, datetime

from fastapi import HTTPException
from database import database
from models import (
    PersonCreate, PersonUpdate,
    EmploymentCreate,
    EducationCreate,
    AchievementCreate,
    ThesisUpdate,
    CouncilUpdate,
    ApplicantDetailsUpdate,
    ApplicantDetailsCreate,
    OpponentCreate,
    ParticipationCreate,
)
from routers.persons import create_person, update_person
from routers.employments import create_employment
from routers.educations import create_education
from routers.achievements import create_achievement
from routers.theses import (
    update_thesis, add_opponent, add_participation
)
from routers.councils import update_council
from routers.applicant_details import update_details, create_details
from utils import parse_full_name, parse_russian_date, extract_year


async def _upsert_content_block(thesis_id: int, block_type: str, content: str, order_index: int):
    if content:
        await database.execute(
            "INSERT INTO thesis_content_block (thesis_id, block_type, content, order_index) "
            "VALUES (:tid, :type, :content, :idx) ON CONFLICT DO NOTHING",
            {"tid": thesis_id, "type": block_type, "content": content, "idx": order_index}
        )


async def process_opponent(thesis_id: int, ctx: dict, form_data: dict, idx: int):
    prefix = f"opponent{idx}"
    name_full = form_data.get(f"{prefix}_name_full_I", "")
    if not name_full:
        return

    opponent_id = ctx.get(f"opponent_{idx}_id")
    name_parts = parse_full_name(name_full)

    specialty_code = form_data.get(f"{prefix}_specialty_number")
    specialty_id = None
    if specialty_code:
        existing = await database.fetch_one(
            "SELECT id FROM specialty WHERE code = :code", {"code": specialty_code}
        )
        if existing:
            specialty_id = existing["id"]

    person_data = {
        "last_name": name_parts.get("last_name"),
        "first_name": name_parts.get("first_name"),
        "second_name": name_parts.get("second_name"),
        "degree": form_data.get(f"{prefix}_degree"),
        "academic_title": form_data.get(f"{prefix}_title"),
        "email": form_data.get(f"{prefix}_email"),
        "phone_number": form_data.get(f"{prefix}_phone_number"),
        "specialty_id": specialty_id,
    }

    if opponent_id:
        await update_person(opponent_id, PersonUpdate(**person_data))
    else:
        new_person = await create_person(PersonCreate(**person_data))
        opponent_id = new_person["id"]
        await add_opponent(thesis_id, OpponentCreate(
            thesis_id=thesis_id, person_id=opponent_id, order_index=idx
        ))

    org_name = form_data.get(f"{prefix}_main_workplace_full", "")
    if org_name:
        org = await database.fetch_one(
            "SELECT id FROM organization WHERE full_name = :name", {"name": org_name}
        )
        org_id = org["id"] if org else None
        if not org_id:
            org_id = await database.execute(
                "INSERT INTO organization (full_name, short_name, address) "
                "VALUES (:full_name, :short_name, :address) RETURNING id",
                {"full_name": org_name, "short_name": org_name[:64],
                 "address": form_data.get(f"{prefix}_main_workplace_adress", "—")}
            )
        existing_emp = await database.fetch_one(
            "SELECT id FROM employment_history WHERE person_id = :pid AND is_additional = false",
            {"pid": opponent_id}
        )
        if existing_emp:
            await database.execute(
                "UPDATE employment_history SET organization_id = :oid, position = :pos, division = :div "
                "WHERE id = :eid",
                {"oid": org_id, "pos": form_data.get(f"{prefix}_main_job"),
                 "div": form_data.get(f"{prefix}_main_workplace_division"), "eid": existing_emp["id"]}
            )
        else:
            await create_employment(EmploymentCreate(
                person_id=opponent_id,
                organization_id=org_id,
                position=form_data.get(f"{prefix}_main_job"),
                division=form_data.get(f"{prefix}_main_workplace_division"),
                start_date=date(2000, 1, 1),
                is_additional=False
            ))

    for i in range(1, 16):
        article = form_data.get(f"{prefix}_article_{i}", "")
        if article:
            ach = await create_achievement(AchievementCreate(
                person_id=opponent_id,
                type=1,
                text_content=article,
                year=extract_year(article) or 2020,
                quartile=None
            ))
            await database.execute(
                "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main) "
                "VALUES (:tid, :aid, false) ON CONFLICT DO NOTHING",
                {"tid": thesis_id, "aid": ach["id"]}
            )


async def process_achievements(thesis_id: int, applicant_id: int, form_data: dict):
    for i in range(1, 17):
        text = form_data.get(f"applicant_article_{i}", "")
        if not text:
            continue
        quartile = form_data.get(f"applicant_article_BD_{i}", "")
        if quartile and len(quartile) > 32:
            quartile = quartile[:32]
        contribution = form_data.get(f"applicant_article_contribution_{i}", "")
        year = extract_year(text)
        ach = await create_achievement(AchievementCreate(
            person_id=applicant_id,
            type=1,
            text_content=text,
            year=year or 2020,
            quartile=quartile if quartile else None
        ))
        is_main = i <= 3
        await database.execute(
            "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main, author_contribution) "
            "VALUES (:tid, :aid, :is_main, :contr) "
            "ON CONFLICT (thesis_id, achievement_id) DO UPDATE SET is_main = :is_main, author_contribution = :contr",
            {"tid": thesis_id, "aid": ach["id"], "is_main": is_main, "contr": contribution}
        )

    for i in range(1, 31):
        text = form_data.get(f"applicant_conference_{i}", "")
        if not text:
            continue
        ach = await create_achievement(AchievementCreate(
            person_id=applicant_id,
            type=3,
            text_content=text,
            year=extract_year(text) or 2020
        ))
        await database.execute(
            "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main) "
            "VALUES (:tid, :aid, false) ON CONFLICT DO NOTHING",
            {"tid": thesis_id, "aid": ach["id"]}
        )

    for i in range(1, 31):
        text = form_data.get(f"applicant_thesis_{i}", "")
        if not text:
            continue
        ach = await create_achievement(AchievementCreate(
            person_id=applicant_id,
            type=3,
            text_content=text,
            year=extract_year(text) or 2020
        ))
        await database.execute(
            "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main) "
            "VALUES (:tid, :aid, false) ON CONFLICT DO NOTHING",
            {"tid": thesis_id, "aid": ach["id"]}
        )

    for i in range(1, 6):
        text = form_data.get(f"applicant_RID_{i}", "")
        if not text:
            continue
        ach = await create_achievement(AchievementCreate(
            person_id=applicant_id,
            type=2,
            text_content=text,
            year=extract_year(text) or 2020
        ))
        await database.execute(
            "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main) "
            "VALUES (:tid, :aid, false) ON CONFLICT DO NOTHING",
            {"tid": thesis_id, "aid": ach["id"]}
        )


async def process_content_blocks(thesis_id: int, form_data: dict):
    for (block_type, prefix, cnt) in [
        ("task", "thesis_tasks", 8),
        ("novelty", "thesis_novelty", 6),
        ("value", "thesis_value", 6),
        ("provision", "thesis_provision", 6),
        ("specialty_passport", "applicant_speciality_pasport_item_text", 3),
    ]:
        for i in range(1, cnt + 1):
            content = form_data.get(f"{prefix}_{i}", "")
            await _upsert_content_block(thesis_id, block_type, content, i)

    for role, name_field, degree_field in [
        ("department_head", "departament_head_name", "departament_head_degree"),
        ("faculty_head", "faculty_head_name", "faculty_head_degree")
    ]:
        name = form_data.get(name_field, "")
        degree = form_data.get(degree_field, "")
        content = f"{degree} {name}".strip()
        await _upsert_content_block(thesis_id, role, content, 200)

    pub = form_data.get("applicant_artciles_number_total_W", "")
    await _upsert_content_block(thesis_id, "publications_info", f"Число публикаций: {pub}", 100)

    dept_num = form_data.get("applicant_department_number", "")
    dept_title = form_data.get("applicant_department_title", "")
    await _upsert_content_block(thesis_id, "applicant_department", f"{dept_num} {dept_title}".strip(), 300)

    dir_num = form_data.get("applicant_PG_direction_number", "")
    dir_title = form_data.get("applicant_PG_direction_title", "")
    await _upsert_content_block(thesis_id, "pg_direction", f"{dir_num} {dir_title}".strip(), 301)

    for field, bt in [
        ("seminar_departament_number", "seminar_dep_number"),
        ("seminar_departament_title", "seminar_dep_title"),
        ("seminar_faculty", "seminar_faculty"),
    ]:
        val = form_data.get(field, "")
        await _upsert_content_block(thesis_id, bt, val, 302)


async def process_events(thesis_id: int, form_data: dict):
    if form_data.get("seminar_protocol_number"):
        await database.execute(
            "INSERT INTO ds_event (thesis_id, event_type, protocol_number, protocol_date) "
            "VALUES (:tid, 'seminar', :num, :date) ON CONFLICT DO NOTHING",
            {"tid": thesis_id,
             "num": form_data["seminar_protocol_number"],
             "date": parse_russian_date(form_data.get("seminar_date", "2020-01-01"))}
        )
    if form_data.get("18_1_protocol_number"):
        await database.execute(
            "INSERT INTO ds_event (thesis_id, event_type, protocol_number, protocol_date, votes_total, votes_yes) "
            "VALUES (:tid, 'commission_creation', :num, :date, :total, :yes) ON CONFLICT DO NOTHING",
            {"tid": thesis_id,
             "num": form_data["18_1_protocol_number"],
             "date": parse_russian_date(form_data.get("18_1_protocol_date", "2020-01-01")),
             "total": form_data.get("18_1_vote_results"),
             "yes": form_data.get("18_1_vote_results")}
        )
    if form_data.get("19_2_protocol_number"):
        await database.execute(
            "INSERT INTO ds_event (thesis_id, event_type, protocol_number, protocol_date, votes_total, votes_yes) "
            "VALUES (:tid, 'acceptance_for_defense', :num, :date, :total, :yes) ON CONFLICT DO NOTHING",
            {"tid": thesis_id,
             "num": form_data["19_2_protocol_number"],
             "date": parse_russian_date(form_data.get("19_2_protocol_date", "2020-01-01")),
             "total": form_data.get("19_2_vote_results"),
             "yes": form_data.get("19_2_vote_results")}
        )


async def process_thesis_form(thesis_id: int, form_data: dict):
    query = """
        SELECT 
            t.id AS thesis_id,
            t.applicant_id,
            t.council_id,
            t.specialty_id,
            dc.chairman_id,
            dc.secretary_id,
            (SELECT tp.person_id FROM thesis_participation tp 
             WHERE tp.thesis_id = t.id AND tp.role = 'supervisor' LIMIT 1) AS supervisor_id,
            (SELECT jsonb_object_agg(too.order_index::text, too.person_id) 
             FROM thesis_official_opponent too WHERE too.thesis_id = t.id) AS opponents
        FROM thesis t
        JOIN dissertation_council dc ON t.council_id = dc.id
        WHERE t.id = :id
    """
    row = await database.fetch_one(query, {"id": thesis_id})
    if not row:
        raise HTTPException(status_code=404, detail="Диссертация не найдена")

    opponents_raw = row["opponents"]
    opponents = {}
    if isinstance(opponents_raw, str):
        try:
            opponents = json.loads(opponents_raw)
        except json.JSONDecodeError:
            pass
    elif opponents_raw:
        opponents = dict(opponents_raw)

    ctx = {
        "thesis_id": row["thesis_id"],
        "applicant_id": row["applicant_id"],
        "council_id": row["council_id"],
        "specialty_id": row["specialty_id"],
        "chairman_id": row["chairman_id"],
        "secretary_id": row["secretary_id"],
        "supervisor_id": row["supervisor_id"],
    }
    for i in range(1, 4):
        ctx[f"opponent_{i}_id"] = opponents.get(str(i))

    thesis_upd = {}
    if form_data.get("thesis_title"): thesis_upd["title"] = form_data["thesis_title"]
    if form_data.get("degree_R"): thesis_upd["target_degree"] = form_data["degree_R"]
    if form_data.get("thesis_participation"): thesis_upd["personal_participation"] = form_data["thesis_participation"]
    if form_data.get("thesis_reliability"): thesis_upd["reliability_text"] = form_data["thesis_reliability"]
    if form_data.get("achievement"): thesis_upd["achievement_summary"] = form_data["achievement"]
    if form_data.get("applicant_speciality_type"): thesis_upd["science_branch"] = form_data["applicant_speciality_type"]

    if form_data.get("planned_defence_date"):
        thesis_upd["planned_defence_date"] = parse_russian_date(form_data["planned_defence_date"])
    defence_d = parse_russian_date(form_data.get("defence_date", ""))
    if defence_d and form_data.get("defence_time"):
        try:
            t = datetime.strptime(form_data["defence_time"], "%H:%M").time()
            thesis_upd["defence_date_time"] = datetime.combine(defence_d, t)
        except ValueError:
            pass
    if form_data.get("data_publishing_MEPhI"):
        thesis_upd["website_publish_date"] = parse_russian_date(form_data["data_publishing_MEPhI"])
    if form_data.get("link_screenshot_publishing_MEPhI"): thesis_upd["website_link"] = form_data["link_screenshot_publishing_MEPhI"]
    if form_data.get("link_text_publishing_MEPhI"): thesis_upd["dissertation_text_link"] = form_data["link_text_publishing_MEPhI"]

    if thesis_upd:
        await update_thesis(thesis_id, ThesisUpdate(**thesis_upd))

    if form_data.get("DS_number"):
        await update_council(ctx["council_id"], CouncilUpdate(number=form_data["DS_number"]))

    if form_data.get("DS_chairman_degree"):
        await update_person(ctx["chairman_id"], PersonUpdate(degree=form_data["DS_chairman_degree"]))
    if form_data.get("DS_secretary_degree"):
        await update_person(ctx["secretary_id"], PersonUpdate(degree=form_data["DS_secretary_degree"]))

    applicant_id = ctx["applicant_id"]
    app_name = parse_full_name(form_data.get("applicant_full_name_I", ""))
    if app_name:
        await update_person(applicant_id, PersonUpdate(**app_name))
    pers_upd = {}
    if form_data.get("applicant_email"): pers_upd["email"] = form_data["applicant_email"]
    if form_data.get("applicant_phone_number"): pers_upd["phone_number"] = form_data["applicant_phone_number"]
    if pers_upd:
        await update_person(applicant_id, PersonUpdate(**pers_upd))

    det_upd = {}
    det_map = {
        "applicant_SNILS": "snils",
        "applicant_document": "passport_type",
        "applicant_document_series": "passport_series",
        "applicant_document_number": "passport_number",
        "applicant_full_adress": "home_address",
    }
    for fk, dbk in det_map.items():
        if form_data.get(fk):
            det_upd[dbk] = form_data[fk]
    if form_data.get("end_of_postgrad_date"):
        det_upd["is_postgrad_completed"] = True
        det_upd["postgrad_end_date"] = parse_russian_date(form_data["end_of_postgrad_date"])

    if det_upd:
        existing = await database.fetch_one("SELECT person_id FROM applicant_details WHERE person_id = :pid", {"pid": applicant_id})
        if existing:
            await update_details(applicant_id, ApplicantDetailsUpdate(**det_upd))
        else:
            full_det = {
                "person_id": applicant_id,
                "snils": det_upd.get("snils", "000-000-000 00"),
                "passport_type": det_upd.get("passport_type", "паспорт"),
                "passport_series": det_upd.get("passport_series", "0000"),
                "passport_number": det_upd.get("passport_number", "000000"),
                "home_address": det_upd.get("home_address", "Не указан"),
                "sex": 1,
                "birth_date": date(1900, 1, 1),
                "is_postgrad_completed": det_upd.get("is_postgrad_completed", False),
                "postgrad_end_date": det_upd.get("postgrad_end_date"),
            }
            for k, v in det_upd.items():
                if v is not None:
                    full_det[k] = v
            await create_details(ApplicantDetailsCreate(**full_det))

    if form_data.get("applicant_job_organisation"):
        org_name = form_data["applicant_job_organisation"]
        org = await database.fetch_one("SELECT id FROM organization WHERE full_name = :name", {"name": org_name})
        org_id = org["id"] if org else None
        if not org_id:
            org_id = await database.execute(
                "INSERT INTO organization (full_name, short_name, address) VALUES (:full_name, :short_name, :address) RETURNING id",
                {"full_name": org_name, "short_name": org_name[:64], "address": form_data.get("applicant_full_adress", "Не указан")}
            )
        dept_num = form_data.get("applicant_job_department_number", "")
        dept_title = form_data.get("applicant_job_department_title", "")
        division_str = f"{dept_num} - {dept_title}" if dept_num or dept_title else None

        existing_main = await database.fetch_one(
            "SELECT id FROM employment_history WHERE person_id = :pid AND is_additional = false", {"pid": applicant_id}
        )
        if existing_main:
            await database.execute(
                "UPDATE employment_history SET organization_id = :oid, position = :pos, division = :div WHERE id = :eid",
                {"oid": org_id, "pos": form_data.get("applicant_main_job"),
                 "div": division_str, "eid": existing_main["id"]}
            )
        else:
            await create_employment(EmploymentCreate(
                person_id=applicant_id,
                organization_id=org_id,
                position=form_data.get("applicant_main_job"),
                division=division_str,
                start_date=date(2000, 1, 1),
                is_additional=False
            ))

    if form_data.get("applicant_addition_job_place"):
        org_name = form_data["applicant_addition_job_place"]
        org = await database.fetch_one("SELECT id FROM organization WHERE full_name = :name", {"name": org_name})
        org_id = org["id"] if org else None
        if not org_id:
            org_id = await database.execute(
                "INSERT INTO organization (full_name, short_name, address) VALUES (:full_name, :short_name, :address) RETURNING id",
                {"full_name": org_name, "short_name": org_name[:64], "address": "—"}
            )
        existing_add = await database.fetch_one(
            "SELECT id FROM employment_history WHERE person_id = :pid AND is_additional = true", {"pid": applicant_id}
        )
        if existing_add:
            await database.execute(
                "UPDATE employment_history SET organization_id = :oid, position = :pos WHERE id = :eid",
                {"oid": org_id, "pos": form_data.get("applicant_addition_job"), "eid": existing_add["id"]}
            )
        else:
            await create_employment(EmploymentCreate(
                person_id=applicant_id,
                organization_id=org_id,
                position=form_data.get("applicant_addition_job"),
                start_date=date(2000, 1, 1),
                is_additional=True
            ))

    if form_data.get("applicant_HE_type"):
        spec_id = None
        if form_data.get("applicant_HE_direction_number"):
            spec_row = await database.fetch_one("SELECT id FROM specialty WHERE code = :code", {"code": form_data["applicant_HE_direction_number"]})
            spec_id = spec_row["id"] if spec_row else None
        org_name = None
        parts = form_data["applicant_HE_type"].split()
        if len(parts) > 1:
            org_name = " ".join(parts[1:])
        org_id = None
        if org_name:
            org_row = await database.fetch_one("SELECT id FROM organization WHERE full_name = :name", {"name": org_name})
            org_id = org_row["id"] if org_row else None
        await create_education(EducationCreate(
            person_id=applicant_id,
            edu_level=form_data["applicant_HE_type"],
            end_year=form_data.get("applicant_HE_end_year"),
            is_honors=form_data.get("applicant_excellency") == "с отличием",
            qualification=form_data.get("applicant_HE_qualification"),
            organization_id=org_id,
            specialty_id=spec_id
        ))

    if form_data.get("applicant_PG_study"):
        spec_id = None
        if form_data.get("applicant_PG_speciality_number"):
            spec_row = await database.fetch_one("SELECT id FROM specialty WHERE code = :code", {"code": form_data["applicant_PG_speciality_number"]})
            spec_id = spec_row["id"] if spec_row else None
        org_name = None
        parts = form_data["applicant_PG_study"].split()
        if len(parts) > 1:
            org_name = " ".join(parts[1:])
        org_id = None
        if org_name:
            org_row = await database.fetch_one("SELECT id FROM organization WHERE full_name = :name", {"name": org_name})
            org_id = org_row["id"] if org_row else None
        ref_date = parse_russian_date(form_data.get("applicant_PG_reference_date"))
        await create_education(EducationCreate(
            person_id=applicant_id,
            edu_level=form_data["applicant_PG_study"],
            end_year=form_data.get("applicant_PG_end_year"),
            reference_date=ref_date,
            organization_id=org_id,
            specialty_id=spec_id
        ))

    supervisor_id = ctx["supervisor_id"]
    sup_name = parse_full_name(form_data.get("advisor_name_full", ""))
    if sup_name:
        sup_data = {
            "last_name": sup_name["last_name"],
            "first_name": sup_name["first_name"],
            "second_name": sup_name.get("second_name"),
            "degree": form_data.get("advisor_degree"),
            "academic_title": form_data.get("advisor_title"),
            "email": form_data.get("advisor_email"),
            "phone_number": form_data.get("advisor_phone_number"),
            "specialty_id": ctx["specialty_id"],
        }
        if not supervisor_id:
            new_sup = await create_person(PersonCreate(**sup_data))
            supervisor_id = new_sup["id"]
            await add_participation(thesis_id, ParticipationCreate(
                thesis_id=thesis_id, person_id=supervisor_id, role="supervisor", order_index=1
            ))
        else:
            await update_person(supervisor_id, PersonUpdate(**sup_data))

        org_name = form_data.get("advisor_main_workplace_full", "")
        if org_name:
            org = await database.fetch_one("SELECT id FROM organization WHERE full_name = :name", {"name": org_name})
            org_id = org["id"] if org else None
            if not org_id:
                org_id = await database.execute(
                    "INSERT INTO organization (full_name, short_name, address) VALUES (:full_name, :short_name, :address) RETURNING id",
                    {"full_name": org_name, "short_name": org_name[:64], "address": form_data.get("advisor_main_workplace_adress", "—")}
                )
            existing_emp = await database.fetch_one(
                "SELECT id FROM employment_history WHERE person_id = :pid AND is_additional = false", {"pid": supervisor_id}
            )
            if existing_emp:
                await database.execute(
                    "UPDATE employment_history SET organization_id = :oid, position = :pos, division = :div WHERE id = :eid",
                    {"oid": org_id, "pos": form_data.get("advisor_main_job"),
                     "div": form_data.get("advisor_main_workplace_division"), "eid": existing_emp["id"]}
                )
            else:
                await create_employment(EmploymentCreate(
                    person_id=supervisor_id,
                    organization_id=org_id,
                    position=form_data.get("advisor_main_job"),
                    division=form_data.get("advisor_main_workplace_division"),
                    start_date=date(2000, 1, 1),
                    is_additional=False
                ))

        for i in range(1, 16):
            article = form_data.get(f"advisor_article_{i}", "")
            if article:
                ach = await create_achievement(AchievementCreate(
                    person_id=supervisor_id,
                    type=1,
                    text_content=article,
                    year=extract_year(article) or 2020,
                    quartile=None
                ))
                await database.execute(
                    "INSERT INTO thesis_achievement (thesis_id, achievement_id, is_main) "
                    "VALUES (:tid, :aid, false) ON CONFLICT DO NOTHING",
                    {"tid": thesis_id, "aid": ach["id"]}
                )

    for i in range(1, 4):
        await process_opponent(thesis_id, ctx, form_data, i)

    await process_achievements(thesis_id, applicant_id, form_data)
    await process_content_blocks(thesis_id, form_data)
    await process_events(thesis_id, form_data)
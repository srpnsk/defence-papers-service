# data_assembler.py
import logging
from database import database
from models import ThesisFormData

logger = logging.getLogger("data_assembler")
logging.basicConfig(level=logging.INFO)

def _safe_str(value) -> str:
    return str(value) if value is not None else ""

async def assemble_full_thesis_json(thesis_id: int) -> dict:
    result = {key: "" for key in ThesisFormData.__fields__}

    thesis_query = """
        SELECT 
            t.title,
            t.target_degree,
            t.science_branch,
            t.planned_defence_date,
            t.defence_date_time,
            t.website_publish_date,
            t.website_link,
            t.dissertation_text_link,
            t.achievement_summary,
            t.reliability_text,
            t.personal_participation,
            t.applicant_id,
            t.specialty_id,
            dc.number AS ds_number,
            dc.chairman_id,
            dc.secretary_id
        FROM thesis t
        JOIN dissertation_council dc ON t.council_id = dc.id
        WHERE t.id = :id
    """
    thesis_row = await database.fetch_one(thesis_query, {"id": thesis_id})
    if not thesis_row:
        logger.warning(f"Thesis {thesis_id} not found")
        return result

    thesis = dict(thesis_row)

    result["DS_number"] = _safe_str(thesis.get("ds_number"))
    result["thesis_title"] = _safe_str(thesis.get("title"))
    result["degree_R"] = _safe_str(thesis.get("target_degree"))
    result["science_branch"] = _safe_str(thesis.get("science_branch"))
    result["achievement"] = _safe_str(thesis.get("achievement_summary"))
    result["thesis_reliability"] = _safe_str(thesis.get("reliability_text"))
    result["thesis_participation"] = _safe_str(thesis.get("personal_participation"))
    result["link_screenshot_publishing_MEPhI"] = _safe_str(thesis.get("website_link"))
    result["link_text_publishing_MEPhI"] = _safe_str(thesis.get("dissertation_text_link"))
    result["applicant_speciality_type"] = _safe_str(thesis.get("science_branch"))

    if thesis.get("planned_defence_date"):
        result["planned_defence_date"] = str(thesis["planned_defence_date"])
    if thesis.get("defence_date_time"):
        dt = thesis["defence_date_time"]
        result["defence_date"] = dt.strftime("%d.%m.%Y")
        result["defence_time"] = dt.strftime("%H:%M")
    if thesis.get("website_publish_date"):
        result["data_publishing_MEPhI"] = str(thesis["website_publish_date"])

    for role, prefix in [("chairman_id", "DS_chairman"), ("secretary_id", "DS_secretary")]:
        person_id = thesis.get(role)
        if person_id:
            person_row = await database.fetch_one(
                "SELECT last_name, first_name, second_name, degree FROM person WHERE id = :id",
                {"id": person_id}
            )
            if person_row:
                p = dict(person_row)
                full = f"{p.get('last_name','')} {p.get('first_name','')}"
                if p.get('second_name'):
                    full += f" {p['second_name']}"
                result[f"{prefix}_name_I"] = full.strip()
                result[f"{prefix}_name_D"] = full.strip()
                result[f"{prefix}_degree"] = _safe_str(p.get("degree"))

    applicant_id = thesis.get("applicant_id")
    if applicant_id:
        applicant_row = await database.fetch_one(
            "SELECT last_name, first_name, second_name, email, phone_number FROM person WHERE id = :id",
            {"id": applicant_id}
        )
        if applicant_row:
            a = dict(applicant_row)
            full = f"{a.get('last_name','')} {a.get('first_name','')}"
            if a.get('second_name'):
                full += f" {a['second_name']}"
            result["applicant_full_name_I"] = full
            short = f"{a['last_name']}~{a['first_name'][0]}."
            if a.get('second_name'):
                short += f"{a['second_name'][0]}."
            result["applicant_short_name_I"] = short
            result["applicant_full_name_R"] = full + "а" if full.endswith("в") or full.endswith("н") else full
            result["applicant_short_name_R"] = short
            result["applicant_email"] = _safe_str(a.get("email"))
            result["applicant_phone_number"] = _safe_str(a.get("phone_number"))

        details_row = await database.fetch_one(
            "SELECT snils, passport_type, passport_series, passport_number, home_address, postgrad_end_date "
            "FROM applicant_details WHERE person_id = :pid",
            {"pid": applicant_id}
        )
        if details_row:
            d = dict(details_row)
            result["applicant_SNILS"] = _safe_str(d.get("snils"))
            result["applicant_document"] = _safe_str(d.get("passport_type"))
            result["applicant_document_series"] = _safe_str(d.get("passport_series"))
            result["applicant_document_number"] = _safe_str(d.get("passport_number"))
            result["applicant_full_adress"] = _safe_str(d.get("home_address"))
            if d.get("postgrad_end_date"):
                result["end_of_postgrad_date"] = str(d["postgrad_end_date"])

        main_emp_row = await database.fetch_one(
            """SELECT e.position, e.division, o.full_name
               FROM employment_history e
               JOIN organization o ON e.organization_id = o.id
               WHERE e.person_id = :pid AND e.is_additional = false""",
            {"pid": applicant_id}
        )
        if main_emp_row:
            me = dict(main_emp_row)
            result["applicant_job_organisation"] = _safe_str(me.get("full_name"))
            result["applicant_main_job"] = _safe_str(me.get("position"))
            division = me.get("division") or ""
            if " - " in division:
                num, title = division.split(" - ", 1)
                result["applicant_job_department_number"] = num
                result["applicant_job_department_title"] = title
            else:
                result["applicant_job_department_title"] = division

        add_emp_row = await database.fetch_one(
            """SELECT e.position, o.full_name
               FROM employment_history e
               JOIN organization o ON e.organization_id = o.id
               WHERE e.person_id = :pid AND e.is_additional = true""",
            {"pid": applicant_id}
        )
        if add_emp_row:
            ae = dict(add_emp_row)
            result["applicant_addition_job"] = _safe_str(ae.get("position"))
            result["applicant_addition_job_place"] = _safe_str(ae.get("full_name"))

        edu_rows = await database.fetch_all(
            "SELECT edu_level, end_year, is_honors, qualification, reference_date, specialty_id "
            "FROM education_history WHERE person_id = :pid ORDER BY id",
            {"pid": applicant_id}
        )
        for edu_row in edu_rows:
            edu = dict(edu_row)
            if edu.get("edu_level") and "аспирант" in edu["edu_level"].lower():
                result["applicant_PG_study"] = _safe_str(edu.get("edu_level"))
                result["applicant_PG_end_year"] = edu.get("end_year")
                if edu.get("reference_date"):
                    result["applicant_PG_reference_date"] = str(edu["reference_date"])
                if edu.get("specialty_id"):
                    spec_row = await database.fetch_one("SELECT code, name FROM specialty WHERE id = :id", {"id": edu["specialty_id"]})
                    if spec_row:
                        sp = dict(spec_row)
                        result["applicant_PG_speciality_number"] = _safe_str(sp.get("code"))
                        result["applicant_PG_speciality_title"] = _safe_str(sp.get("name"))
            else:
                result["applicant_HE_type"] = _safe_str(edu.get("edu_level"))
                result["applicant_HE_end_year"] = edu.get("end_year")
                result["applicant_HE_qualification"] = _safe_str(edu.get("qualification"))
                result["applicant_excellency"] = "с отличием" if edu.get("is_honors") else ""
                if edu.get("specialty_id"):
                    spec_row = await database.fetch_one("SELECT code, name FROM specialty WHERE id = :id", {"id": edu["specialty_id"]})
                    if spec_row:
                        sp = dict(spec_row)
                        result["applicant_HE_direction_number"] = _safe_str(sp.get("code"))
                        result["applicant_HE_direction_title"] = _safe_str(sp.get("name"))

    specialty_id = thesis.get("specialty_id")
    if specialty_id:
        spec_row = await database.fetch_one("SELECT code, name FROM specialty WHERE id = :id", {"id": specialty_id})
        if spec_row:
            sp = dict(spec_row)
            result["applicant_specialty_number"] = _safe_str(sp.get("code"))
            result["applicant_specialty_title"] = _safe_str(sp.get("name"))

    supervisor_row = await database.fetch_one(
        """SELECT p.* FROM thesis_participation tp
           JOIN person p ON tp.person_id = p.id
           WHERE tp.thesis_id = :tid AND tp.role = 'supervisor'""",
        {"tid": thesis_id}
    )
    if supervisor_row:
        sup = dict(supervisor_row)
        full = f"{sup.get('last_name','')} {sup.get('first_name','')}"
        if sup.get('second_name'):
            full += f" {sup['second_name']}"
        result["advisor_name_full"] = full
        short = f"{sup['last_name']}~{sup['first_name'][0]}."
        if sup.get('second_name'):
            short += f"{sup['second_name'][0]}."
        result["advisor_name_short"] = short
        result["advisor_degree"] = _safe_str(sup.get("degree"))
        result["advisor_title"] = _safe_str(sup.get("academic_title"))
        result["advisor_degree_title"] = f"{sup.get('degree')}, {sup.get('academic_title')}" if sup.get('degree') and sup.get('academic_title') else _safe_str(sup.get('degree'))
        result["advisor_email"] = _safe_str(sup.get("email"))
        result["advisor_phone_number"] = _safe_str(sup.get("phone_number"))
        if sup.get("specialty_id"):
            spec_row = await database.fetch_one("SELECT code, name FROM specialty WHERE id = :id", {"id": sup["specialty_id"]})
            if spec_row:
                sp = dict(spec_row)
                result["advisor_specialty_number"] = _safe_str(sp.get("code"))
                result["advisor_specialty_title"] = _safe_str(sp.get("name"))

        emp_row = await database.fetch_one(
            """SELECT e.position, e.division, o.full_name, o.address
               FROM employment_history e
               JOIN organization o ON e.organization_id = o.id
               WHERE e.person_id = :pid AND e.is_additional = false""",
            {"pid": sup["id"]}
        )
        if emp_row:
            em = dict(emp_row)
            result["advisor_main_job"] = _safe_str(em.get("position"))
            result["advisor_main_workplace_full"] = _safe_str(em.get("full_name"))
            result["advisor_main_workplace_division"] = _safe_str(em.get("division"))
            result["advisor_main_workplace_adress"] = _safe_str(em.get("address"))

        sup_articles = await database.fetch_all(
            "SELECT text_content FROM achievement WHERE person_id = :pid AND type = 1 ORDER BY year DESC LIMIT 15",
            {"pid": sup["id"]}
        )
        for i, art in enumerate(sup_articles, start=1):
            a = dict(art)
            result[f"advisor_article_{i}"] = a["text_content"]

    for i in range(1, 4):
        opp_row = await database.fetch_one(
            """SELECT p.* FROM thesis_official_opponent too
               JOIN person p ON too.person_id = p.id
               WHERE too.thesis_id = :tid AND too.order_index = :idx""",
            {"tid": thesis_id, "idx": i}
        )
        if opp_row:
            opp = dict(opp_row)
            full = f"{opp.get('last_name','')} {opp.get('first_name','')}"
            if opp.get('second_name'):
                full += f" {opp['second_name']}"
            result[f"opponent{i}_name_full_I"] = full
            short = f"{opp['last_name']}~{opp['first_name'][0]}."
            if opp.get('second_name'):
                short += f"{opp['second_name'][0]}."
            result[f"opponent{i}_name_short"] = short
            result[f"opponent{i}_degree"] = _safe_str(opp.get("degree"))
            result[f"opponent{i}_title"] = _safe_str(opp.get("academic_title"))
            result[f"opponent{i}_degree_title"] = f"{opp.get('degree')}, {opp.get('academic_title')}" if opp.get('degree') and opp.get('academic_title') else _safe_str(opp.get('degree'))
            result[f"opponent{i}_email"] = _safe_str(opp.get("email"))
            result[f"opponent{i}_phone_number"] = _safe_str(opp.get("phone_number"))
            if opp.get("specialty_id"):
                spec_row = await database.fetch_one("SELECT code, name FROM specialty WHERE id = :id", {"id": opp["specialty_id"]})
                if spec_row:
                    sp = dict(spec_row)
                    result[f"opponent{i}_specialty_number"] = _safe_str(sp.get("code"))
                    result[f"opponent{i}_specialty_title"] = _safe_str(sp.get("name"))

            emp_row = await database.fetch_one(
                """SELECT e.position, e.division, o.full_name, o.address
                   FROM employment_history e
                   JOIN organization o ON e.organization_id = o.id
                   WHERE e.person_id = :pid AND e.is_additional = false""",
                {"pid": opp["id"]}
            )
            if emp_row:
                em = dict(emp_row)
                result[f"opponent{i}_main_job"] = _safe_str(em.get("position"))
                result[f"opponent{i}_main_workplace_full"] = _safe_str(em.get("full_name"))
                result[f"opponent{i}_main_workplace_division"] = _safe_str(em.get("division"))
                result[f"opponent{i}_main_workplace_adress"] = _safe_str(em.get("address"))

            opp_articles = await database.fetch_all(
                "SELECT text_content FROM achievement WHERE person_id = :pid AND type = 1 ORDER BY year DESC LIMIT 15",
                {"pid": opp["id"]}
            )
            for j, art in enumerate(opp_articles, start=1):
                a = dict(art)
                result[f"opponent{i}_article_{j}"] = a["text_content"]

    if applicant_id:
        ach_rows = await database.fetch_all(
            """SELECT a.type, a.text_content, a.quartile, ta.author_contribution
               FROM thesis_achievement ta
               JOIN achievement a ON ta.achievement_id = a.id
               WHERE ta.thesis_id = :tid
               ORDER BY a.year DESC, a.id""",
            {"tid": thesis_id}
        )
        art_idx = conf_idx = thes_idx = rid_idx = 0
        for ach_row in ach_rows:
            ach = dict(ach_row)
            if ach["type"] == 1:
                art_idx += 1
                if art_idx <= 16:
                    result[f"applicant_article_{art_idx}"] = ach["text_content"]
                    result[f"applicant_article_BD_{art_idx}"] = _safe_str(ach.get("quartile"))
                    result[f"applicant_article_contribution_{art_idx}"] = _safe_str(ach.get("author_contribution"))
            elif ach["type"] == 2:
                rid_idx += 1
                if rid_idx <= 5:
                    result[f"applicant_RID_{rid_idx}"] = ach["text_content"]
            elif ach["type"] == 3:
                text = ach["text_content"].lower()
                if "конференц" in text or "симпозиум" in text:
                    conf_idx += 1
                    if conf_idx <= 30:
                        result[f"applicant_conference_{conf_idx}"] = ach["text_content"]
                else:
                    thes_idx += 1
                    if thes_idx <= 30:
                        result[f"applicant_thesis_{thes_idx}"] = ach["text_content"]

    blocks = await database.fetch_all(
        "SELECT block_type, content, order_index FROM thesis_content_block WHERE thesis_id = :tid",
        {"tid": thesis_id}
    )
    for blk_row in blocks:
        blk = dict(blk_row)
        btype = blk["block_type"]
        content = blk["content"]
        idx = blk["order_index"]
        if btype == "task" and 1 <= idx <= 8:
            result[f"thesis_tasks_{idx}"] = content
        elif btype == "novelty" and 1 <= idx <= 6:
            result[f"thesis_novelty_{idx}"] = content
        elif btype == "value" and 1 <= idx <= 6:
            result[f"thesis_value_{idx}"] = content
        elif btype == "provision" and 1 <= idx <= 6:
            result[f"thesis_provision_{idx}"] = content
        elif btype == "specialty_passport" and 1 <= idx <= 3:
            result[f"applicant_speciality_pasport_item_text_{idx}"] = content
        elif btype == "department_head":
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                result["departament_head_degree"] = parts[0]
                result["departament_head_name"] = parts[1]
            else:
                result["departament_head_name"] = content
        elif btype == "faculty_head":
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                result["faculty_head_degree"] = parts[0]
                result["faculty_head_name"] = parts[1]
            else:
                result["faculty_head_name"] = content
        elif btype == "publications_info":
            result["applicant_artciles_number_total_W"] = content
        elif btype == "applicant_department":
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                result["applicant_department_number"] = parts[0]
                result["applicant_department_title"] = parts[1]
            else:
                result["applicant_department_title"] = content
        elif btype == "pg_direction":
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                result["applicant_PG_direction_number"] = parts[0]
                result["applicant_PG_direction_title"] = parts[1]
            else:
                result["applicant_PG_direction_title"] = content
        elif btype == "seminar_dep_number":
            result["seminar_departament_number"] = content
        elif btype == "seminar_dep_title":
            result["seminar_departament_title"] = content
        elif btype == "seminar_faculty":
            result["seminar_faculty"] = content

    event_rows = await database.fetch_all(
        "SELECT event_type, protocol_number, protocol_date, votes_total FROM ds_event WHERE thesis_id = :tid",
        {"tid": thesis_id}
    )
    for ev_row in event_rows:
        ev = dict(ev_row)
        if ev["event_type"] == "commission_creation":
            result["18_1_protocol_number"] = ev["protocol_number"]
            result["18_1_protocol_date"] = str(ev["protocol_date"])
            result["18_1_vote_results"] = ev["votes_total"]
        elif ev["event_type"] == "acceptance_for_defense":
            result["19_2_protocol_number"] = ev["protocol_number"]
            result["19_2_protocol_date"] = str(ev["protocol_date"])
            result["19_2_vote_results"] = ev["votes_total"]
        elif ev["event_type"] == "seminar":
            result["seminar_protocol_number"] = ev["protocol_number"]
            result["seminar_date"] = str(ev["protocol_date"])

    return result
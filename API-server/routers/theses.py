from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import database
from models import ThesisCreate, ThesisUpdate, ThesisOut, OpponentCreate, OpponentOut, ParticipationCreate, ParticipationOut, DsEventCreate, DsEventOut
from datetime import date

router = APIRouter(prefix="/theses", tags=["theses"])

@router.get("/", response_model=List[ThesisOut])
async def list_theses(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    query = "SELECT * FROM thesis ORDER BY id LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{thesis_id}", response_model=ThesisOut)
async def get_thesis(thesis_id: int):
    query = "SELECT * FROM thesis WHERE id = :id"
    row = await database.fetch_one(query, {"id": thesis_id})
    if not row:
        raise HTTPException(status_code=404, detail="Диссертация не найдена")
    return dict(row)

@router.post("/", response_model=ThesisOut, status_code=201)
async def create_thesis(thesis: ThesisCreate):
    query = """
        INSERT INTO thesis (applicant_id, council_id, title, science_branch, target_degree, planned_defence_date, defence_date_time,
                            website_publish_date, website_link, dissertation_text_link, achievement_summary, reliability_text,
                            personal_participation, specialty_id)
        VALUES (:applicant_id, :council_id, :title, :science_branch, :target_degree, :planned_defence_date, :defence_date_time,
                :website_publish_date, :website_link, :dissertation_text_link, :achievement_summary, :reliability_text,
                :personal_participation, :specialty_id)
        RETURNING id
    """
    values = thesis.dict()
    new_id = await database.execute(query, values)
    return await get_thesis(new_id)

@router.put("/{thesis_id}", response_model=ThesisOut)
async def update_thesis(thesis_id: int, thesis: ThesisUpdate):
    await get_thesis(thesis_id)
    updates = {k: v for k, v in thesis.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_thesis(thesis_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE thesis SET {set_clause} WHERE id = :id"
    values = {**updates, "id": thesis_id}
    await database.execute(query, values)
    return await get_thesis(thesis_id)

@router.delete("/{thesis_id}", status_code=204)
async def delete_thesis(thesis_id: int):
    await get_thesis(thesis_id)
    query = "DELETE FROM thesis WHERE id = :id"
    await database.execute(query, {"id": thesis_id})
    return

# Дополнительные эндпоинты для связанных сущностей
@router.post("/{thesis_id}/opponents", response_model=OpponentOut, status_code=201)
async def add_opponent(thesis_id: int, opponent: OpponentCreate):
    await get_thesis(thesis_id)
    query = """
        INSERT INTO thesis_official_opponent (thesis_id, person_id, order_index)
        VALUES (:thesis_id, :person_id, :order_index)
        RETURNING id
    """
    values = opponent.dict()
    values["thesis_id"] = thesis_id
    new_id = await database.execute(query, values)
    # Получить созданную запись
    get_query = "SELECT * FROM thesis_official_opponent WHERE id = :id"
    row = await database.fetch_one(get_query, {"id": new_id})
    return dict(row)

@router.get("/{thesis_id}/opponents", response_model=List[OpponentOut])
async def list_opponents(thesis_id: int):
    await get_thesis(thesis_id)
    query = "SELECT * FROM thesis_official_opponent WHERE thesis_id = :tid ORDER BY order_index"
    rows = await database.fetch_all(query, {"tid": thesis_id})
    return [dict(r) for r in rows]

@router.post("/{thesis_id}/participations", response_model=ParticipationOut, status_code=201)
async def add_participation(thesis_id: int, part: ParticipationCreate):
    await get_thesis(thesis_id)
    query = """
        INSERT INTO thesis_participation (thesis_id, person_id, role, order_index)
        VALUES (:thesis_id, :person_id, :role, :order_index)
        RETURNING id
    """
    values = part.dict()
    values["thesis_id"] = thesis_id
    new_id = await database.execute(query, values)
    get_query = "SELECT * FROM thesis_participation WHERE id = :id"
    row = await database.fetch_one(get_query, {"id": new_id})
    return dict(row)

@router.get("/{thesis_id}/participations", response_model=List[ParticipationOut])
async def list_participations(thesis_id: int):
    await get_thesis(thesis_id)
    query = "SELECT * FROM thesis_participation WHERE thesis_id = :tid"
    rows = await database.fetch_all(query, {"tid": thesis_id})
    return [dict(r) for r in rows]

@router.post("/{thesis_id}/events", response_model=DsEventOut, status_code=201)
async def add_event(thesis_id: int, event: DsEventCreate):
    await get_thesis(thesis_id)
    query = """
        INSERT INTO ds_event (thesis_id, event_type, protocol_number, protocol_date, votes_total, votes_yes, votes_no, votes_abstain,
                              present_offline, present_online)
        VALUES (:thesis_id, :event_type, :protocol_number, :protocol_date, :votes_total, :votes_yes, :votes_no, :votes_abstain,
                :present_offline, :present_online)
        RETURNING id
    """
    values = event.dict()
    values["thesis_id"] = thesis_id
    new_id = await database.execute(query, values)
    get_query = "SELECT * FROM ds_event WHERE id = :id"
    row = await database.fetch_one(get_query, {"id": new_id})
    return dict(row)

@router.get("/{thesis_id}/events", response_model=List[DsEventOut])
async def list_events(thesis_id: int):
    await get_thesis(thesis_id)
    query = "SELECT * FROM ds_event WHERE thesis_id = :tid ORDER BY protocol_date"
    rows = await database.fetch_all(query, {"tid": thesis_id})
    return [dict(r) for r in rows]
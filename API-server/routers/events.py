from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from models import DsEventCreate, DsEventUpdate, DsEventOut

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[DsEventOut])
async def list_events():
    query = "SELECT * FROM ds_event ORDER BY id"
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]

@router.get("/{event_id}", response_model=DsEventOut)
async def get_event(event_id: int):
    query = "SELECT * FROM ds_event WHERE id = :id"
    row = await database.fetch_one(query, {"id": event_id})
    if not row:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return dict(row)

@router.post("/", response_model=DsEventOut, status_code=201)
async def create_event(event: DsEventCreate):
    query = """
        INSERT INTO ds_event (thesis_id, event_type, protocol_number, protocol_date,
                              votes_total, votes_yes, votes_no, votes_abstain,
                              present_offline, present_online)
        VALUES (:thesis_id, :event_type, :protocol_number, :protocol_date,
                :votes_total, :votes_yes, :votes_no, :votes_abstain,
                :present_offline, :present_online)
        RETURNING id
    """
    values = event.dict()
    new_id = await database.execute(query, values)
    return await get_event(new_id)

@router.put("/{event_id}", response_model=DsEventOut)
async def update_event(event_id: int, event: DsEventUpdate):
    await get_event(event_id)
    updates = {k: v for k, v in event.dict().items() if v is not None}
    if not updates:
        return await get_event(event_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE ds_event SET {set_clause} WHERE id = :id"
    values = {**updates, "id": event_id}
    await database.execute(query, values)
    return await get_event(event_id)

@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int):
    await get_event(event_id)
    query = "DELETE FROM ds_event WHERE id = :id"
    await database.execute(query, {"id": event_id})
    return
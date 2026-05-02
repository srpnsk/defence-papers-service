from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from models import ParticipationCreate, ParticipationOut

router = APIRouter(prefix="/participations", tags=["participations"])

@router.get("/", response_model=List[ParticipationOut])
async def list_participations():
    query = "SELECT * FROM thesis_participation ORDER BY id"
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]

@router.get("/{participation_id}", response_model=ParticipationOut)
async def get_participation(participation_id: int):
    query = "SELECT * FROM thesis_participation WHERE id = :id"
    row = await database.fetch_one(query, {"id": participation_id})
    if not row:
        raise HTTPException(status_code=404, detail="Участие не найдено")
    return dict(row)

@router.post("/", response_model=ParticipationOut, status_code=201)
async def create_participation(participation: ParticipationCreate):
    query = """
        INSERT INTO thesis_participation (thesis_id, person_id, role, order_index)
        VALUES (:thesis_id, :person_id, :role, :order_index)
        RETURNING id
    """
    values = participation.dict()
    new_id = await database.execute(query, values)
    return await get_participation(new_id)

@router.delete("/{participation_id}", status_code=204)
async def delete_participation(participation_id: int):
    await get_participation(participation_id)
    query = "DELETE FROM thesis_participation WHERE id = :id"
    await database.execute(query, {"id": participation_id})
    return
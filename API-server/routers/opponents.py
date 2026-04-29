from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from models import OpponentCreate, OpponentOut

router = APIRouter(prefix="/opponents", tags=["opponents"])

@router.get("/", response_model=List[OpponentOut])
async def list_opponents():
    query = "SELECT * FROM thesis_official_opponent ORDER BY id"
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]

@router.get("/{opponent_id}", response_model=OpponentOut)
async def get_opponent(opponent_id: int):
    query = "SELECT * FROM thesis_official_opponent WHERE id = :id"
    row = await database.fetch_one(query, {"id": opponent_id})
    if not row:
        raise HTTPException(status_code=404, detail="Оппонент не найден")
    return dict(row)

@router.post("/", response_model=OpponentOut, status_code=201)
async def create_opponent(opponent: OpponentCreate):
    query = """
        INSERT INTO thesis_official_opponent (thesis_id, person_id, order_index)
        VALUES (:thesis_id, :person_id, :order_index)
        RETURNING id
    """
    values = opponent.dict()
    new_id = await database.execute(query, values)
    return await get_opponent(new_id)

@router.delete("/{opponent_id}", status_code=204)
async def delete_opponent(opponent_id: int):
    await get_opponent(opponent_id)
    query = "DELETE FROM thesis_official_opponent WHERE id = :id"
    await database.execute(query, {"id": opponent_id})
    return
from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import AchievementCreate, AchievementUpdate, AchievementOut

router = APIRouter(prefix="/achievements", tags=["achievements"])

@router.get("/", response_model=List[AchievementOut])
async def list_achievements(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    query = "SELECT * FROM achievement ORDER BY year DESC LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{ach_id}", response_model=AchievementOut)
async def get_achievement(ach_id: int):
    query = "SELECT * FROM achievement WHERE id = :id"
    row = await database.fetch_one(query, {"id": ach_id})
    if not row:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    return dict(row)

@router.post("/", response_model=AchievementOut, status_code=201)
async def create_achievement(ach: AchievementCreate):
    query = """
        INSERT INTO achievement (person_id, type, text_content, year, city_id, quartile)
        VALUES (:person_id, :type, :text_content, :year, :city_id, :quartile)
        RETURNING id
    """
    new_id = await database.execute(query, ach.dict())
    return await get_achievement(new_id)

@router.put("/{ach_id}", response_model=AchievementOut)
async def update_achievement(ach_id: int, ach: AchievementUpdate):
    await get_achievement(ach_id)
    updates = {k: v for k, v in ach.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_achievement(ach_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE achievement SET {set_clause} WHERE id = :id"
    values = {**updates, "id": ach_id}
    await database.execute(query, values)
    return await get_achievement(ach_id)

@router.delete("/{ach_id}", status_code=204)
async def delete_achievement(ach_id: int):
    await get_achievement(ach_id)
    query = "DELETE FROM achievement WHERE id = :id"
    await database.execute(query, {"id": ach_id})
    return
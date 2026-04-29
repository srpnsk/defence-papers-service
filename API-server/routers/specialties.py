from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import SpecialtyCreate, SpecialtyUpdate, SpecialtyOut

router = APIRouter(prefix="/specialties", tags=["specialties"])

@router.get("/", response_model=List[SpecialtyOut])
async def list_specialties(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    query = "SELECT * FROM specialty ORDER BY id LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{spec_id}", response_model=SpecialtyOut)
async def get_specialty(spec_id: int):
    query = "SELECT * FROM specialty WHERE id = :id"
    row = await database.fetch_one(query, {"id": spec_id})
    if not row:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    return dict(row)

@router.post("/", response_model=SpecialtyOut, status_code=201)
async def create_specialty(spec: SpecialtyCreate):
    query = """
        INSERT INTO specialty (code, name)
        VALUES (:code, :name)
        RETURNING id
    """
    new_id = await database.execute(query, spec.dict())
    return await get_specialty(new_id)

@router.put("/{spec_id}", response_model=SpecialtyOut)
async def update_specialty(spec_id: int, spec: SpecialtyUpdate):
    await get_specialty(spec_id)
    updates = {k: v for k, v in spec.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_specialty(spec_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE specialty SET {set_clause} WHERE id = :id"
    values = {**updates, "id": spec_id}
    await database.execute(query, values)
    return await get_specialty(spec_id)

@router.delete("/{spec_id}", status_code=204)
async def delete_specialty(spec_id: int):
    await get_specialty(spec_id)
    query = "DELETE FROM specialty WHERE id = :id"
    await database.execute(query, {"id": spec_id})
    return
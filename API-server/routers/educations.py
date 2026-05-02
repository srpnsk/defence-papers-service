from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import EducationCreate, EducationUpdate, EducationOut

router = APIRouter(prefix="/educations", tags=["educations"])

@router.get("/", response_model=List[EducationOut])
async def list_educations(person_id: int = Query(None), skip: int = 0, limit: int = 100):
    if person_id:
        query = "SELECT * FROM education_history WHERE person_id = :pid ORDER BY end_year DESC LIMIT :limit OFFSET :skip"
        rows = await database.fetch_all(query, {"pid": person_id, "limit": limit, "skip": skip})
    else:
        query = "SELECT * FROM education_history ORDER BY id LIMIT :limit OFFSET :skip"
        rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{edu_id}", response_model=EducationOut)
async def get_education(edu_id: int):
    query = "SELECT * FROM education_history WHERE id = :id"
    row = await database.fetch_one(query, {"id": edu_id})
    if not row:
        raise HTTPException(status_code=404, detail="Запись об образовании не найдена")
    return dict(row)

@router.post("/", response_model=EducationOut, status_code=201)
async def create_education(edu: EducationCreate):
    query = """
        INSERT INTO education_history (person_id, edu_level, end_year, is_honors, qualification, reference_date, organization_id, specialty_id)
        VALUES (:person_id, :edu_level, :end_year, :is_honors, :qualification, :reference_date, :organization_id, :specialty_id)
        RETURNING id
    """
    new_id = await database.execute(query, edu.dict())
    return await get_education(new_id)

@router.put("/{edu_id}", response_model=EducationOut)
async def update_education(edu_id: int, edu: EducationUpdate):
    await get_education(edu_id)
    updates = {k: v for k, v in edu.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_education(edu_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE education_history SET {set_clause} WHERE id = :id"
    values = {**updates, "id": edu_id}
    await database.execute(query, values)
    return await get_education(edu_id)

@router.delete("/{edu_id}", status_code=204)
async def delete_education(edu_id: int):
    await get_education(edu_id)
    query = "DELETE FROM education_history WHERE id = :id"
    await database.execute(query, {"id": edu_id})
    return
from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import EmploymentCreate, EmploymentUpdate, EmploymentOut

router = APIRouter(prefix="/employments", tags=["employments"])

@router.get("/", response_model=List[EmploymentOut])
async def list_employments(person_id: int = Query(None), skip: int = 0, limit: int = 100):
    if person_id:
        query = "SELECT * FROM employment_history WHERE person_id = :pid ORDER BY start_date DESC LIMIT :limit OFFSET :skip"
        rows = await database.fetch_all(query, {"pid": person_id, "limit": limit, "skip": skip})
    else:
        query = "SELECT * FROM employment_history ORDER BY id LIMIT :limit OFFSET :skip"
        rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{emp_id}", response_model=EmploymentOut)
async def get_employment(emp_id: int):
    query = "SELECT * FROM employment_history WHERE id = :id"
    row = await database.fetch_one(query, {"id": emp_id})
    if not row:
        raise HTTPException(status_code=404, detail="Запись о работе не найдена")
    return dict(row)

@router.post("/", response_model=EmploymentOut, status_code=201)
async def create_employment(emp: EmploymentCreate):
    query = """
        INSERT INTO employment_history (person_id, organization_id, position, division, start_date, end_date, is_additional)
        VALUES (:person_id, :organization_id, :position, :division, :start_date, :end_date, :is_additional)
        RETURNING id
    """
    new_id = await database.execute(query, emp.dict())
    return await get_employment(new_id)

@router.put("/{emp_id}", response_model=EmploymentOut)
async def update_employment(emp_id: int, emp: EmploymentUpdate):
    await get_employment(emp_id)
    updates = {k: v for k, v in emp.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_employment(emp_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE employment_history SET {set_clause} WHERE id = :id"
    values = {**updates, "id": emp_id}
    await database.execute(query, values)
    return await get_employment(emp_id)

@router.delete("/{emp_id}", status_code=204)
async def delete_employment(emp_id: int):
    await get_employment(emp_id)
    query = "DELETE FROM employment_history WHERE id = :id"
    await database.execute(query, {"id": emp_id})
    return
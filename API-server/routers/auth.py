# routers/auth.py
from fastapi import APIRouter, Response, Request, HTTPException, Depends
from sqlalchemy import select, insert, delete
from database import database, users, sessions, person
from models import UserRegisterRequest, AuthRequest, UserInfo
import uuid
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])
AUTH_COOKIE = "auth"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


@router.post("/register")
async def register(response: Response, reg_data: UserRegisterRequest):
    query_check = select(users.c.id).where(users.c.email == reg_data.email)
    existing = await database.fetch_one(query_check)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    async with database.transaction():
        person_query = insert(person).values(
            last_name=reg_data.last_name,
            first_name=reg_data.first_name,
            second_name=reg_data.second_name,
            degree=reg_data.degree,
            academic_title=reg_data.academic_title,
            email=reg_data.email,
            phone_number=reg_data.phone_number,
            specialty_id=reg_data.specialty_id
        )
        new_person_id = await database.execute(person_query)

        hashed_pwd = hash_password(reg_data.password)
        user_query = insert(users).values(
            person_id=new_person_id,
            email=reg_data.email,
            hashed_password=hashed_pwd
        )
        new_user_id = await database.execute(user_query)

        session_id = str(uuid.uuid4())
        session_query = insert(sessions).values(
            session_id=session_id,
            user_id=new_user_id
        )
        await database.execute(session_query)

    response.set_cookie(
        key=AUTH_COOKIE,
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"status": "success", "person_id": new_person_id}


@router.post("/login")
async def login(response: Response, auth_request: AuthRequest) -> dict:
    query = select(users.c.id, users.c.hashed_password).where(users.c.email == auth_request.email)
    user = await database.fetch_one(query)

    if not user or not verify_password(auth_request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    session_id = str(uuid.uuid4())
    session_query = insert(sessions).values(session_id=session_id, user_id=user["id"])
    await database.execute(session_query)

    response.set_cookie(
        key=AUTH_COOKIE,
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Успешный вход"}


@router.post("/logout")
async def logout(request: Request, response: Response) -> dict:
    token = request.cookies.get(AUTH_COOKIE)
    if token:
        delete_query = delete(sessions).where(sessions.c.session_id == token)
        await database.execute(delete_query)
        response.delete_cookie(AUTH_COOKIE)
    return {"message": "Успешный выход"}


async def get_current_user(request: Request) -> UserInfo:
    token = request.cookies.get(AUTH_COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")

    query = (
        select(users.c.id, person.c.last_name, person.c.first_name, person.c.second_name)
        .select_from(
            sessions.join(users, sessions.c.user_id == users.c.id)
                    .join(person, users.c.person_id == person.c.id)
        )
        .where(sessions.c.session_id == token)
    )
    user_data = await database.fetch_one(query)
    if not user_data:
        raise HTTPException(status_code=401, detail="Сессия недействительна")

    # Преобразуем Record в dict для безопасного доступа
    user_dict = dict(user_data)

    # Формируем отображаемое имя
    full_name = user_dict.get("last_name", "")
    if user_dict.get("first_name"):
        full_name += f" {user_dict['first_name'][0]}."
        if user_dict.get("second_name"):
            full_name += f" {user_dict['second_name'][0]}."

    return UserInfo(user_id=user_dict["id"], username=full_name)


@router.get("/me")
async def me(user_info: UserInfo = Depends(get_current_user)) -> UserInfo:
    return user_info
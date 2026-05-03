from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy import insert, select
from database import database, users, sessions, person # Импортируем твои таблицы
from models import UserRegisterRequest
import uuid
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])
AUTH_COOKIE = "auth"

# --- Вспомогательные функции хеширования ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

@router.post("/register")
async def register(response: Response, reg_data: UserRegisterRequest):
    # 1. Проверяем, не занят ли email
    query_check = select(users.c.id).where(users.c.email == reg_data.email)
    existing = await database.fetch_one(query_check)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # 2. Начинаем транзакцию, чтобы всё сохранилось вместе
    async with database.transaction():
        # А. Создаем запись в таблице person
        person_query = insert(person).values(
            last_name=reg_data.last_name,
            first_name=reg_data.first_name,
            second_name=reg_data.second_name,
            degree=reg_data.degree,
            academic_title=reg_data.academic_title,
            email=reg_data.email, # Дублируем email в person, если нужно по схеме
            phone_number=reg_data.phone_number,
            specialty_id=reg_data.specialty_id
        )
        new_person_id = await database.execute(person_query)

        # Б. Создаем запись в таблице users
        hashed_pwd = bcrypt.hashpw(reg_data.password.encode(), bcrypt.gensalt()).decode()
        user_query = insert(users).values(
            person_id=new_person_id,
            email=reg_data.email,
            hashed_password=hashed_pwd
        )
        new_user_id = await database.execute(user_query)

        # В. Создаем сессию
        session_id = str(uuid.uuid4()) # Генерируем UUID как строку
        session_query = insert(sessions).values(
            session_id=session_id, 
            user_id=new_user_id
        )
        await database.execute(session_query)

    # 3. Устанавливаем куку
    response.set_cookie(
        key="auth", 
        value=session_id, 
        httponly=True, 
        secure=False, # True для HTTPS
        samesite="lax"
    )
    
    return {"status": "success", "person_id": new_person_id}

@router.post("/login")
async def login(response: Response, auth_request: AuthRequest) -> dict:
    query = select(users.c.id, users.c.hashed_password).where(users.c.username == auth_request.username)
    user = await database.fetch_one(query)
    
    if not user or not verify_password(auth_request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    session_id = str(uuid.uuid4())
    session_query = insert(sessions).values(session_id=session_id, user_id=user["id"])
    await database.execute(session_query)
    
    response.set_cookie(key=AUTH_COOKIE, value=session_id, httponly=True, secure=False, samesite="lax")
    return {"message": "Успешный вход"}

@router.post("/logout")
async def logout(request: Request, response: Response) -> dict:
    token = request.cookies.get(AUTH_COOKIE)
    if token:
        delete_query = delete(sessions).where(sessions.c.session_id == token)
        await database.execute(delete_query)
        response.delete_cookie(AUTH_COOKIE)
    return {"message": "Успешный выход"}

# Зависимость для получения текущего пользователя
async def get_current_user(request: Request) -> UserInfo:
    token = request.cookies.get(AUTH_COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")
        
    query = select(users.c.id, users.c.username).select_from(
        sessions.join(users, sessions.c.user_id == users.c.id)
    ).where(sessions.c.session_id == token)
    
    user_data = await database.fetch_one(query)
    if not user_data:
        raise HTTPException(status_code=401, detail="Сессия недействительна")
        
    return UserInfo(user_id=user_data["id"], username=user_data["username"])

@router.get("/me")
async def me(user_info: UserInfo = Depends(get_current_user)) -> UserInfo:
    return user_info

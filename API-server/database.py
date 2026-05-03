import databases
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, String, ForeignKey

DATABASE_URL = "postgresql+psycopg://postgres:post@localhost:9543/disser"

database = databases.Database(DATABASE_URL)
metadata = MetaData()

person = Table(
    "person",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("last_name", String(64), nullable=False),
    Column("first_name", String(64), nullable=False),
    Column("second_name", String(64)),
    Column("degree", String(128)),
    Column("academic_title", String(128)),
    Column("email", String(128), unique=True),
    Column("phone_number", String(64)),
    Column("specialty_id", BigInteger, ForeignKey("specialty.id"))
)

users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("person_id", BigInteger, ForeignKey("person.id"), nullable=False),
    Column("email", String(128), nullable=False, unique=True),
    Column("hashed_password", String(255), nullable=False), # Используй String для bcrypt!
)

sessions = Table(
    "sessions",
    metadata,
    Column("session_id", UUID, primary_key=True), # Храним UUID как строку для простоты
    Column("user_id", BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
)

engine = create_engine(DATABASE_URL)

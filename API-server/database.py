import databases
# import sqlalchemy
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql+psycopg://postgres:post@localhost:9543/disser"

database = databases.Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)

# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql://xrayanalizerdb_user:JQI4kUBPd2yLGqIziDyzfe0lJIu1Yn8C"
    "@dpg-d0r0q3idbo4c73el0bv0-a.oregon-postgres.render.com/xrayanalizerdb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DBSettings, lg


engine = create_engine(DBSettings.SQLALCHEMY_DATA_BASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    try:
        db = Session()
        yield db

    except Exception as error:
        lg.error(f"Error while trying get db ->: {error}")
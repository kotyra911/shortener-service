from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from app.config import DBSettings, lg


engine = create_async_engine(DBSettings.SQLALCHEMY_DATA_BASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db

        except Exception as error:
            lg.error(f"Error while trying get db ->: {error}")
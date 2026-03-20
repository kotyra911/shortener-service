from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Link


class LinksRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_link(self, original_link: str, short_link: str, clicks: int):

        stmt = (
            insert(Link)
            .values(original_link=original_link, short_link=short_link, clicks=clicks)
        )
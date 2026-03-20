from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Link
from app.config import lg


class LinksRepository:

    # Get session
    def __init__(self, db: AsyncSession):
        self.db = db

    # Add new link
    async def add_link(self, original_link: str, short_link: str, clicks: int):

        stmt = (
            insert(Link)
            .values(original_link=original_link, short_link=short_link, clicks=clicks)
        )

        try:
            await self.db.execute(stmt)

        except Exception as error:
            lg.error(f"Error while trying to insert link ->:{error}")

    # Get redirect link by short
    async def get_redirect_link(self, short_link: str):

        stmt = (
            select(Link.original_link)
            .where(Link.short_link == short_link)
        )

        result = await self.db.execute(stmt)
        redirect_link = result.scalar_one()
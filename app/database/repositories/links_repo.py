from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Link
from app.config import lg


class LinksRepository:

    # Get session
    def __init__(self, db: AsyncSession):
        self.db = db

    # Add new link
    async def add_link(self, original_link: str, short_link: str, clicks: int) -> None:

        stmt = (
            insert(Link)
            .values(original_link=original_link, short_link=short_link, clicks=clicks)
        )

        try:
            await self.db.execute(stmt)
            await self.db.commit()

        except Exception as error:
            lg.error(f"Error while trying to insert link ->:{error}")
            await self.db.rollback()

    # Get redirect link by short
    async def get_redirect_link(self, short_link: str) -> str:

        stmt = (
            select(Link.original_link)
            .where(Link.short_link == short_link)
        )
        try:
            result = await self.db.execute(stmt)
            redirect_link = result.scalar_one()

            return redirect_link

        except Exception as error:

            lg.error(f"Error while trying to get redirect link ->:{error}")
            await self.db.rollback()
            return ""

    # Increases the number of clicks by 1
    async def increase_click(self, short_link: str) -> None:

        stmt = (
            update(Link)
            .where(Link.short_link == short_link)
            .values(clicks=Link.clicks + 1)
        )

        try:
            await self.db.execute(stmt)
            await self.db.commit()

        except Exception as error:
            lg.error(f"Error while trying to update clicks ->:{error}")
            await self.db.rollback()

    # Get clicks number
    async def  get_link_stats(self, short_link: str) -> int:
        stmt = (
            select(Link.clicks)
            .where(Link.short_link == short_link)
        )

        try:
            result = await self.db.execute(stmt)
            clicks = result.scalar_one()
            return clicks

        except Exception as error:
            lg.error(f"Error while trying to get clicks ->:{error}")
            await self.db.rollback()
            return 0
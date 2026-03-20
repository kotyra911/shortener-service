from app.database.connection import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import BASE_URL
from app.schemas.schemas import ShortenLinkResponse, ShortenLink


router = APIRouter()

@router.post("/shorten", response_model=ShortenLinkResponse)
async def shorten_link(link: ShortenLink, db: AsyncSession = Depends(get_db)):
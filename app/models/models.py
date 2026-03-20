from base import Base
from sqlalchemy import Column, Integer, String, Text, BigInteger


class Link(Base):
    __tablename__ = 'links'

    link_id = Column(Integer, primary_key=True, index=True) #pk
    original_link = Column(Text, nullable=False)
    short_link = Column(String(10), unique=True, nullable=False)
    clicks = Column(BigInteger, default=0)

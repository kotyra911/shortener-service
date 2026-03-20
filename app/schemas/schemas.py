from pydantic import BaseModel


class ShortenLinkResponse(BaseModel):
    short_link: str

class ShortenLink(BaseModel):

    original_link: str
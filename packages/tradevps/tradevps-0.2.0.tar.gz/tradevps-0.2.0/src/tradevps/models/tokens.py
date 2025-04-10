from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, UUID4, Field

class APIToken(BaseModel):
    id: int
    tokenable_type: str
    tokenable_id: UUID4
    name: str
    abilities: List[str]
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class PaginationInfo(BaseModel):
    current_page: int
    last_page: int
    per_page: int
    total: int
    first_page_url: str
    from_: Optional[int] = Field(None, alias="from")
    last_page_url: str
    next_page_url: Optional[str]
    prev_page_url: Optional[str]

class APITokenList(BaseModel):
    data: List[APIToken]
    pagination: PaginationInfo

class APITokenResponse(BaseModel):
    token: str
    name: str


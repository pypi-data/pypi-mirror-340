from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field

class Notification(BaseModel):
    id: UUID
    type: str
    notifiable_type: Optional[str] = None
    notifiable_id: str
    notifiable_model: Optional[str] = None
    data: Dict
    read_at: Optional[datetime]
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

class NotificationList(BaseModel):
    data: List[Notification]
    pagination: PaginationInfo





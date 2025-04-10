from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4

class Profile(BaseModel):
    id: UUID4
    name: str
    email: str
    email_verified_at: Optional[datetime]
    plan: int
    status: int
    plan_expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    referrer_id: Optional[UUID4]
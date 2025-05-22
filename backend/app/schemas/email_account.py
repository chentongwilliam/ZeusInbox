from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailAccountBase(BaseModel):
    email: EmailStr
    imap_server: str
    imap_port: int
    username: str
    password: str

class EmailAccountCreate(EmailAccountBase):
    pass

class EmailAccountUpdate(BaseModel):
    email: Optional[EmailStr] = None
    imap_server: Optional[str] = None
    imap_port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class EmailAccount(EmailAccountBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 
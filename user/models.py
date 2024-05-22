from pydantic import BaseModel

from typing import Optional

from datetime import datetime

class User(BaseModel):
    email: str
    username: Optional[str] = None
    password: str
    is_active: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now()
    update_at: Optional[datetime] = datetime.now()

    class Config:
        from_attributes = True



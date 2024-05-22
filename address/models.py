from pydantic import BaseModel
from datetime import datetime

from typing import Optional

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    longitude: float  
    latitude: float
    created_at: datetime = datetime.now()
    update_at: datetime = datetime.now()
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True
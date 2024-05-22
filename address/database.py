from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    DateTime, 
    Float
)
from sqlalchemy.orm import relationship

from datetime import datetime

from ab_app.database import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip_code = Column(String, index=True)
    country = Column(String, index=True)
    longitude = Column(Float, index=True)  
    latitude = Column(Float, index=True)
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="addresses")


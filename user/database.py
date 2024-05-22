from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy_utils import EmailType, PasswordType

from datetime import datetime

from ab_app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

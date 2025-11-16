from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    TECHNICIAN = "technician"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.TECHNICIAN)
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
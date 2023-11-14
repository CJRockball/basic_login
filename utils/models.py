from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass


class RegisteredUsers(Base):
    __tablename__ = 'registered_users'
    
    id = Column(Integer(), autoincrement=True, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(500), nullable=False, unique=True)
    #admin = Column(Boolean, unique=False, default=False)
    #created_on = Column(DateTime(timezone=False), default=datetime.now())
    #updated_on = Column(DateTime(timezone=False), default=datetime.now())
    
    def dict_out(self):
        return {'username': self.username,
                'password': self.password}







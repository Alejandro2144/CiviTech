from sqlalchemy import Column, Integer, String
from config.db import Base

class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    civi_email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

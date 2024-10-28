# models.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime



Base = declarative_base()

# this function has the function to manage the table
class URL(Base):
    __tablename__ = "urls"

    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

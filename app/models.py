from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column (String, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    summary = Column(String)
    word_count = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

from app import db
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text


class Post(db.Model):

    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    author = Column(String(64), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


from app import db
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


class Post(db.Model):

    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts", cascade="all, delete")
    messages = relationship("Message", back_populates="post", cascade="all, delete")


class Message(db.Model):

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages", cascade="all, delete")
    post = relationship("Post", back_populates="messages", cascade="all, delete")
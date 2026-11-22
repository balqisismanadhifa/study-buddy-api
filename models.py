from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(Text)
    major = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    subject = Column(String)
    sub_topic = Column(String)
    description = Column(Text)
    max_members = Column(Integer)
    current_members = Column(Integer, default=1)
    status = Column(String, default="open")
    created_at = Column(DateTime, server_default=func.now())

class PostMember(Base):
    __tablename__ = "post_members"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, server_default=func.now())
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(32),unique=True, index=True)
    hashed_password = Column(String(32))
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True,index=True)
    content = Column(String(256))
    send_time = Column(DateTime, default=datetime.datetime.utcnow)
    sender_id = Column(Integer, ForeignKey(User.id),nullable=False)
    target_chat_id = Column(Integer, ForeignKey(Chat.id),nullable=False)


class MessageReadedBy(Base):
    __tablename__ = "messages_readed_by"

    message_id = Column(Integer, ForeignKey(Message.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)

class ChatMembership(Base):
    __tablename__ = "chat_memeberships"

    chat_id = Column(Integer, ForeignKey(Chat.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)


Base.metadata.create_all(bind=engine, checkfirst=True)
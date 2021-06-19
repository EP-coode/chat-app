import datetime
import hashlib
import os

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# ========= database connection =========
db_user = os.getenv("db_user", "root")
db_password = os.getenv("db_password", "example")
db_host = os.getenv("db_host", "127.0.0.1")
db_port = os.getenv("db_port", "3306")

engine = create_engine("mysql+pymysql://{}:{}@{}:{}".format(
    db_user, db_password, db_host, db_port
))

engine.execute(r"CREATE DATABASE IF NOT EXISTS messenger")
engine.execute(r"USE messenger")

DB_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ========= database models ============
Base = declarative_base()
Base.query = scoped_session(DB_Session).query_property()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(32))
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.hashed_password = hashlib.md5(password.encode()).hexdigest()


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    creator = Column(Integer, ForeignKey(User.id))
    messages = relationship("Message")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256))
    send_time = Column(DateTime, default=datetime.datetime.utcnow)
    sender_id = Column(Integer, ForeignKey(User.id), nullable=False)
    target_chat_id = Column(Integer, ForeignKey(Chat.id), nullable=False)


class MessageReadedBy(Base):
    __tablename__ = "messages_readed_by"

    message_id = Column(Integer, ForeignKey(Message.id),
                        nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id),
                     nullable=False, primary_key=True)


class ChatMembership(Base):
    __tablename__ = "chat_memeberships"

    chat_id = Column(Integer, ForeignKey(Chat.id),
                     nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id),
                     nullable=False, primary_key=True)


# temporary sollution for problem with not adding "IF NOT EXISTS" to sql executed by DB
try:
    Base.metadata.create_all(bind=engine)
except:
    pass

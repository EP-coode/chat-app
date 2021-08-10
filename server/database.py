import datetime
import enum
import hashlib
import os
from flask.helpers import send_file

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Enum, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# ========= database connection =========
db_user = os.getenv("db_user", "root")
db_password = os.getenv("db_password", "example")
db_host = os.getenv("db_host", "127.0.0.1")
db_port = os.getenv("db_port", "3306")
db_name = os.getenv('db_name', 'messenger')

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(
    db_user, db_password, db_host, db_port, db_name
))

# trzeba to zmienić
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
    name = Column(String(32))
    creator = Column(Integer, ForeignKey(User.id))
    personal = Column(Boolean, default=False)
    messages = relationship("Message")
    members = relationship(
        "ChatMembership", primaryjoin="Chat.id==ChatMembership.chat_id", cascade="all, delete")

    def __init__(self, creator_id: int, name: str, personal: bool = False) -> None:
        self.name = name
        self.creator = creator_id
        self.personal = personal


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256))
    send_time = Column(DateTime, default=datetime.datetime.utcnow)
    sender_id = Column(Integer, ForeignKey(User.id), nullable=False)
    target_chat_id = Column(Integer, ForeignKey(Chat.id), nullable=False)

    def __init__(self, creator: User, content: str, target: Chat):
        self.content = content
        self.sender_id = creator.id
        self.target_chat_id = target.id


class MessageReadedBy(Base):
    __tablename__ = "messages_readed_by"

    message_id = Column(Integer, ForeignKey(Message.id),
                        nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id),
                     nullable=False, primary_key=True)

    def __init__(self,user_id: int, msg_id: int) -> None:
        self.message_id = msg_id
        self.user_id = user_id


class ChatMembership(Base):
    __tablename__ = "chat_memeberships"

    chat_id = Column(Integer, ForeignKey(Chat.id),
                     nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id),
                     nullable=False, primary_key=True)

    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id


class Friendships(Base):
    __tablename__ = "friendships"

    user_1 = Column(Integer, ForeignKey(User.id),
                    nullable=False, primary_key=True)
    user_2 = Column(Integer, ForeignKey(User.id),
                    nullable=False, primary_key=True)


class InvitationStatus(enum.Enum):
    pending = 1
    rejected = 2
    accepted = 3


class Invitation(Base):
    __tablename__ = "invitations"

    creator_user = Column(Integer, ForeignKey(User.id),
                          nullable=False, primary_key=True)
    target_user = Column(Integer, ForeignKey(User.id),
                         nullable=False, primary_key=True)
    status = Column(Enum(InvitationStatus), default=False)

    def __init__(self, creator_user_ID: int, target_user_ID: int):
        self.creator_user = creator_user_ID
        self.target_user = target_user_ID
        self.status = InvitationStatus.pending


# temporary sollution for problem with not adding "IF NOT EXISTS" to sql executed by DB
try:
    Base.metadata.create_all(bind=engine)
except:
    pass

from typing import List
from sqlalchemy.orm import Session, session

from database import DB_Session, User, Chat, Message, Chat


def loginUser(login: str, password: str) -> User:
    session: Session = DB_Session()
    user = User(login=login, password=password)
    try:
        found_usr: User = session.query(User).filter(
            User.login == user.login).first()
    except:
        return None
    finally:
        session.close()

    if not found_usr:
        return None

    if not user.hashed_password == found_usr.hashed_password:
        return None

    return found_usr


def isLoginAvalible(login: str) -> bool:
    session: Session = DB_Session()
    try:
        found_usr: User = session.query(User).filter(
            User.login == login).first()
    except:
        return False
    finally:
        session.close()

    return not found_usr


def registerUser(login: str, password: str) -> User:
    session: Session = DB_Session()
    user = User(login=login, password=password)
    try:
        session.add(user)
        session.commit()
    except:
        session.rollback()
        return None
    finally:
        session.close()

    return user


def getUserById(id: int) -> User:
    session: Session = DB_Session()
    try:
        user: User = session.query(User).filter(User.id == id).first()
    except:
        session.rollback()
        return None
    finally:
        session.close()

    return user


def getChatById(id: int) -> Chat:
    session: Session = DB_Session()
    try:
        chat: Chat = session.query(Chat).filter(Chat.id == id).first()
    except:
        session.rollback()
        return None
    finally:
        session.close()

    return chat


def sendMessage(message: Message) -> bool:
    session: Session = DB_Session()
    try:
        session.add(message)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()

    return True


def addChat(chat: Chat):
    session: Session = DB_Session()
    try:
        session.add(chat)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()

    return True


def getChatList():
    session: Session = DB_Session()
    try:
        chatlist = session.query(Chat).all()
    except:
        return None
    finally:
        session.close()

    return chatlist

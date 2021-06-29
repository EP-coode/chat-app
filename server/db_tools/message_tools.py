from os import stat
from sqlalchemy.orm import Session, session

from database import DB_Session, Chat, Message, Chat, User, MessageReadedBy


def getChatMessages(chat_id):
    session: Session = DB_Session()
    try:
        chat: Chat = session.query(Chat).filter(
            Chat.id == chat_id).first()
        return chat.messages
    except:
        return False
    finally:
        session.close()


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


def isMesssageReaded(message_id: int, user_id: int, session: Session = DB_Session()):
    try:
        message: Message = session.query(Message).filter(Message.id == message_id).first()
        if message.sender_id == user_id:
            return True
            
        status = session.query(MessageReadedBy).filter(MessageReadedBy.message_id == message_id, MessageReadedBy.user_id == user_id).first()
    except:
        return False
    finally:
        session.close()

    return bool(status)


def markAsReaded(messsage_id: int, user_id: int):
    session: Session = DB_Session()
    try:
        message: Message = session.query(Message).filter(
            Message.id == messsage_id).first()

        chat: Chat = session.query(Chat).filter(
            Chat.id == message.target_chat_id, Chat.members.any(User.id == user_id)).first()

        if chat:
            status = MessageReadedBy(user_id, messsage_id)
            session.add(status)
            session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()

    return True

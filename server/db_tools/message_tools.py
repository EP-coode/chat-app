from sqlalchemy.orm import Session

from database import DB_Session, Chat, Message, Chat


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

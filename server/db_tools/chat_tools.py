from sqlalchemy.orm import Session

from database import DB_Session, User, Chat, Chat, ChatMembership


def getChatById(id: int) -> Chat:
    session: Session = DB_Session()
    try:
        chat: Chat = session.query(Chat).filter(Chat.id == id).first()
    except:
        return None
    finally:
        session.close()

    return chat


def isMemberOfChat(chat_id: int, user_id: int) -> bool:
    session: Session = DB_Session()
    try:
        chat: Chat = session.query(Chat).filter(
            Chat.id == chat_id, Chat.members.any(User.id == user_id)).first()
        return bool(chat)
    except:
        return False
    finally:
        session.close()


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


def getChatList(user_id: int):
    session: Session = DB_Session()
    try:
        chat_ids = session.query(ChatMembership).filter(
            ChatMembership.user_id == user_id).all()
        chat_ids = [chat_id.chat_id for chat_id in chat_ids]
        chatlist = session.query(Chat).filter(
            Chat.id.in_(chat_ids)).all()

        for chat in chatlist:
            if chat.personal:

                other_member = session.query(ChatMembership).filter(
                    ChatMembership.chat_id == chat.id, ChatMembership.user_id != user_id).first()
                other_member = session.query(User).filter(
                    User.id == other_member.user_id).first()

                if other_member:
                    chat.name = other_member.login
    except:
        return None
    finally:
        session.close()

    return chatlist

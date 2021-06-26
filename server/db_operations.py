from sqlalchemy.orm import Session

from database import DB_Session, User, Chat, Message, Chat, Invitation, ChatMembership, InvitationStatus


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
        return None
    finally:
        session.close()

    return chat


def isMemberOfChat(chat_id: int, user_id: int) -> bool:
    session: Session = DB_Session()
    try:
        chat: Chat = session.query(Chat).filter(Chat.id == chat_id, Chat.members.any(User.id == user_id)).first()
        return bool(chat)
    except:
        return False
    finally:
        session.close()


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


def getInvitations(userId: int) -> Invitation:
    session: Session = DB_Session()
    try:
        invitations = session.query(Invitation).filter(
            Invitation.target_user == userId).all()
    except:
        return None
    finally:
        session.close()

    return invitations


def addInvitation(creatorId: int, targetId: int) -> bool:
    session: Session = DB_Session()
    try:
        inv = Invitation(creator_user_ID=creatorId, target_user_ID=targetId)
        session.add(inv)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()

    return True


def acceptInvitation(creator_id: int, target_id: int) -> bool:
    session: Session = DB_Session()
    try:
        invitation: Invitation = session.query(Invitation).filter(
            Invitation.target_user == target_id, Invitation.creator_user == creator_id).first()

        if not invitation.status == InvitationStatus.pending:
            return False

        invitation.status = InvitationStatus.accepted

        personal_chat = Chat(None, None, personal=True)
        session.add(personal_chat)
        session.commit()

        mem1 = ChatMembership(chat_id=personal_chat.id,
                              user_id=invitation.creator_user)
        mem2 = ChatMembership(chat_id=personal_chat.id,
                              user_id=invitation.target_user)

        session.add(mem1)
        session.add(mem2)

        session.commit()
    except:
        return False
    finally:
        session.close()

    return True

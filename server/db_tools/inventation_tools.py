from sqlalchemy.orm import Session

from database import DB_Session, Chat, Chat, Invitation, ChatMembership, InvitationStatus


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

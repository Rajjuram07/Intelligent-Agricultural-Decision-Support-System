from sqlalchemy.orm import sessionmaker

from database.db import engine

from database.models import ChatHistory


SessionLocal = sessionmaker(
    bind=engine
)


# SAVE MESSAGE
def save_message(role, message):

    session = SessionLocal()

    chat = ChatHistory(
        role=role,
        message=message
    )

    session.add(chat)

    session.commit()

    session.close()


# LOAD CHAT HISTORY
def load_chat_history():

    session = SessionLocal()

    chats = session.query(
        ChatHistory
    ).all()

    session.close()

    return chats


# ANALYTICS
def get_chat_statistics():

    session = SessionLocal()

    total_messages = session.query(
        ChatHistory
    ).count()

    total_user_queries = session.query(
        ChatHistory
    ).filter(
        ChatHistory.role == "user"
    ).count()

    total_ai_responses = session.query(
        ChatHistory
    ).filter(
        ChatHistory.role == "assistant"
    ).count()

    latest_chat = session.query(
        ChatHistory
    ).order_by(
        ChatHistory.created_at.desc()
    ).first()

    session.close()

    return {
        "total_messages": total_messages,
        "total_user_queries": total_user_queries,
        "total_ai_responses": total_ai_responses,
        "latest_chat": latest_chat
    }

def clear_chat_history():

    session = SessionLocal()

    session.query(
        ChatHistory
    ).delete()

    session.commit()

    session.close() 
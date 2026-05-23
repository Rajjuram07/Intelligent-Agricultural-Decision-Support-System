from sqlalchemy.orm import sessionmaker

from database.db import engine

from database.models import (
    ChatHistory,
    ActivityHistory
)

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

# =========================================================
# SAVE ACTIVITY
# =========================================================
def save_activity(

    module,

    query,

    response,

    retrieval_engine,

    language,

    ai_temperature
):

    session = SessionLocal()

    activity = ActivityHistory(

        module=module,

        query=query,

        response=response,

        retrieval_engine=retrieval_engine,

        language=language,

        ai_temperature=ai_temperature
    )

    session.add(activity)

    session.commit()

    session.close()


# =========================================================
# LOAD ACTIVITIES
# =========================================================
def load_activities():

    session = SessionLocal()

    activities = session.query(

        ActivityHistory

    ).order_by(

        ActivityHistory.created_at.desc()

    ).all()

    session.close()

    return activities


# =========================================================
# DELETE ACTIVITY
# =========================================================
def delete_activity(activity_id):

    session = SessionLocal()

    activity = session.query(

        ActivityHistory

    ).filter(

        ActivityHistory.id == activity_id

    ).first()

    if activity:

        session.delete(activity)

        session.commit()

    session.close()
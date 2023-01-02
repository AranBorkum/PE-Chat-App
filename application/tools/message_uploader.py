from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config
from db.messages import Message
from db.user import User

DB_URI = Config.DB_URI


def upload_message(user, message):
    with Session(create_engine(DB_URI)) as session:
        user = session.query(User).filter(User.username == user).first()
        new_message = Message(message=message, send_user=user)
        session.add(new_message)
        session.commit()

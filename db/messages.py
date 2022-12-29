from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref

from db.base import Base
from db.user import User


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    send_user_id = Column(Integer, ForeignKey(User.id))
    send_user = relationship(User, backref=backref("messages"))
    time_sent = Column(DateTime(timezone=True), server_default=func.now())

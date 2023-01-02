from typing import Any

from flask_login import UserMixin
from sqlalchemy import Column, Date, DateTime, Integer, String, func
from werkzeug.security import check_password_hash, generate_password_hash

from db.base import Base

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"


class User(UserMixin, Base):

    __tablename__ = "main_users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email_address = Column(String)
    date_of_birth = Column(Date)
    password = Column(String)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(
        self,
        username,
        email_address,
        date_of_birth,
        password,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.username = username
        self.email_address = email_address
        self.date_of_birth = date_of_birth
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.email_address}>"

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_user_by_email_address(session, email_address):
        users = session.query(User).filter(User.email_address == email_address)
        return users.first()

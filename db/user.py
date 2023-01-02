from typing import Any

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from db.base import Base

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"


class User(UserMixin, Base):

    __tablename__ = "main_users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, nullable=False)
    email_address = sa.Column(sa.String)
    date_of_birth = sa.Column(sa.Date)
    password = sa.Column(sa.String)
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

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

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.user import User


def login_procedure(form, db_uri):
    email_address = form.get("inputName")
    password = form.get("password")

    if not email_address:
        return None, "Please enter a valid email address"

    if not password:
        return None, "Please enter a valid password"

    with Session(create_engine(db_uri)) as session:
        user = User.get_user_by_email_address(session, email_address)

        if not user:
            return None, "Invalid username or password."

        if not user.verify_password(password):
            return None, "Invalid username or password."

        return user, ""

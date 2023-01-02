from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.user import User


def create_new_user(form, db_uri):
    username = form.get("inputName")
    email_address = form.get("email address")
    date_of_birth = form.get("Date of birth")
    password = form.get("password")
    password2 = form.get("password2")

    with Session(create_engine(db_uri)) as session:
        if not username:
            return False, "Please provide a username."

        if session.query(User).filter(User.username == username).count():
            return False, "Username already in use."

        if not email_address:
            return False, "Please provide an email address."

        if User.get_user_by_email_address(session, email_address).count():
            return False, "Email address already in use."

        if not date_of_birth:
            return False, "Please provide a date of birth."

        if len(password) < 7:
            return False, "Password needs to be at least 8 characters long."

        if password2 != password:
            return False, "Passwords don't match."

        new_user = User(
            username=username,
            email_address=email_address,
            date_of_birth=datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
            password=password,
        )

        session.add(new_user)
        session.commit()
        return True, "Account created!"

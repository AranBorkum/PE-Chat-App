import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from application.tools.login_tools import login_procedure
from application.tools.registration_tools import create_new_user
from db.messages import Message

view = Blueprint("views", __name__)
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
LOGIN_TIME = datetime.timedelta(hours=1)


@view.route("/")
def home():
    print(current_user, current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for("views.chat"))
    else:
        return redirect(url_for("views.login"))


@view.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        print(request.form)
    return render_template("chat.html", **{"history": get_history()})


@view.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("views.chat"))

    if request.method == "POST":
        user, message = login_procedure(request.form, DB_URI)

        if user is not None:
            login_user(user, remember=True, duration=LOGIN_TIME)
            flash("Logged in successfully.")
            return redirect(url_for("views.chat"))

    return render_template("login.html")


@view.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form:
            result, message = create_new_user(request.form, DB_URI)
            flash(message)

            if result:
                return redirect(url_for("views.chat"))

    return render_template("register.html")


@view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@view.route("/get_history")
def get_history(n_messages=100):
    with Session(create_engine(DB_URI)) as sql_session:
        return [
            (i.send_user.username, i.message)
            for i in sql_session.query(Message)
            .order_by(Message.time_sent)
            .limit(n_messages)
        ]

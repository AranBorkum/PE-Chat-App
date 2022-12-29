import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, LoginManager, login_manager, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from application.tools.login_tools import login_procedure
from application.tools.registration_tools import create_new_user
from config import get_values
from db.user import User

view = Blueprint("views", __name__)
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"


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
        message = request.form.get("message")
        user = request.form.get("username")
        print(message, user)
        # upload_message(user, message[1:])

    return render_template("chat.html")


@view.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("views.chat"))

    if request.method == "POST":
        user, message = login_procedure(request.form, DB_URI)

        if user is not None:
            login_user(user, remember=True, duration=datetime.timedelta(hours=1))
            flash("Logged in successfully.")
            return redirect(url_for("views.chat"))

    return render_template("login.html")


@view.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form:
            result, message = create_new_user(request.form, DB_URI)
            flash(message)

            if result:
                return redirect(url_for("views.chat"))

    return render_template("register.html")


@view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

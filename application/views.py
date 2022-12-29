from flask import Blueprint, render_template, request

view = Blueprint("views", __name__)


@view.route("/")
def index():
    return render_template("index.html")


@view.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")
    # if request.method == "POST":
    #
    #     user, message = login_procedure(request.form, DB_URI)
    #
    #     if user is not None:
    #         login_user(user, remember=True, duration=datetime.timedelta(hours=1))
    #         flash("Logged in successfully.")
    #         return redirect(url_for("chat"))


@view.route('/register', methods=["GET", "POST"])
def register():
    return render_template("register.html")
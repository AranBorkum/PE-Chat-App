from flask import Flask, render_template
from flask_socketio import SocketIO, send

from application import create_app

# app = Flask(__name__)
# app.config["SECRET"] = "secret_key"
# socketio = SocketIO(app, cors_allowed_origins="*")
#
#
# @socketio.on("message")
# def handle_message(message):
#     print(f"Received message: {message}")
#     if message != "User connected!":
#         send(message, broadcast=True)
#
#
# @app.route("/")
# def index():
#     return render_template("index.html")


app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}")
    if message != "User connected!":
        send(message, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, allow_unsafe_werkzeug=True)
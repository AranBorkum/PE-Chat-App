from flask_socketio import SocketIO, send
from application import create_app
from application.tools.message_uploader import upload_message

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(message) -> None:
    """
    socketio event hook for broadcasting messages to users on the server
    and upload the messages to the database.
    :param message: The message string sent by a given user.
    :return: None
    """
    print(f"Received message: {message}")
    if message != "User connected!":
        send(message, broadcast=True)
        user, message = message.split(":")
        upload_message(user, message[1:])

    socketio.emit("message response:", message)


if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, allow_unsafe_werkzeug=True)

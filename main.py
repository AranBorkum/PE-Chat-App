from flask_socketio import SocketIO, send
from application import create_app
from application.tools.message_uploader import upload_message

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}")
    if message != "User connected!":
        send(message, broadcast=True)


    socketio.emit('message response:', message)


if __name__ == "__main__":
    socketio.run(app, host="192.168.0.2", debug=True, allow_unsafe_werkzeug=True)

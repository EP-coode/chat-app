import datetime
import hashlib
import os

from flask import Flask, request
from sqlalchemy.orm.session import Session
import jwt

from database import Chat, Message, User, DB_Session
from db_operations import getChatById, isLoginAvalible, loginUser, registerUser, getUserById, sendMessage, addChat, getChatList
from decorators import require_token

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    "TOKEN_SECRET", "yoursuperstrongpassword123")


@app.route('/ping', methods=['GET'])
def pong():
    return 'pong', 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not 'login' in data or not 'password' in data:
        return 'Bad request', 400

    if not isLoginAvalible(data['login']):
        return 'User with this login already exist', 409

    registerUser(data['login'], data['password'])

    return 'Account created', 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not 'login' in data or not 'password' in data:
        return 'Bad request', 400

    user = loginUser(data['login'], data['password'])
    if not user:
        return 'Password or login is worong', 403

    token = jwt.encode({
        'id': user.id,
        'user': user.login,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'])

    return {"token": token}, 200


@app.route('/chat', methods=['POST', 'GET'])
@require_token
def room(token_payload):
    if request.method == 'POST':
        data = request.get_json()
        name = data['name'] if 'name' in data else "default name"
        user = getUserById(token_payload['id'])
        chat = Chat(user, name)
        addChat(chat)
        return 'chat created', 201

    if request.method == 'GET':
        chatlist = getChatList()
        chatlist = list(map(Chat.to_dict, chatlist))
        return {'chatlist': chatlist}, 200


@app.route('/message', methods=['POST'])
@require_token
def message(token_payload):
    data = request.get_json()

    if not 'target' in data or not 'content' in data:
        return 'Bad request', 400

    user = getUserById(token_payload['id'])
    target_chat = getChatById(data['target'])

    if not user:
        return 'Bad request', 400

    if not target_chat:
        return 'Target chat not found', 404  # change this error code

    message = Message(user, data['content'], target_chat)

    if sendMessage(message):
        return 'succes', 201
    return 'fail', 400  # change this eerror code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

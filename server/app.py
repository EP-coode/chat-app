import datetime
import os

from flask import Flask, request
import jwt

from database import Message
from db_operations import *
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
    # if request.method == 'POST':
    #     data = request.get_json()
    #     name = data['name'] if 'name' in data else "default name"
    #     user: User = getUserById(token_payload['id'])
    #     chat = Chat(user.id, name)
    #     addChat(chat)
    #     return 'chat created', 201

    if request.method == 'GET':
        chatlist = getChatList(token_payload['id'])
        chatlist = list(
            map(lambda inv: {'id': inv.id, 'name': inv.name, 'inv': inv.creator}, chatlist))
        return {'chatlist': chatlist}, 200


@app.route('/message', methods=['POST', 'GET'])
@require_token
def message(token_payload):
    if request.method == 'POST':
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

    if request.method == 'GET':
        data = request.get_json()

        if not 'chat_id' in data:
            return 'Bad request', 400

        chat: Chat = getChatById(data['chat_id'])

        if not isMemberOfChat(chat.id, token_payload['id']):
            return 'you are not member of this chat', 403

        messages = getChatMessages(chat.id)

        messages = list(
            map(Message.to_dict, messages))
        return {'messages': messages}, 500


@app.route('/invitate', methods=['GET', 'POST'])
@require_token
def invitate(token_payload):
    if request.method == 'GET':
        invitations = getInvitations(token_payload['id'])
        invitations = list(
            map(lambda inv: {'user_id': inv.creator_user, 'status': inv.status.name}, invitations))

        return {'invitations': invitations}, 200

    if request.method == 'POST':
        data = request.get_json()

        if 'user_id' not in data:
            return 'Bad request', 400

        inv_user_id = data['user_id']

        if inv_user_id == token_payload['id']:
            return 'Can not invite yourself', 400

        if addInvitation(token_payload['id'], inv_user_id):
            return 'invitation created', 201

        return 'fail', 400


@app.route('/accept_invitation',  methods=['POST'])
@require_token
def acceptInv(token_payload):
    data = request.get_json()

    if 'user_id' not in data:
        return 'Bad request', 400
    inv_user_id = data['user_id']

    if acceptInvitation(inv_user_id, token_payload['id']):
        return'invitation accepted', 201

    return 'fail', 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

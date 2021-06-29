import datetime
import os

from flask import Flask, request
import jwt
from flask_cors import CORS
from flask_socketio import SocketIO, disconnect, rooms

from database import ChatMembership, Message, Chat
from db_tools import user_tools, chat_tools, inventation_tools, message_tools
from decorators import require_token

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    "TOKEN_SECRET", "yoursuperstrongpassword123")

cors = CORS(app)

sio = SocketIO(app, always_connect=True, cors_allowed_orgins='*')

# websocket stuff
user_sid = {}
sid_user = {}

@app.route('/ping', methods=['GET'])
def pong():
    return 'pong', 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not 'login' in data or not 'password' in data:
        return 'Bad request', 400

    if not user_tools.isLoginAvalible(data['login']):
        return 'User with this login already exist', 409

    if not user_tools.registerUser(data['login'], data['password']):
        'Unknown error', 500

    return 'Account created', 201

# przydał by się refresh token
# czas życia tokena można przenioeść do zm środowiskowych
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not 'login' in data or not 'password' in data:
        return 'Bad request', 400

    user = user_tools.loginUser(data['login'], data['password'])
    if not user:
        return 'Password or login is worong', 403

    token = jwt.encode({
        'id': user.id,
        'user': user.login,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'])

    return {"token": token}, 200


# wysyła listę wszystkich nicków/loginów zarejestrowanych w bazie
@app.route('/users', methods=['GET'])
@require_token
def getAllUsers(token_payload):
    users = user_tools.getAllUsers()
    users = list(map(lambda usr: {'login': usr.login,'id': usr.id},users))

    return {'users': users}, 200


# wysyła listę aktywych chatów do klienta
@app.route('/chat', methods=['GET'])
@require_token
def getChatList(token_payload):
    chatlist = chat_tools.getChatList(token_payload['id'])

    chatlist = list(
        map(lambda inv: {
            'id': inv.id, 
            'name': inv.name, 
            'inv': inv.creator, 
            'new_messages': chat_tools.getNewMessagesCount(token_payload['id'], inv.id)
            }, chatlist))
        
    return {'chatlist': chatlist}, 200


# służy do wysyłania wiadomości przez kilenta oraz ich odbierania
@app.route('/message', methods=['POST', 'GET'])
@require_token
def message(token_payload):
    if request.method == 'POST':
        data = request.get_json()

        if not 'target' in data or not 'content' in data:
            return 'Bad request', 400

        user = user_tools.getUserById(token_payload['id'])
        target_chat = chat_tools.getChatById(data['target'])

        if not user:
            return 'Bad request', 400

        if not target_chat:
            return 'Target chat not found', 404 # może inny error code ?

        message = Message(user, data['content'], target_chat)

        if message_tools.sendMessage(message):
            membersips = chat_tools.getChatMembersIds(target_chat.id)
            
            for m in membersips:
                if m.user_id in user_sid:
                    sio.emit('new_message', target_chat.id, room=user_sid[m.user_id])

            return 'succes', 201

        return 'fail', 400  # może inny error code ?

    if request.method == 'GET':
        data = request.get_json()

        if not 'chat_id' in data:
            return 'Bad request', 400

        chat: Chat = chat_tools.getChatById(data['chat_id'])

        if not chat_tools.isMemberOfChat(chat.id, token_payload['id']):
            return 'you are not member of this chat', 403

        messages = message_tools.getChatMessages(chat.id)

        data_for_client = []
        for m in messages:
            data_for_client.append({
                'id': m.id,
                'content': m.content,
                'send_time': m.send_time, 
                'readed': message_tools.isMesssageReaded(m.id,token_payload['id']),
                'sender_name': user_tools.getUserById(m.sender_id).login
            })

        return {'messages': data_for_client}, 200


@app.route('/message/status',methods=['POST'])
@require_token
def markMessage(token_payload):
    user_id = token_payload['id']
    data = request.get_json()

    if not 'msg_ids' in data or not user_id:
        return 'Bad request', 400

    for msg_id in data['msg_ids']:
        message_tools.markAsReaded(msg_id, user_id)

    return 'succes', 201  

# słóży do pobierania i wysyłania zaproszeń
@app.route('/invitate', methods=['GET', 'POST'])
@require_token
def invitate(token_payload):
    if request.method == 'GET':
        invitations = inventation_tools.getInvitations(token_payload['id'])
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

        if inventation_tools.addInvitation(token_payload['id'], inv_user_id):
            return 'invitation created', 201

        return 'failed to create or invitation already exist', 400


# słóży do akceptacji zaproszeń
@app.route('/invitate/accept',  methods=['POST'])
@require_token
def acceptInv(token_payload):
    data = request.get_json()

    if 'user_id' not in data:
        return 'Bad request', 400
    inv_user_id = data['user_id']

    if inventation_tools.acceptInvitation(inv_user_id, token_payload['id']):
        return'invitation accepted', 201

    return 'fail', 400


# ================================ web-sockets =========================================

@sio.on('connect')
def connSocket():
    try: 
        data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
    except:
        disconnect(sid=request.sid)
        raise ConnectionRefusedError('unauthorized')
    
    print("Connecting: " + str(request.sid))
    if 'id' in data:
        user_id = data['id']
        #updateStatus(user_id, active=True)
        user_sid[user_id] = request.sid
        sid_user[request.sid] = user_id


@sio.on('disconnect')
def discSocket():
    #updateStatus(sid_user[request.sid], active = False)
    del user_sid[sid_user[request.sid]]
    del sid_user[request.sid]

# def updateStatus(user_id: int, active: bool):
#     sio.emit('')


# ================================ web-sockets =========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    sio.run(app, host='0.0.0.0', port=port)
    #app.run(debug=True, host='0.0.0.0', port=port)

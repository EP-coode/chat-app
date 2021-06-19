import datetime
import hashlib
import os

from flask import Flask, request
from sqlalchemy.orm.session import Session
import jwt

from database import User, DB_Session
from db_operations import isLoginAvalible, loginUser, registerUser

app = Flask(__name__)
token_secret = os.getenv("TOKEN_SECRET", "yoursuperstrongpassword123")


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
    }, token_secret)

    return {"token": token}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

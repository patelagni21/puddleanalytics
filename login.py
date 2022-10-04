import authorization

from flask_login import LoginManager
#from flask_login import current_user, login_user, logout_user, login_required
from flask_pymongo import PyMongo


import base64

auth = authorization.Auth()
login_manager = LoginManager()
mongo = PyMongo()

class Login():
    def __init__(self, app):
        mongo.init_app(app)
        login_manager.init_app(app)
        auth.init_app(app)

class User(): # Compose a User from a MongoDB document.
    def __init__(self, obj):
        self.id = obj["_id"]
        self.session_id = obj.get("_sessionId")

        self.email = obj["email"]
        self.password_hash = obj["hashedPw"]
        self.salt = obj["salt"]
        

@login_manager.request_loader
def load_user_from_request(request):
    auth_key = request.headers.get('Authorization')
    if auth_key:
        auth_key = auth_key.replace('Basic','',1)
        try:
            auth_key = base64.b64decode(auth_key)
        except TypeError:
            pass

        session = mongo.db.auth.sessions.find_one({"session_token":auth_key})
        if session:
            user = mongo.db.auth.login.find_one({"user_id":session["user_id"]})
            if user:
                return user
            else: return None
        else:
            return None

@login_manager.user_loader
def load_user(email):
    user = auth.get_user(email)
    if user != None:
        return User(user)
    else:
        return None
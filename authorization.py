from flask_pymongo import PyMongo
import bcrypt, string, random
import secrets, time
__id_charset__ = string.ascii_letters+string.digits

class Auth:
    def __init__(self, app=None):
        self.mongo = PyMongo(app)
        
    def init_app(self, app):
        self.mongo.init_app(app)

    # append user, pass, and salt to database
    # generate entry in sessions for new user
    def registerUser(self, user, password):
        print(f"Registering user with {user}:{password}")

        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(password=password, salt=salt)
        id = ''.join(random.choice(__id_charset__) for x in range(5))

        
        if self.get_user(user) == None:
            try:
                self.mongo.db.login.insert_one(
                    {
                        "_id":id,
                        "email":user,
                        "hashedPw":pw_hash.decode("utf-8"),
                        "salt":salt.decode("utf-8")
                    }
                )
                print("Successfully registered user.")
            except Exception as e:
                print(repr(e))
            
        else:
            return False
    
    def get_user(self, email):
        return self.mongo.db.login.find_one({"email":email})

    def validate_user(self, user, password): #Flask user object
        pw_hash, salt = user['hashedPw'], user['salt']

        password = password.encode('utf-8')
        salt = salt.encode('utf-8')

        hashed = bcrypt.hashpw(password, salt)

        if hashed.decode('utf-8') == pw_hash:
            return True

            
        return False

class Sessions:
    def __init__(self, app=None):
        self.mongo = PyMongo(app)
        
    def init_app(self, app):
        self.mongo.init_app(app)

    # Update expiration time if cookie matches.
    def __updateSession__(self, user_id, token):
        return self.mongo.db.login.find_one_and_update(
            {"_id": user_id},
            {"_sessionId": token}
        )

    # Delete document with id.
    def deleteSession(self, session_id):
        if (self.getUserFromSession(session_id) != None):
            return self.mongo.db.login.find_one_and_update(
                {"_sessionId":session_id},
                {"$unset":{"_sessionId":None, "expires":None}}   
            )



    def getUserFromSession(self, session_id):
        user = self.mongo.db.login.find_one(
            {"_sessionId":session_id}
        )
        if(user != None):
            if time.time() > user['expires']:
                self.mongo.db.login.find_one_and_update(
                    {"_sessionId":session_id},
                    {"$unset":{"_sessionId":None, "expires":None}}   
                )
                return None
            return user
        else:
            return None

    # Get session document by id
    def __getSessionFromUser__(self, user_id):
        doc = self.mongo.db.login.find_one(
            {"_id":user_id}
        )
        return None if doc == None else doc.get("_sessionId")

    # Assign a cookie and expiration time.
    def newSession(self, user_id):
        print(f"Creating a session for USER_ID={user_id}")

        session_id = self.__getSessionFromUser__(user_id)
        if session_id != None:
            print("A session already exists. Delete existing session.")
            self.deleteSession(session_id)
        
        token = secrets.token_urlsafe(32)

        print(f"Session id is {token}")
        self.mongo.db.login.update_one(
            {"_id":user_id}, # Sessions expire after 1 hour
            {"$set":{"_sessionId": token, "expires":time.time()+(60*60)}}
        )
        
        return token

    # Validate cookie with id
    def validateSession(self, user_id, token) -> bool:
        return self.mongo.auth.sessions.find_one({"_id":user_id, "_token":token}) != None
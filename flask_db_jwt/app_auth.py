from users import User

def authenticate(username, password):
    user = User.find_by_name(username)
    if user and user.password == password:
        return user

def identity(payload):
    return User.find_by_id(payload['identity'])



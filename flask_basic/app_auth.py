from users import User
from werkzeug.security import safe_str_cmp

users_list = [
    User(1, 'bob', 'abcd'),
    User(2, 'alice', 'xyz')
]

users_table = {u.name:u for u in users_list}
userid_table = {u.id:u for u in users_list}


def authenticate1(username, password):
    user = users_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity1(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

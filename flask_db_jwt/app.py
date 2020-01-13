from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from users import UserRegister, User, UsersList
from app_auth import authenticate, identity
from items import Item, ItemList


app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'python'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, '/items')
api.add_resource(UsersList, "/user")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

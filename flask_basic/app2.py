from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from app_auth import authenticate1, identity1

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'abcd'

api = Api(app)
jwt = JWT(app, authenticate1, identity1) ## it will create the /auth endpoint

items = [
    {
        'name':'guitar',
        'price':300
    },
    {
        'name':'keyboard',
        'price':400
    }
]

class Item(Resource):
    @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return {'item': item}
        return {'message':'Item does not exists.'}

    def post(self, name):
        ## first check if item exists
        request_data = request.get_json()
        for item in items:
            if item['name'] == name:
                return ({'message':'Item already exists.'})

        item = {'name':name, 'price':request_data.get('price')}
        items.append(item)
        return item

    def put(self, name):
        request_data = request.get_json()
        for item in items:
            if item['name'] == name:
                item['price'] = request_data.get('price')
                return item
        item = {'name':name, 'price':request_data.get('price')}
        items.append(item)
        return item

    def delete(self, name):
        global items
        temp = []
        for item in items:
            if item['name'] != name:
                temp.append(item)
        items = temp
        return {'message':'item deleted'}

class ItemList(Resource):

    def get(self):
        return {'items':items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)
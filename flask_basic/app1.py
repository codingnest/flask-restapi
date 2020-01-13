from flask import Flask, request, jsonify

app = Flask(__name__)

stores = [
    {'name':'my_store1',
        'items':[
            {
                'name':'guitar',
                'price':30.5
            },
            {
                'name':'violin',
                'price':40
            }
        ]
    },
    {'name':'my_store2',
        'items':[
            {
                'name':'python book',
                'price':130.5
            },
            {
                'name':'java book',
                'price':140
            }
        ]
    }
]

# get /store
@app.route("/store/<string:store_name>")
def get_store(store_name):
    for store in stores:
        if store['name'] == store_name:
            return jsonify(store)
    return jsonify({'message':'store not exists.'})


# post /store
@app.route("/store", methods=['post'])
def create_store():
    request_data = request.get_json() ## its a dict object
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

# create item
@app.route("/store/<string:store_name>/item", methods=['post'])
def create_store_item(store_name):
    request_data = request.get_json()
    item = {
        'name':request_data['name'],
        'price':request_data['price']
    }
    for store in stores:
        if store['name'] == store_name:
            store['items'].append(item)
            return jsonify(item)
    return jsonify({'message':'store not exists.'})

# get store
@app.route("/store")
def get_stores():
    return jsonify({'stores':stores})

@app.route("/store/<string:store_name>/item")
def get_items(store_name):
    for store in stores:
        if store['name'] == store_name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'store not exists.'})

app.run(port=5000)





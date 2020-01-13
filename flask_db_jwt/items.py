import sqlite3
from flask_jwt import JWT
from flask import Flask, request
from flask_restful import Resource
from flask_jwt import jwt_required

class Item(Resource):
    TABLE_NAME = 'ITEMS'

    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'Item not found.'}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        request_data = request.get_json()
        price = request_data['price']

        item = {'name':name, 'price':price}
        self.insert(item)
        return item

    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            Item.insert(updated_item)
        else:
            Item.update(updated_item)
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select * from {table} where name=?'.format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}


class ItemList(Resource):
    TABLE_NAME = 'items'

    @jwt_required()
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select * from {table}'.format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        conn.close()
        return {'items':items}





from flask_restful import Resource
from flask_jwt import JWT
from flask import request
import sqlite3


class User():
    TABLE_NAME = "users"

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select * from {table} where username=?'.format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))

        row = result.fetchone()
        conn.close()

        if row:
            return User(*row)

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select * from {table} where id=?'.format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        conn.close()

        if row:
            return User(*row)


class UserRegister(Resource):
    TABLE_NAME = 'users'

    def post(self):
        request_data = request.get_json()
        name = request_data['username']
        password = request_data['password']

        if User.find_by_name(name):
            return {'message':'user already exists.'}, 400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (name, password))

        conn.commit()
        conn.close()

        return {'message':'user created successfuly.'}, 201


class UsersList(Resource):
    TABLE_NAME = 'users'

    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = 'select * from {table}'.format(table=self.TABLE_NAME)
        result = cursor.execute(query)

        users = []
        for user in result:
            users.append({'userid':user[0], 'username':user[1]})

        return {'users':users}




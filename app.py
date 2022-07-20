import json
import sqlite3
from flask import Flask, request, abort
from flask_cors import CORS

import collections

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except ValueError as e:
        print('Cannot connecting to database', e)


# -------------- Методы желаний -------------- #

# Метод получения всех желаний
@app.route('/wishList')
def getWishesList():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # sql_Query = 'SELECT * FROM wishes WHERE id=1'
        # cursor.execute(sql_Query)
        cursor.execute('SELECT * FROM wishes')
        rows = cursor.fetchall()
        conn.close()

    except ValueError as e:
        print('Error reading data from SQL table', e)

    wish_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['title'] = row[1]
        d['active'] = row[2]
        wish_list.append(d)

    return json.dumps({"data": wish_list})


# Метод добавления нового желания
@app.route('/addWish', methods=['POST'])
def addWish():
    request_data = request.get_json()

    firstName = None
    lastName = None
    wish_id = None

    if request_data:
        if 'firstName' in request_data:
            firstName = request_data['firstName']

        if 'lastName' in request_data:
            lastName = request_data['lastName']

        if 'wish_id' in request_data:
            wish_id = request_data['wish_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (firstName, lastName) VALUES (?, ?)',
                       (firstName, lastName))

        user_id = cursor.lastrowid
        if user_id > 0:
            cursor.execute('INSERT INTO client_wishes (id_client, id_wish) VALUES (?, ?)',
                           (user_id, wish_id))
        else:
            print('create user error')
        conn.commit()
        conn.close()

        return '''
            creator is: {}
            title is {}'''.format(user_id, wish_id)


# Метод изменения желания
@app.route('/wishes/edit', methods=['POST'])
def wish_edit():
    request_data = request.get_json()

    title = request_data['title']

    id = request_data['id']

    conn = get_db_connection()
    conn.execute('UPDATE wishes SET title = ? WHERE id = ?',
                 (title, id))
    conn.commit()
    conn.close()

    return '''
        title is {}'''.format(title)


# Метод удаления желания
@app.route('/wishes/delete', methods=['DELETE'])
def wish_delete():
    request_data = request.get_json()

    id = request_data['id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM wishes WHERE id = ?',
                   (id,))
    conn.commit()
    conn.close()

    return ''


# -------------- Методы пользователей -------------- #

@app.route('/userList')
def getUserList():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # sql_Query = 'SELECT * FROM wishes WHERE id=1'
        # cursor.execute(sql_Query)
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()

    except ValueError as e:
        print('Error reading data from SQL table', e)

    user_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['firstName'] = row[1]
        d['lastName'] = row[2]
        user_list.append(d)

    return json.dumps({"data": user_list})


# Метод изменения пользователя
@app.route('/users/edit', methods=['POST'])
def user_edit():
    request_data = request.get_json()

    first_name = request_data['firstName']

    last_name = request_data['lastName']

    user_id = request_data['id']

    conn = get_db_connection()
    conn.execute('UPDATE users SET firstName = ?, lastName = ? WHERE id = ?',
                 (first_name, last_name, user_id))
    conn.commit()
    conn.close()

    return '''
        title is {}'''.format(id)


# Метод получения всех пользователей, которые выбрали конкретное желание
@app.route('/users-wish', methods=['POST'])
def getUsersWishList():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        request_data = request.get_json()

        wish_id = request_data['id']

        cursor.execute('SELECT users.id, users.firstName || " " || users.lastname as fullName'
                       ' FROM client_wishes'
                       ' INNER JOIN wishes ON wishes.id = client_wishes.id_wish'
                       ' INNER JOIN users ON users.id = client_wishes.id_client '
                       'WHERE wishes.id = ?',
                       (wish_id,))
        rows = cursor.fetchall()
        conn.close()

    except ValueError as e:
        print('Error reading data from SQL table', e)

    list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['fullName'] = row[1]
        list.append(d)

    return json.dumps({"data": list})

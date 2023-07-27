from flask import Flask, jsonify, request
from bson import ObjectId
from flask_cors import CORS
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://saochoa1:bgiT6rF3J4EzjVDa@clusterdashboardic.erg0gfr.mongodb.net/ic_dashboard'
mongo = PyMongo(app)

CORS(app)

@app.route('/users', methods=['GET'])
def obtain_users():
    users = mongo.db.users.find()
    response = []
    for user in users:
        response.append({
            '_id': str(user['_id']),
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'username': user['email'],
            'password': user['password'],
            'role': user['role']
        })
    return jsonify(response)

@app.route('/users/<id>', methods=['GET'])
def obtain_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = []
    if user:
        response.append({
            '_id': str(user['_id']),
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'username': user['username'],
            'password': user['password'],
            'role': user['role']
        })
        return jsonify(response), 200
    else:
        response = {'message': 'User not found'}
    return jsonify(response)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data.get('email')})
    if user:
        response = {'message': 'User already exists'}
    else:
        mongo.db.users.insert_one(data)
        response = {'message': 'User created successfully'}, 201
    return jsonify(response)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': id})
    if user:
        mongo.db.users.update_one({'_id': id}, {'$set': {
            'first_name': request.json['first_name'],
            'last_name': request.json['last_name'],
            'email': request.json['email'],
            'username': request.json['email'],
            'password': request.json['password'],
            'role': request.json['role']
        }})
        response = {'message': 'User updated successfully'}, 200
    else:
        response = {'message': 'User not found'}, 404
    return jsonify(response)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = {'message': 'User deleted successfully'}, 200
    else:
        response = {'message': 'User not found'}, 404
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

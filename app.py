from json import dumps
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import pymongo
from bson.objectid import ObjectId

connection_url = 'mongodb+srv://chandhu:Chandhu@cluster0.ih2ppdh.mongodb.net/?retryWrites=true&w=majority'
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)
Database = client.get_database('sampledb')
Sample_Collection = Database.samplecollection

@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _firstname = _json['first name']
    _lastname = _json['last name']
    _email = _json['email']
    _pwd = _json['password']
    if _firstname and _lastname and _email and _pwd and request.method == 'POST':
        _hashed_password = generate_password_hash(_pwd)
        id = Sample_Collection.insert_one({'first name':_firstname, 'last name':_lastname, 'email':_email, 'password':_hashed_password})
        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/all', methods=['GET'])
def get_all_user():
    users = Sample_Collection.find()
    resp = [{'first name' : user['first name'], 'last name' : user['last name'], 'email' : user['email'], 'password' : user['password']} for user in users]
    return jsonify(resp)

@app.route('/user/<id>')
def user(id):
    user = Sample_Collection.find_one({'_id': ObjectId(id)})
    resp = [{'first name' : user['first name'], 'last name' : user['last name'], 'email' : user['email'], 'password' : user['password']}]
    return jsonify(resp)

@app.route('/update/<id>', methods=['PUT'])
def user_update(id):
    _json = request.json
    _firstname = _json['first name']
    _lastname = _json['last name']
    _email = _json['email']
    _pwd = _json['password']
    if _firstname or _lastname or _email or _pwd and request.method == 'PUT':
        _hashed_password = generate_password_hash(_pwd)
        Sample_Collection.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'first name':_firstname, 'last name':_lastname, 'email':_email, 'password':_hashed_password}})
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/delete/<id>', methods=['DELETE'])
def user_delete(id):
    Sample_Collection.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)

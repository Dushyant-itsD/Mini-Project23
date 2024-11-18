import os
from flask import Flask,request,jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/Car_rental'
mongo=PyMongo(app)

CORS(app)

db=mongo.db.users


app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@app.route("/users",methods=['POST'])
def createUser():
    user_data = request.json
    password = user_data['password']
    hashed_password = generate_password_hash(password)

    new_user = {
            "fullName": user_data['fullName'],
            "email": user_data['email'],
            "contact": user_data['contact'],
            "current_location": user_data['current_location'],
            "password": hashed_password,
            "avatarUrl": "",  
            
           
                }
    db.insert_one(new_user)
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/user/<id>',methods=['GET'])
def getUser(id):
    user = db.find_one({"_id": ObjectId(id)}, {"_id": False, "password": False})

    return jsonify(
        {
            "fullName": user['fullName'],
            "email": user['email'],
            "contact": user['contact'],
            "current_location": user['current_location'],
            "avatarUrl": "",  
        }
    )

@app.route('/user/<id>',methods=['PUT'])
def updateUser(id):
    user_data = request.json
    password = user_data['password']
    hashed_password = generate_password_hash(password)
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        "fullName": user_data['fullName'],
        "email": user_data['email'],
        "contact": user_data['contact'],
        "current_location": user_data['current_location'],
        "password": hashed_password,
        "avatarUrl": "",  
    }})
    print(password)
    return jsonify({'msg':"User Updated successfully"})

if __name__=='__main__':
    app.run(debug=True)



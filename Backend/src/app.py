import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Car_rental'
mongo = PyMongo(app)
CORS(app)
db = mongo.db.users

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

@app.route("/users", methods=['POST'])
def create_user():
    user_data = request.json
    print(user_data)  # Print received user data for debugging

    try:
        hashed_password = generate_password_hash(user_data['password'])
        new_user = {
            "fullName": user_data['fullName'],
            "email": user_data['email'],
            "Contact": user_data['Contact'],
            "current_location": user_data['current_location'],
            "password": hashed_password,
            "avatarUrl": "",
        }

        result = db.insert_one(new_user)
        print(f"New user inserted with ID: {result.inserted_id}")  # Debug to see if insertion is successful
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")  # Print any error
        return jsonify({"error": str(e)}), 500


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.find_one({"_id": ObjectId(id)}, {"_id": False, "password": False})
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.json
    hashed_password = generate_password_hash(user_data['password'])
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        "fullName": user_data['fullName'],
        "email": user_data['email'],
        "contact": user_data['contact'],
        "current_location": user_data['current_location'],
        "password": hashed_password,
        "avatarUrl": "",
    }})
    return jsonify({'message': "User updated successfully"})

@app.route('/user/login', methods=['POST'])
def login_user():
    try:
        user_data = request.json
        email = user_data['email']
        password = user_data['password']

        
        user = db.find_one({"email": email})

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid email or password"}), 401

        
        access_token = create_access_token(identity={"email": email, "fullName": user['fullName']})

        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    except Exception as e:
        
        return jsonify({"error": str(e)}), 400

@app.route('/user/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        current_user_email = current_user['email']
        print("Current User:", current_user)  # Debug print to check the JWT identity
        
        # Fetch user from the database
        user = db.find_one({"email": current_user_email}, {"_id": False, "password": False})
        print("User Found:", user)  # Debug print to see the user data
        
        if user:
            return jsonify({
                "message": "Access to profile",
                "user": {
                    "fullName": user['fullName'],
                    "email": user['email'],
                    "contact": user['contact'],
                    "current_location": user['current_location'],
                    "avatarUrl": "",
                }
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Error: {e}")  # Debug print to check for any exceptions
        return jsonify({"error": "An error occurred while fetching the profile. Please try again later."}), 500



if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import logging

# Initialize Flask app
app = Flask(__name__)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Car_rental'
mongo = PyMongo(app)
db = mongo.db.users

# Enable CORS
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

### User Management Routes

@app.route("/users", methods=['POST'])
def create_user():
    """
    Register a new user.
    """
    try:
        user_data = request.json
        if db.find_one({"email": user_data['email']}):
            return jsonify({"error": "Email already exists"}), 400

        # Hash the password and save the user
        user_data['password'] = generate_password_hash(user_data['password'])
        user_data['avatarUrl'] = user_data.get('avatarUrl', '')
        result = db.insert_one(user_data)

        logger.info(f"User registered with ID: {result.inserted_id}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({"error": "Failed to register user"}), 500


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    """
    Retrieve user details by ID.
    """
    try:
        user = db.find_one({"_id": ObjectId(id)}, {"_id": False, "password": False})
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return jsonify({"error": "Failed to retrieve user"}), 500


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    """
    Update user details by ID.
    """
    try:
        user_data = request.json
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])
        db.update_one({'_id': ObjectId(id)}, {'$set': user_data})

        logger.info(f"User {id} updated successfully")
        return jsonify({'message': "User updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return jsonify({"error": "Failed to update user"}), 500


### Authentication Routes
import json

@app.route('/user/login', methods=['POST'])
def login_user():
    """
    Authenticate a user and generate a JWT token.
    """
    try:
        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Fetch user from database
        user = db.find_one({"email": email})
        if not user or not check_password_hash(user['password'], password):
            logger.warning(f"Invalid login attempt for email: {email}")
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate JWT token with serialized identity
        identity = json.dumps({
            "id": str(user['_id']),
            "fullName": user['fullName'],
            "email": user['email']
        })
        access_token = create_access_token(identity=identity)

        logger.info(f"User {email} logged in successfully")
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"error": "Failed to log in"}), 500


@app.route('/user/profile', methods=['GET'])
@jwt_required()
def profile():
    
    try:
        # Parse the serialized identity
        current_user = json.loads(get_jwt_identity())
        if not current_user:
            return jsonify({"error": "Unauthorized access"}), 401

        return jsonify({
            "message": "Profile retrieved successfully",
            "user": current_user
        }), 200
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        return jsonify({"error": "Failed to fetch profile"}), 500



### Entry Point

if __name__ == '__main__':
    app.run(debug=True)

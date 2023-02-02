from datetime import datetime, timedelta, timezone
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt

from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
jwt = JWTManager(app)

from controllers import user_controller


@app.route("/")
def home():
    return "Welcome to our houseplant API"


# Handle logging in 
@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test": # Need to compare these to database
        return {"message": "Invalid credentials"}, 401
    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}  


@app.route("/logout")
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route("/users")
def get_all_users():
    return user_controller.index

@app.route('/users/<int:id>')
def get_user():
    return user_controller.show

@app.route('/users/<int:id>/plants', methods=['GET','POST'])
def user_plants():
    return 

@app.route('/users/<int:id>/plants/<int:plant_id>', method=['GET', 'PUT', 'DELETE'])
def plant_handler():
    fns = {
        'GET':,
        'PUT':,
        'DELETE':
    }
     

if __name__ == "__main__":
    app.run(debug=True)

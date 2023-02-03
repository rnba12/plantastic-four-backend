from datetime import datetime, timedelta, timezone
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt
from werkzeug import exceptions
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
jwt = JWTManager(app)

from controllers import user_controller, user_plant_controller, plant_controller
from models import User

@app.route("/")
def home():
    return "Welcome to our houseplant API"


@app.route("/register", methods=['POST'])
def register():
    user_controller.create(request)
    return jsonify({"message": "User Created"})

# Handle logging in 
@app.route("/login", methods=["POST"])
def create_token():
    username = request.get_json()['username']
    password = request.get_json()['password']
    user = User.query.filter_by(username = username).first_or_404()
    print(user.check_password(password))
    if not user.check_password(password): # Need to compare these to database
        return {"message": "Invalid credentials"}, 401
    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}  
    return response


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


@app.route('/users/<username>')
@jwt_required()
def get_user(username):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    return user_controller.show(request, username)


@app.route('/users/<username>/plants', methods=['GET','POST'])
@jwt_required()
def user_plants(username):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    fns = {
        'GET': user_plant_controller.index ,
        'POST' : user_plant_controller.create
    }
    resp, code = fns[request.method](request, username)
    return jsonify(resp), code


@app.route('/users/<username>/plants/<int:plant_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def plant_handler(username, plant_id):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    fns = {
        'GET':user_plant_controller.show,
        'PUT': user_plant_controller.update,
        'DELETE': user_plant_controller.destroy
    }
    resp, code = fns[request.method](request, username, plant_id - 1)
    return jsonify(resp), code


@app.route("/plants")
@jwt_required()
def all_plants():
    resp, code = plant_controller.index(request)
    print(resp)
    return (resp), code
    


@app.route("/plants/<int:plant_id>")
@jwt_required()
def get_plant(plant_id):
    resp, code = plant_controller.show(request, plant_id)
    return (resp), code


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500

if __name__ == "__main__":
    app.run(debug=True)

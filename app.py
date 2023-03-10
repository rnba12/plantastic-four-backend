from apscheduler.schedulers.background import BackgroundScheduler
import time

from datetime import datetime, timedelta, timezone, date
import json
from flask import Flask, jsonify, request, Markup, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt
from werkzeug import exceptions
from config import Config


import os
from werkzeug.utils import secure_filename
import logging

import utils
app = Flask(__name__)
app.app_context().push()

from flask_mail import Message
from mailers import mail_config
mail = mail_config(app)

CORS(app)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
jwt = JWTManager(app)
app.config['UPLOAD_FOLDER'] = './TestSrc/uploads'
from model import predict_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('I am a plant')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from controllers import user_controller, user_plant_controller, plant_controller
from models import User, Plant


@app.route("/")
def home():
    return "Welcome to our houseplant API"


@app.route("/register", methods=['POST'])
def register():
    user_controller.create(request)
    return jsonify({"message": "User Created"}), 201

# Handle logging in


@app.route("/login", methods=["POST"])
def create_token():
    username = request.get_json()['username']
    password = request.get_json()['password']
    user = User.query.filter_by(username=username).first_or_404()
    print(user.check_password(password))
    if not user.check_password(password):  # Need to compare these to database
        return {"message": "Invalid credentials"}, 401
    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}
    return response, 201


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


@app.route('/users/<username>', methods=['PUT', 'DELETE'])
@jwt_required()
def get_user(username):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    fns = {
        'PUT': user_controller.update,
        'DELETE': user_controller.destroy
    }
    resp, code = fns[request.method](request, username)
    return jsonify(resp), code


@app.route('/users/<username>/plants', methods=['GET', 'POST'])
@jwt_required()
def user_plants(username):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    fns = {
        'GET': user_plant_controller.index,
        'POST': user_plant_controller.create
    }
    resp, code = fns[request.method](request, username)
    return jsonify(resp), code


@app.route('/users/<username>/plants/<int:plant_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def plant_handler(username, plant_id):
    if get_jwt_identity() != username:
        return jsonify({"message": "Thats not you"}), 401
    fns = {
        'GET': user_plant_controller.show,
        'PUT': user_plant_controller.update,
        'DELETE': user_plant_controller.destroy
    }
    resp, code = fns[request.method](request, username, plant_id - 1)
    return jsonify(resp), code


@app.route("/plants")
@jwt_required()
def all_plants():
    resp, code = plant_controller.index(request)
    return (resp), code


@app.route("/plants/<int:plant_id>")
@jwt_required()
def get_plant(plant_id):
    resp, code = plant_controller.show(request, plant_id)
    return (resp), code


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'POST':
#         try:
#             file = request.files['file']
#             img = file.read()
#             prediction = predict_image(img)
#             print(prediction)
#             res = Markup(utils.disease_dic[prediction])
#             print(res)
#             return res, 200
#         except:
#             pass
#     return "Nothing Posted so nothing to get | Internal Server Error", 500

# @app.route('/upload', methods=['POST'])
# def fileUpload():
#     target = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     logger.info("welcome to trying to upload my plant image`")
#     file = request.files['file']
#     #filename = secure_filename(file.filename)
#     #destination = "/".join([target, filename])
#     #file.save(destination)
#     #session['uploadFilePath'] = destination
#     img = file.read()
#     prediction = predict_image(img)
#     print(prediction)
#     res = Markup(utils.disease_dic[prediction])
#     response = jsonify(res)
#     return response, 200

# @app.route('/upload', methods=['GET', 'POST'])
# def fileUpload():
#     logger.info("welcome to trying to upload my plant image`")
#     msg = "nothing uploaded"
#     if request.method == 'POST':
#         file = request.files['file']
#         img = file.read()
#         prediction = predict_image(img)
#         print(prediction)
#         res = Markup(utils.disease_dic[prediction])
#         print(res)
#         response = jsonify(res)
#         return response, 200
#     return msg, 400

@app.route('/upload', methods=['GET', 'POST'])
def fileUpload():

    file = request.files['file']
    img = file.read()
    prediction = predict_image(img)
    # print(prediction)
    res = Markup(utils.disease_dic[prediction])
    print(res)
    result = jsonify(res)
    print(result)
    return result, 200


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    logger.info("welcome to trying to upload my plant image`")
    msg = "nothing uploaded"
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction)
            result = Markup(utils.disease_dic[prediction])
            print(result)
            result2 = jsonify(result)
            print(result2)
            return result2, 200
        except:
            pass
    return jsonify({"message": "Internal server problem"}), 500


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500


def send_email(email, plant_name, water_freq, username):
    msg = Message('Plant Watering Reminder',
                  sender='your_email@gmail.com', recipients=[email])
    # msg.body = f"It's been {water_freq} days since you last watered {plant_name}. Please water it today."
    msg.html = render_template(
        "email.html", plant_name=plant_name, water_freq=water_freq, username=username)
    mail.send(msg)


def check_watering():
    app.app_context().push()
    plant_data = Plant.query.all()
    for plant in plant_data:
        username = plant.owner.username
        email = plant.owner.email
        plant_name = plant.nickname
        last_watered_date = plant.last_watered
        water_freq = plant.water_freq

        diff = date.today() - last_watered_date
        if diff.days >= water_freq:
            send_email(email, plant_name, water_freq, username)


check_watering()

sched = BackgroundScheduler(daemon=True)
sched.add_job(check_watering, 'interval', days=1)
sched.start()

if __name__ == "__main__":
    app.run(debug=True)

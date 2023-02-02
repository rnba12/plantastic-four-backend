from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from controllers import user_controller


@app.route("/")
def home():
    return "Welcome to our houseplant API"

@app.route("/users")
def get_all_users():
    return user_controller.index

if __name__ == "__main__":
    app.run(debug=True)

from models import User
from app import db
from werkzeug.security import generate_password_hash



def show(req, username):
    user = User.query.filter_by(username = username).first_or_404()
    return User.as_dict(user), 200


def create(req):
    user_data = req.get_json()
    print(user_data)
    password_hash = generate_password_hash(user_data['password'])
    user = User(
        username = user_data['username'],
        password_hash = password_hash,
        email = user_data['email']
    )
    db.session.add(user)
    db.session.commit()
    return user_data

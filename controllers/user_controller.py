from models import User

def index(req):
    return User.query.all(), 200



from models import Plant, User
from app import db

# Get users plants
def index(req, user_id):
    user = User.query.get(user_id)
    all_plants = user.plants.all()
    return all_plants.plants, 200

# Get data for one plant
def show(req, user_id, plant_id):
    user = User.query.get(user_id)
    plant = user.plants.get(plant_id)
    return plant, 200

# Add new plant
def create(req, data, user_id):
    user = User.query.get(user_id)
    plant = Plant(data)
    db.session.add(plant, owner=user)
    db.session.commit()
    return plant, 201

# Delete plant
def destroy(req, plant_id):
    user = User.query.get(user_id)
    plant = user.plants.get(plant_id)
    db.session.delete(plant)
    db.commit()
    return "Plant Deleted", 204

def update(req, user_id, plant_id):
    user = User.query.get(user_id)
    plant_to_edit = user.plants.get(plant_id)
    data = req.get_json()
    plant_to_edit.nickname = data.nickname
    plant_to_edit.water_freq = data.water_freq
    plant_to_edit.purchase_date = data.purchase_date

    return plant_to_edit, 200

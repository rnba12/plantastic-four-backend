from models import Plant, User
from app import db

# Get users plants
def index(req, username):
    user = User.query.filter_by(username = username).first_or_404()
    all_plants = user.plants.all()
    return_list = []
    for plant in all_plants:
        return_list.append(plant.as_dict())
    return return_list, 200

# Get data for one plant
def show(req, username, plant_id):
    user = User.query.filter_by(username = username).first_or_404()
    plant = user.plants[plant_id]
    return {"plant": plant.as_dict(), "data": plant.data.as_dict()}, 200

# Add new plant
def create(req, username):
    user = User.query.filter_by(username = username).first_or_404()
    data = req.get_json()
    plant = Plant(
        nickname = data['nickname'],
        water_freq = data['water_freq'],
        purchase_date = data['purchase_date'],
        plant_data_id = data['plant_data_id'],
        owner = user
    )
    db.session.add(plant)
    db.session.commit()
    return {'message': 'Plant Added'}, 201

# Delete plant
def destroy(req, username, plant_id):
    user = User.query.filter_by(username = username).first_or_404()
    plant = user.plants[plant_id]
    print(plant)
    db.session.delete(plant)
    db.session.commit()
    return "Plant Deleted", 204

def update(req, username, plant_id):
    user = User.query.filter_by(username = username).first_or_404()
    plant_to_edit = user.plants[plant_id]
    data = req.get_json()
    plant_to_edit.nickname = data["nickname"]
    plant_to_edit.water_freq = data["water_freq"]
    # plant_to_edit.purchase_date = data["purchase_date"]
    db.session.commit()
    return plant_to_edit.as_dict(), 200

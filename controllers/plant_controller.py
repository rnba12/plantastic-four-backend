from models import Plant_Data
from app import db

def index(req):
    all_plants = Plant_Data.query.all()
    return_list = []
    for plant in all_plants:
        return_list.append(Plant_Data.as_dict(plant))
    return return_list, 200


def show(req, plant_id):
    plant = Plant_Data.query.get(plant_id)
    return Plant_Data.as_dict(plant), 200

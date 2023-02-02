import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://qjtgrmfm:Fa7_jQDLidMKezEMid4xaWlspAj75rOw@hattie.db.elephantsql.com/qjtgrmfm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

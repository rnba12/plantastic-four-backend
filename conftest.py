import pytest
import app


@pytest.fixture
def api():
    # test_users = [
    #     {
    #         "id": 1,
    #         "username": "username1",
    #         "email": "email1@email1.com",
    #         "password": "password1"
    #     },
    #     {
    #         "id": 2,
    #         "username": "username2",
    #         "email": "email2@email2.com",
    #         "password": "password2"
    #     }
    # ]

    # test_plants = [
    #     {
    #         "id": 1,
    #         "user_id": 1,
    #         "nickname": "plant1",
    #         "water_freq": 1,
    #         "purchase_date": "01/01/01",
    #         "plant_data_id": 1
    #     },
    #     {
    #         "id": 2,
    #         "user_id": 2,
    #         "nickname": "plant2",
    #         "water_freq": 2,
    #         "purchase_date": "02/02/02",
    #         "plant_data_id": 2
    #     }
    # ]

    # test_plant_data = [
    #     {
    #         "id": 1,
    #         "category": "category1",
    #         "names": "names1",
    #         "latin_name": "latin_name1",
    #         "min_temp": 1,
    #         "max_tem": 10,
    #         "ideal_light": "ideal_light1",
    #         "tolerated_light": "tolerated_light1",
    #         "pests": "pests1",
    #         "watering": "watering1",
    #         "origin": "origin1",
    #         "climate": "climate1"
    #     },
    #     {
    #         "id": 2,
    #         "category": "category2",
    #         "names": "names2",
    #         "latin_name": "latin_name2",
    #         "min_temp": 2,
    #         "max_tem": 20,
    #         "ideal_light": "ideal_light2",
    #         "tolerated_light": "tolerated_light2",
    #         "pests": "pests2",
    #         "watering": "watering2",
    #         "origin": "origin2",
    #         "climate": "climate2"
    #     }
    # ]

    # monkeypatch.setattr(app, "users", test_users)
    # monkeypatch.setattr(app, "plants", test_plants)
    # monkeypatch.setattr(app, "plant_data", test_plant_data)
    app.app.app_context().push()
    api = app.app.test_client()
    return api


# @pytest.fixture(scope='session')
# def database(request):
#     '''
#     Create a Postgres database for the tests, and drop it when the tests are done.
#     '''
#     pg_host = DB_OPTS.get("host")
#     pg_port = DB_OPTS.get("port")
#     pg_user = DB_OPTS.get("username")
#     pg_db = DB_OPTS["database"]

#     init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

#     @request.addfinalizer
#     def drop_database():
#         drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)


# @pytest.fixture(scope='session')
# def app(database):
#     '''
#     Create a Flask app context for the tests.
#     '''
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

#     return app


# @pytest.fixture(scope='session')
# def _db(app):
#     '''
#     Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
#     database connection.
#     '''
#     db = SQLAlchemy(app=app)

#     return db

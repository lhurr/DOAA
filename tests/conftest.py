import pytest,datetime
from application import db
from application.model.user import User, add_new_user
from application.model.pred_history import PredictionHistory
from werkzeug.security import generate_password_hash
from app import app_init

test_app = app_init(env='testing')

@pytest.fixture
def app():
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    # print(app.static_url_path)
    return app.test_client()



@pytest.fixture
def add_user():
    new_app = app_init(env='testing')
    from application import db
    users =  {"email": "user1@example.com",
            "password": "Password1234!"}
    try:
        with new_app.app_context():
            new_user = User(
                    email=users["email"],
                    password=generate_password_hash(users["password"]),
                    created=datetime.datetime.utcnow(),
                )
            add_new_user(new_user)
        yield dict(context = new_app.test_client() , userid = new_user.id )
        with new_app.app_context():
            User.session.query.delete()
            PredictionHistory.session.query.delete() 
            db.session.commit()
    except:
        pass
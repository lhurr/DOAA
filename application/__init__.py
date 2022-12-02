from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import cloudpickle

with open('application/static/regressor_final.p', 'rb') as f:
    MODEL = cloudpickle.load(f)

APP_TITLE = 'Super Life'

# ONLY ALLOW MIN to MAX values of the dataset
INTRAPOLATION = {
 'age_min': 18,
 'age_max': 66,
 'height_min': 145,
 'height_max': 188,
 'weight_min': 51,
 'weight_max': 132,
 'price_min': 15000 *0.017,
 'price_max': 40000*0.017
}
# Convert to SGD

db = SQLAlchemy()

def app_init(env='development'):
    app = Flask(__name__)
    if env == 'development':
        app.config.from_pyfile('dev_config.cfg')
        
    elif env == 'testing':
        app.testing = True
        app.config.from_pyfile('test_config.cfg')



    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = "routes.login"
    login_manager.login_message_category = "info"
    login_manager.login_message = "Login to access that page"
    login_manager.init_app(app)

    
    from .model.user import User
    from .model.pred_history import PredictionHistory
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    with app.app_context():
        db.create_all()

    from .controller.routes import routes 
    app.register_blueprint(routes)

    from .controller.api import api
    app.register_blueprint(api)
    return app

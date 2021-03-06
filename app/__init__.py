from flask import Flask
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
#from flask_principal import Principal
#from flask_migrate import Migrate
from flask_user import UserManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap



login_manager = LoginManager()
db = SQLAlchemy()
admin = Admin()
mail = Mail()
bootsrap = Bootstrap()
#principal = Principal()
#migrate = Migrate()


def create_app(config_name='config.py'):

    app = Flask(__name__)

    # lee la config desde el archivo config.py
    app.config.from_pyfile(config_name)
    bootsrap.init_app(app)

    login_manager.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    #principal.init_app(app)
    # Se inicializa el objeto migrate
    #migrate.init_app(app, db)

    # Registro de los Blueprints
    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .restricted import restricted_bp
    app.register_blueprint(restricted_bp)

    from .auth.models import User
    user_manager = UserManager(app, db, User)

    return app








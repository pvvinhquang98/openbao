from flask import Flask
from config import Config
from app.models import db
from flask_migrate import Migrate
from app.views import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    # Đăng ký blueprint
    app.register_blueprint(main)

    return app

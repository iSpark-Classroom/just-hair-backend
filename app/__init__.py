from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return "Welcome to Just Hair Backend!"

    # Import models so migrations can detect them
    from app import models

    # Register routes (Blueprints)
    from app.routes.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app

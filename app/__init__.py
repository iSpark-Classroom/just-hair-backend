
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import os
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,API_URL,config={'app_name':"API"}
    )
    app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)

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
    from app.routes.reviews import  reviews_bp
    app.register_blueprint(reviews_bp)


    return app








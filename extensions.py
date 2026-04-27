"""Flask Extensions"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import get_config

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


config = get_config()

def init_extensions(app):
    """Initialize extensions before the app"""
    cors.init_app(
        app,
        supports_credentials=True,
        origins=[config.FRONTEND_URL],
    )
    jwt.init_app(app)
    db.init_app(app)

    # Imports models before to allow alembic generate models
    from src.models.user_model import User 
    from src.models.piece_model import Piece

    migrate.init_app(
        app,
        db,
        compare_type=True,
        compare_server_default=True,
    )

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_session import Session
from flask_compress import Compress
from flask_talisman import Talisman

# Extensions

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300})
session_ext = Session()
compress = Compress()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(app.instance_path, "shop.db")),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE="filesystem",
        SESSION_PERMANENT=False,
    )

    os.makedirs(app.instance_path, exist_ok=True)

    # Security headers (basic)
    Talisman(app, content_security_policy=None)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)
    session_ext.init_app(app)
    compress.init_app(app)

    # Blueprints
    from .blueprints.storefront import bp as storefront_bp
    from .blueprints.account import bp as account_bp
    from .blueprints.cart import bp as cart_bp
    from .blueprints.admin import bp as admin_bp
    app.register_blueprint(storefront_bp)
    app.register_blueprint(account_bp, url_prefix="/account")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app

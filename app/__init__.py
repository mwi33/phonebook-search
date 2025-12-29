import os
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Default config
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        DATABASE_PATH=os.environ.get(
        "DATABASE_PATH",
            os.path.join(app.instance_path, "phonebook.db"),
        ),
        MAX_RESULTS_PER_PAGE=int(os.environ.get("MAX_RESULTS_PER_PAGE", "50")),
        MAX_TOTAL_RESULTS=int(os.environ.get("MAX_TOTAL_RESULTS", "500")),
    )

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Register DB + routes
    from . import db
    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

from flask import Flask
from .db import init_db
from .auth import auth_bp
from .dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    init_db(app)  # setup DB connection

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app

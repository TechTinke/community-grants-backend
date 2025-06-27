from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    db_path = '/opt/render/project/src/grants.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ee16580264f049f9a8dcb69a16761f79')
    
    print(f"Checking if database exists at: {db_path}")
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
    
    db.init_app(app)
    migrate.init_app(app, db)
    # Broaden CORS for debugging
    CORS(app, resources={r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }})
    
    # Debug CORS headers
    @app.after_request
    def add_cors_headers(response):
        print(f"Adding CORS headers to response: {response.headers}")
        return response
    
    with app.app_context():
        db.create_all()
        print("Tables created:", db.engine.table_names())
    
    from . import models
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    return app
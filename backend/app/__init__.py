from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    """ method used to create an app instance """
    app = Flask(__name__)

    CORS(app, resources={r"/api/v1/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    # Load configuration from the specified config class
    app.config.from_object(config_class)

    api = Api(app, version='1.0', title='Skill Sessions API', description='Skill Sessions Booking Platform API')
    
    # Initialize the database with the app
    db.init_app(app)

    # Initialize Flask-Migrate for handling database migrations
    # migrate = Migrate(app, db)

    from app.api.v1.users import api as users_ns
    from app.api.v1.skills import api as skills_ns
    from app.api.v1.skill_sessions import api as skill_sessions_ns
    from app.api.v1.bookings import api as bookings_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(skills_ns, path='/api/v1/skills')
    api.add_namespace(skill_sessions_ns, path='/api/v1/skill-sessions')
    api.add_namespace(bookings_ns, path='/api/v1/bookings')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Ensure database tables are created before the first request
    with app.app_context():
        db.create_all()
        
    return app

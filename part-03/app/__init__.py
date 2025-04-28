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

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    
    # Initialize the database with the app
    db.init_app(app)

    # Initialize Flask-Migrate for handling database migrations
    # migrate = Migrate(app, db)

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Ensure database tables are created before the first request
    with app.app_context():
        db.create_all()
        
    return app

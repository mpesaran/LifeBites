from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.utils.jwt_auth import get_current_user_from_token

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'bio': fields.String(required=False, description='User bio'),
    'phone': fields.String(required=False, description='User phone'),
    'location': fields.String(required=False, description='User location'),
    'experience_level': fields.String(required=False, description='User experience level'),
    'hourly_rate': fields.Float(required=False, description='Hourly rate for instructors'),
    'is_instructor': fields.Boolean(required=False, description='Is user an instructor')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        token = user.generate_token()
        return {
            'access_token': token,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_instructor': user.is_instructor,
                'is_admin': user.is_admin
            }
        }, 200

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Register a new user and return a JWT token"""
        user_data = api.payload

        # Check if user already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'User with this email already exists'}, 400

        try:
            # Create new user
            new_user = facade.create_user(user_data)
            token = new_user.generate_token()

            return {
                'access_token': token,
                'user': {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email,
                    'is_instructor': new_user.is_instructor,
                    'is_admin': new_user.is_admin
                }
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/me')
class CurrentUser(Resource):
    def get(self):
        """Get current user information from JWT token"""
        current_user = get_current_user_from_token()
        if not current_user:
            return {'error': 'Invalid or missing token'}, 401

        return {
            'id': current_user.id,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'bio': current_user.bio,
            'profile_picture': current_user.profile_picture,
            'phone': current_user.phone,
            'location': current_user.location,
            'experience_level': current_user.experience_level,
            'hourly_rate': current_user.hourly_rate,
            'is_instructor': current_user.is_instructor,
            'is_admin': current_user.is_admin,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        }, 200
        
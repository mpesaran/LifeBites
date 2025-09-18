"""JWT Authentication utilities and decorators."""

from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User
from app.services.facade import facade


def jwt_required(f):
    """Decorator to require JWT authentication."""
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        token = None

        # Check for token in Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Bearer <token>
                token = auth_header.split(' ')[1]
            except IndexError:
                return {'error': 'Invalid token format'}, 401

        if not token:
            return {'error': 'Token is missing'}, 401

        # Verify token
        payload = User.verify_token(token)
        if payload is None:
            return {'error': 'Token is invalid or expired'}, 401

        # Get current user from facade
        current_user = facade.get_user(payload['user_id'])
        if not current_user:
            return {'error': 'User not found'}, 401

        # Pass current_user to the decorated function
        return f(self, current_user, *args, **kwargs)

    return decorated_function


def instructor_required(f):
    """Decorator to require instructor privileges."""
    @wraps(f)
    def decorated_function(self, current_user, *args, **kwargs):
        if not current_user.is_instructor:
            return {'error': 'Instructor privileges required'}, 403
        return f(self, current_user, *args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated_function(self, current_user, *args, **kwargs):
        if not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        return f(self, current_user, *args, **kwargs)

    return decorated_function


def get_current_user_from_token():
    """Extract current user from JWT token in request."""
    token = None
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None

    if not token:
        return None

    payload = User.verify_token(token)
    if payload is None:
        return None

    return facade.get_user(payload['user_id'])
""" User model """

import uuid
import re
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
from app import db
from sqlalchemy.orm import validates


bcrypt = Bcrypt()


class User(db.Model):
    """ User class for skill session platform """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    experience_level = db.Column(db.String(20), nullable=False, default='beginner')  # beginner, intermediate, advanced, expert
    hourly_rate = db.Column(db.Float, nullable=True)  # for instructors
    is_instructor = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    # Relationships
    skill_sessions_r = db.relationship('SkillSession', back_populates='instructor_r', cascade="all, delete")
    reviews_written_r = db.relationship('Review', foreign_keys='Review.user_id', back_populates="user_r", cascade="all, delete")
    reviews_received_r = db.relationship('Review', foreign_keys='Review.instructor_id', back_populates="instructor_r", cascade="all, delete")
    bookings_r = db.relationship('Booking', back_populates="user_r", cascade="all, delete")


    def __init__(self, first_name, last_name, email, password, bio=None, phone=None, location=None, experience_level='beginner', hourly_rate=None, is_instructor=False, is_admin=False):
        if first_name is None or last_name is None or email is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.bio = bio.strip() if bio else None
        self.phone = phone.strip() if phone else None
        self.location = location.strip() if location else None
        self.experience_level = experience_level
        self.hourly_rate = hourly_rate
        self.is_instructor = is_instructor
        self.is_admin = is_admin
        self.hash_password(password) 

    @validates("email")
    def validates_email(self, key, value):
        """validate email format before saving."""
        if not re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value):
            raise ValueError("Invalid email format!")
        return value.strip()

    @validates("experience_level")
    def validates_experience_level(self, key, value):
        """Validate experience level is one of the allowed values."""
        allowed_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        if value not in allowed_levels:
            raise ValueError(f"Experience level must be one of: {', '.join(allowed_levels)}")
        return value

    @validates("hourly_rate")
    def validates_hourly_rate(self, key, value):
        """Validate hourly rate is positive if provided."""
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            raise ValueError("Hourly rate must be a positive number")
        return value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def check_password(self, password):
        """Checks the password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)


    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def add_skill_session(self, session):
        """Add a skill session to the instructor."""
        if not self.is_instructor:
            raise ValueError("User must be an instructor to add skill sessions")
        self.skill_sessions_r.append(session)

    def add_booking(self, booking):
        """Add a booking to the user."""
        self.bookings_r.append(booking)

    def get_average_rating(self):
        """Calculate average rating for instructor from reviews."""
        if not self.is_instructor or not self.reviews_received_r:
            return None
        total_rating = sum(review.rating for review in self.reviews_received_r)
        return total_rating / len(self.reviews_received_r)

    # def delete(self, user_id):
    #     user = self.get(user_id)
    #     if user:
    #         db.session.delete(user)
    #         db.session.commit()

    @staticmethod
    def email_exists(email):
        """ Search through all Users to check the email exists """
        # Unused - the facade method get_user_by_email will handle this

    def generate_token(self):
        """Generate JWT token for the user."""
        from flask import current_app
        payload = {
            'user_id': self.id,
            'email': self.email,
            'is_instructor': self.is_instructor,
            'is_admin': self.is_admin,
            'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user data."""
        from flask import current_app
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def email_exists(email):
        """ Search through all Users to check the email exists """
        # Unused - the facade method get_user_by_email will handle this

    @staticmethod
    def user_exists(user_id):
        """ Search through all Users to ensure the specified user_id exists """
        # Unused - the facade method get_user will handle this

""" User model """

import uuid
import re
from datetime import datetime
from flask_bcrypt import Bcrypt
from app import db
from sqlalchemy.orm import validates


bcrypt = Bcrypt()


class User(db.Model):
    """ User class """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())
    
    properties_r = db.relationship('Place', back_populates='owner_r', cascade="all, delete")
    reviews_r = db.relationship('Review', back_populates="user_r", cascade="all, delete")


    def __init__(self, first_name, last_name, email, password, is_admin = False):
        # NOTE: Attributes that don't already exist will be
        # created when called in the constructor

        if first_name is None or last_name is None or email is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.hash_password(password)
        self.is_admin = is_admin

        # self.places = [] # List to store user-owned places
        # self.reviews = [] # List to store user-written reviews 

    @validates("email")
    def validates_email(self, key, value):
        """validate email format before saving."""
        if not re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value):
            raise ValueError("Invalid email format!")
        return value.strip()

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

    def add_place(self, place):
        """Add a place to the user."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the user."""
        self.reviews.append(review)

    # def delete(self, user_id):
    #     user = self.get(user_id)
    #     if user:
    #         db.session.delete(user)
    #         db.session.commit()

    @staticmethod
    def email_exists(email):
        """ Search through all Users to check the email exists """
        # Unused - the facade method get_user_by_email will handle this

    @staticmethod
    def user_exists(user_id):
        """ Search through all Users to ensure the specified user_id exists """
        # Unused - the facade method get_user will handle this

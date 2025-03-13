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

    @validates("email")
    def validates_email(self, key, value):
        """validate email format before saving."""
        if not re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value):
            raise ValueError("Invalid email format!")
        return value.strip()

    

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

        self.places = [] # List to store user-owned places
        self.reviews = [] # List to store user-written reviews 


    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    # --- Getters and Setters ---
    # Setters are actually called when values are assigned in the constructor!
    # @property
    # def password(self):
    #     return self._password
    
    # @password.setter
    # def password(self, value):
    #     self._password = value

    # @property
    # def first_name(self):
    #     """Getter for prop first_name"""
    #     return self._first_name

    # @first_name.setter
    # def first_name(self, value):
    #     """Setter for prop first_name"""
    #     # ensure that the value is up to 50 alphabets only after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._first_name = value.strip()
    #     else:
    #         raise ValueError("Invalid first_name length!")

    # @property
    # def last_name(self):
    #     """Getter for prop last_name"""
    #     return self._last_name

    # @last_name.setter
    # def last_name(self, value):
    #     """Setter for prop last_name"""
    #     # ensure that the value is up to 50 alphabets only after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._last_name = value.strip()
    #     else:
    #         raise ValueError("Invalid last_name length!")

    # @property
    # def email(self):
    #     """Getter for prop email"""
    #     return self._email

    # @email.setter
    # def email(self, value):
    #     """Setter for prop last_name"""
    #     # calls the method in the facade object
    #     from app.services import facade

    #     # add a simple regex check for email format. Nothing too fancy.
    #     is_valid_email = len(value.strip()) > 0 and re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value)
    #     email_exists = facade.get_user_by_email(value.strip())
    #     if is_valid_email and not email_exists:
    #         self._email = value
    #     else:
    #         if email_exists:
    #             raise ValueError("Email already exists!")

    #         raise ValueError("Invalid email format!")

    # @property
    # def is_admin(self):
    #     """Getter for prop is_admin"""
    #     return self._is_admin

    # @is_admin.setter
    # def is_admin(self, value):
    #     """Setter for prop is_admin"""
    #     if isinstance(value, bool):
    #         self._is_admin = value
    #     else:
    #         raise ValueError("Invalid is_admin value!")


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

    @staticmethod
    def email_exists(email):
        """ Search through all Users to check the email exists """
        # Unused - the facade method get_user_by_email will handle this

    @staticmethod
    def user_exists(user_id):
        """ Search through all Users to ensure the specified user_id exists """
        # Unused - the facade method get_user will handle this

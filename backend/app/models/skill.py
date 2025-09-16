""" Skill Model """

import uuid
from datetime import datetime
from app import db
from sqlalchemy.orm import validates
from app.models.associations import session_skill

class Skill(db.Model):
    """ Skill class for categorizing sessions """
    __tablename__ = 'skills'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'Technology', 'Arts', 'Language', 'Cooking', etc.
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    # Relationships
    sessions_r = db.relationship("SkillSession", secondary=session_skill, back_populates="skills_r")

    @validates("name")
    def validates_name(self, key, value):
        """Validates the skill name"""
        # ensure that the value is up to 50 characters after removing excess white-space
        is_valid_name = 0 < len(value.strip()) <= 50
        if is_valid_name:
            return value.strip()
        else:
            raise ValueError("Invalid name length!")

    @validates("category")
    def validates_category(self, key, value):
        """Validates the skill category"""
        allowed_categories = ['Technology', 'Arts', 'Language', 'Cooking', 'Music', 'Sports', 'Business', 'Photography', 'Writing', 'Other']
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return value

    def __init__(self, name, category, description=None):
        if name is None or category is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name.strip()
        self.category = category
        self.description = description.strip() if description else None

    # --- Getters and Setters ---
    # @property
    # def name(self):
    #     """ Returns value of property name """
    #     return self._name

    # @validates("name")
    # def name(self, value):
    #     """Setter for prop name"""
    #     # ensure that the value is up to 50 characters after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._name = value.strip()
    #     else:
    #         raise ValueError("Invalid name length!")
        
    # @name.setter
    # def name(self, value):
    #     """Setter for prop name"""
    #     # ensure that the value is up to 50 characters after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._name = value.strip()
    #     else:
    #         raise ValueError("Invalid name length!")


    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

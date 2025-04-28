import uuid
from app import db
from datetime import datetime
from sqlalchemy.orm import validates


class Review(db.Model):
    """Review Class"""
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user_r = db.relationship('User', back_populates="reviews_r")
    place_r = db.relationship('Place', back_populates="reviews_r")

    def __init__(self, text, rating, place_id, user_id):
        if text is None or rating is None or place_id is None or user_id is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    # --- Validators ---
    @validates('text')
    def validate_text(self, key, value):
        """Ensure text is provided"""
        if not value:
            raise ValueError("Text is required for review")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        """Ensure rating is between 1 and 5"""
        if not (1 <= int(value) <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        """Validate if the user exists"""
        from app.services import facade
        user_exists = facade.get_user(value)
        if not user_exists:
            raise ValueError("User does not exist!")
        return value

    @validates('place_id')
    def validate_place_id(self, key, value):
        """Validate if the place exists"""
        from app.services import facade
        place_exists = facade.get_place(value)
        if not place_exists:
            raise ValueError("Place does not exist!")
        return value
    

    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    @staticmethod
    def review_exists(review_id):
        """ Search through all Reviews to ensure the specified review_id exists """
        # Unused - the facade method get_review will handle this

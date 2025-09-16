import uuid
from app import db
from datetime import datetime
from sqlalchemy.orm import validates


class Review(db.Model):
    """Review Class for skill sessions"""
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # reviewer
    session_id = db.Column(db.String(36), db.ForeignKey('skill_sessions.id'), nullable=False)
    instructor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # instructor being reviewed
    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'), nullable=False)  # ensures only booked users can review

    # Relationships
    user_r = db.relationship('User', foreign_keys=[user_id], back_populates="reviews_written_r")
    instructor_r = db.relationship('User', foreign_keys=[instructor_id], back_populates="reviews_received_r")
    session_r = db.relationship('SkillSession', back_populates="reviews_r")
    booking_r = db.relationship('Booking', back_populates="review_r")

    def __init__(self, text, rating, session_id, user_id, instructor_id, booking_id):
        if text is None or rating is None or session_id is None or user_id is None or instructor_id is None or booking_id is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.session_id = session_id
        self.user_id = user_id
        self.instructor_id = instructor_id
        self.booking_id = booking_id

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

    @validates('session_id')
    def validate_session_id(self, key, value):
        """Validate if the session exists"""
        from app.services import facade
        session_exists = facade.get_skill_session(value)
        if not session_exists:
            raise ValueError("Skill session does not exist!")
        return value

    @validates('instructor_id')
    def validate_instructor_id(self, key, value):
        """Validate if the instructor exists and is an instructor"""
        from app.services import facade
        instructor = facade.get_user(value)
        if not instructor:
            raise ValueError("Instructor does not exist!")
        if not instructor.is_instructor:
            raise ValueError("User is not an instructor!")
        return value

    @validates('booking_id')
    def validate_booking_id(self, key, value):
        """Validate if the booking exists and is completed"""
        from app.services import facade
        booking = facade.get_booking(value)
        if not booking:
            raise ValueError("Booking does not exist!")
        if booking.status != 'completed':
            raise ValueError("Can only review completed sessions!")
        return value
    

    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    @staticmethod
    def review_exists(review_id):
        """ Search through all Reviews to ensure the specified review_id exists """
        # Unused - the facade method get_review will handle this

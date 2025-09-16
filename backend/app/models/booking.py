""" Booking Model """

import uuid
from datetime import datetime
from app import db
from sqlalchemy.orm import validates


class Booking(db.Model):
    """ Booking class for skill session reservations """
    __tablename__ = 'bookings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(36), db.ForeignKey('skill_sessions.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)  # when the session is scheduled
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, cancelled, completed
    participants = db.Column(db.Integer, nullable=False, default=1)  # number of spots booked
    total_price = db.Column(db.Float, nullable=False)
    special_requests = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    # Relationships
    user_r = db.relationship('User', back_populates="bookings_r")
    session_r = db.relationship('SkillSession', back_populates="bookings_r")
    review_r = db.relationship('Review', back_populates="booking_r", uselist=False)

    def __init__(self, user_id, session_id, booking_date, participants=1, special_requests=None):
        if user_id is None or session_id is None or booking_date is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.user_id = user_id
        self.session_id = session_id
        self.booking_date = booking_date
        self.participants = participants
        self.status = 'pending'
        self.special_requests = special_requests.strip() if special_requests else None

        # Calculate total price (will be set by the service layer)
        self.total_price = 0.0

    # --- Validators ---
    @validates('status')
    def validate_status(self, key, value):
        """Validate booking status"""
        allowed_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return value

    @validates('participants')
    def validate_participants(self, key, value):
        """Validate number of participants"""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Participants must be a positive integer")
        return value

    @validates('booking_date')
    def validate_booking_date(self, key, value):
        """Validate booking date is in the future"""
        if value <= datetime.now():
            raise ValueError("Booking date must be in the future")
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

    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def confirm_booking(self):
        """Confirm the booking"""
        self.status = 'confirmed'
        self.save()

    def cancel_booking(self):
        """Cancel the booking"""
        self.status = 'cancelled'
        self.save()

    def complete_booking(self):
        """Mark booking as completed"""
        self.status = 'completed'
        self.save()

    def is_editable(self):
        """Check if booking can be edited (only pending bookings)"""
        return self.status == 'pending'

    def is_cancellable(self):
        """Check if booking can be cancelled (pending or confirmed, and not past date)"""
        return self.status in ['pending', 'confirmed'] and self.booking_date > datetime.now()

    @staticmethod
    def booking_exists(booking_id):
        """ Search through all Bookings to ensure the specified booking_id exists """
        # Unused - the facade method get_booking will handle this
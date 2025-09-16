from app.persistence.repository import SQLAlchemyRepository
from app.models.booking import Booking
from app import db

class BookingRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Booking)

    def get_by_user(self, user_id):
        """Get all bookings by user ID."""
        return self.model.query.filter_by(user_id=user_id).all()

    def get_by_session(self, session_id):
        """Get all bookings for a specific session."""
        return self.model.query.filter_by(session_id=session_id).all()

    def get_by_status(self, status):
        """Get bookings by status."""
        return self.model.query.filter_by(status=status).all()

    def get_confirmed_bookings_for_session(self, session_id):
        """Get all confirmed bookings for a session."""
        return self.model.query.filter_by(session_id=session_id, status='confirmed').all()

    def get_user_booking_for_session(self, user_id, session_id):
        """Get a specific user's booking for a session."""
        return self.model.query.filter_by(user_id=user_id, session_id=session_id).first()

    def booking_exists(self, booking_id):
        """Check if a booking exists by its ID."""
        return self.model.query.filter_by(id=booking_id).first() is not None

    def get_completed_bookings_by_user(self, user_id):
        """Get all completed bookings for a user (for review eligibility)."""
        return self.model.query.filter_by(user_id=user_id, status='completed').all()
import uuid
from datetime import datetime
from app import db
from sqlalchemy.orm import validates
from app.models.associations import session_skill

class SkillSession(db.Model):
    __tablename__ = "skill_sessions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)  # price per session
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    max_participants = db.Column(db.Integer, nullable=False, default=1)
    session_type = db.Column(db.String(20), nullable=False, default='online')  # online, in-person, hybrid
    difficulty_level = db.Column(db.String(20), nullable=False, default='beginner')  # beginner, intermediate, advanced
    location = db.Column(db.String(200), nullable=True)  # for in-person sessions
    latitude = db.Column(db.Float, nullable=True)  # for in-person sessions
    longitude = db.Column(db.Float, nullable=True)  # for in-person sessions
    instructor_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    # Relationships
    instructor_r = db.relationship("User", back_populates="skill_sessions_r")
    reviews_r = db.relationship("Review", back_populates="session_r", lazy=True, cascade="all, delete-orphan")
    skills_r = db.relationship("Skill", secondary=session_skill, lazy='subquery', back_populates="sessions_r")
    bookings_r = db.relationship("Booking", back_populates="session_r", cascade="all, delete-orphan")

    def __init__(self, title, description, price, duration, instructor_id, max_participants=1, session_type='online', difficulty_level='beginner', location=None, latitude=None, longitude=None):
        if title is None or description is None or price is None or duration is None or instructor_id is None:
            raise ValueError("Required attributes not specified!")

        self.title = title
        self.description = description
        self.price = price
        self.duration = duration
        self.max_participants = max_participants
        self.session_type = session_type
        self.difficulty_level = difficulty_level
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.instructor_id = instructor_id
        self.is_active = True

    # --- Validators ---
    @validates("title")
    def validate_title(self, key, value):
        value = value.strip()
        if not 1 <= len(value) <= 100:
            raise ValueError("Title must be a non-empty string with max length 100.")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Invalid value specified for price")
        return float(value)

    @validates("duration")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Duration must be a positive integer (minutes)")
        return value

    @validates("max_participants")
    def validate_max_participants(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Max participants must be a positive integer")
        return value

    @validates("session_type")
    def validate_session_type(self, key, value):
        allowed_types = ['online', 'in-person', 'hybrid']
        if value not in allowed_types:
            raise ValueError(f"Session type must be one of: {', '.join(allowed_types)}")
        return value

    @validates("difficulty_level")
    def validate_difficulty_level(self, key, value):
        allowed_levels = ['beginner', 'intermediate', 'advanced']
        if value not in allowed_levels:
            raise ValueError(f"Difficulty level must be one of: {', '.join(allowed_levels)}")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if value is not None and (not isinstance(value, (int, float)) or not -90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return float(value) if value is not None else None

    @validates("longitude")
    def validate_longitude(self, key, value):
        if value is not None and (not isinstance(value, (int, float)) or not -180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return float(value) if value is not None else None



    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def add_skill(self, skill):
        """Add a skill to the session."""
        if skill not in self.skills_r:
            self.skills_r.append(skill)
            db.session.commit()

    def get_available_spots(self):
        """Get number of available spots for the session."""
        booked_count = len([booking for booking in self.bookings_r if booking.status == 'confirmed'])
        return self.max_participants - booked_count

    def is_fully_booked(self):
        """Check if the session is fully booked."""
        return self.get_available_spots() <= 0

    def get_average_rating(self):
        """Calculate average rating from reviews."""
        if not self.reviews_r:
            return None
        total_rating = sum(review.rating for review in self.reviews_r)
        return total_rating / len(self.reviews_r)

    @staticmethod
    def session_exists(session_id):
        """ Search through all SkillSessions to ensure the specified session_id exists """
        # Unused - the facade get_session method will handle this

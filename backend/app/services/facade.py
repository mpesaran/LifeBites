from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.skill import Skill
from app.models.skill_session import SkillSession
from app.models.review import Review
from app.models.booking import Booking
from app.persistence.user_repository import UserRepository
from app.persistence.skill_repository import SkillRepository
from app.persistence.skill_session_repository import SkillSessionRepository
from app.persistence.booking_repository import BookingRepository


class SkillSessionsFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.skill_session_repo = SkillSessionRepository()
        self.skill_repo = SkillRepository()
        self.booking_repo = BookingRepository()
        self.review_repository = SQLAlchemyRepository(Review)

    # --- Users ---
    def create_user(self, user_data):
        if self.user_repo.email_exists(user_data['email']):
            raise ValueError("Email already exists")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.delete(user_id)

    # --- Skills ---
    def get_skill_by_name(self, name):
        return self.skill_repo.get_by_attribute('name', name)

    def create_skill(self, skill_data):
        skill = Skill(**skill_data)
        self.skill_repo.add(skill)
        return skill

    def get_skill(self, skill_id):
        return self.skill_repo.get(skill_id)

    def get_all_skills(self):
        return self.skill_repo.get_all()

    def get_skills_by_category(self, category):
        return self.skill_repo.get_by_attribute('category', category)

    def update_skill(self, skill_id, skill_data):
        self.skill_repo.update(skill_id, skill_data)

    def delete_skill(self, skill_id):
        self.skill_repo.delete(skill_id)

    # --- Skill Sessions ---
    def create_skill_session(self, session_data):
        # Validate instructor exists and is an instructor
        instructor = self.get_user(session_data['instructor_id'])
        if not instructor:
            raise ValueError("Instructor not found")
        if not instructor.is_instructor:
            raise ValueError("User is not an instructor")

        session = SkillSession(**session_data)
        self.skill_session_repo.add(session)
        return session

    def get_skill_session(self, session_id):
        return self.skill_session_repo.get(session_id)

    def get_all_skill_sessions(self):
        return self.skill_session_repo.get_all()

    def get_sessions_by_instructor(self, instructor_id):
        return self.skill_session_repo.get_by_attribute('instructor_id', instructor_id)

    def get_sessions_by_skill(self, skill_id):
        return self.skill_session_repo.get_sessions_by_skill(skill_id)

    def get_active_sessions(self):
        return self.skill_session_repo.get_by_attribute('is_active', True)

    def update_skill_session(self, session_id, session_data):
        session = self.get_skill_session(session_id)
        if not session:
            raise ValueError("Skill session not found")
        self.skill_session_repo.update(session_id, session_data)

    def delete_skill_session(self, session_id):
        return self.skill_session_repo.delete(session_id)

    def deactivate_skill_session(self, session_id):
        return self.update_skill_session(session_id, {'is_active': False})

    # --- Bookings ---
    def create_booking(self, booking_data):
        # Validate session exists and has availability
        session = self.get_skill_session(booking_data['session_id'])
        if not session:
            raise ValueError("Skill session not found")
        if not session.is_active:
            raise ValueError("Session is not active")
        if session.get_available_spots() < booking_data.get('participants', 1):
            raise ValueError("Not enough available spots")

        # Calculate total price
        booking_data['total_price'] = session.price * booking_data.get('participants', 1)

        booking = Booking(**booking_data)
        self.booking_repo.add(booking)
        return booking

    def get_booking(self, booking_id):
        return self.booking_repo.get(booking_id)

    def get_all_bookings(self):
        return self.booking_repo.get_all()

    def get_bookings_by_user(self, user_id):
        return self.booking_repo.get_by_attribute('user_id', user_id)

    def get_bookings_by_session(self, session_id):
        return self.booking_repo.get_by_attribute('session_id', session_id)

    def get_bookings_by_status(self, status):
        return self.booking_repo.get_by_attribute('status', status)

    def update_booking(self, booking_id, booking_data):
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        self.booking_repo.update(booking_id, booking_data)

    def confirm_booking(self, booking_id):
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        booking.confirm_booking()
        return booking

    def cancel_booking(self, booking_id):
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if not booking.is_cancellable():
            raise ValueError("Booking cannot be cancelled")
        booking.cancel_booking()
        return booking

    def complete_booking(self, booking_id):
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        booking.complete_booking()
        return booking

    # --- Reviews ---
    def create_review(self, review_data):
        # Validate booking exists and is completed
        booking = self.get_booking(review_data['booking_id'])
        if not booking:
            raise ValueError("Booking not found")
        if booking.status != 'completed':
            raise ValueError("Can only review completed sessions")
        if hasattr(booking, 'review_r') and booking.review_r:
            raise ValueError("This booking has already been reviewed")

        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_session(self, session_id):
        return self.review_repository.get_by_attribute('session_id', session_id)

    def get_reviews_by_instructor(self, instructor_id):
        return self.review_repository.get_by_attribute('instructor_id', instructor_id)

    def get_reviews_by_user(self, user_id):
        return self.review_repository.get_by_attribute('user_id', user_id)

    def update_review(self, review_id, review_data):
        self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repository.delete(review_id)

    # --- Session and Skill Management ---
    def add_skill_to_session(self, session_id, skill_id):
        session = self.get_skill_session(session_id)
        skill = self.get_skill(skill_id)
        if not session:
            raise ValueError("Skill session not found")
        if not skill:
            raise ValueError("Skill not found")

        session.add_skill(skill)
        return session


# Create a global instance
facade = SkillSessionsFacade()
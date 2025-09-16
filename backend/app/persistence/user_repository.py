from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get a user by their email address."""
        return self.model.query.filter_by(email=email).first()

    def email_exists(self, email):
        """Check if an email already exists in the database."""
        return self.model.query.filter_by(email=email).first() is not None
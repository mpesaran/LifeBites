from app.persistence.repository import SQLAlchemyRepository
from app.models.skill_session import SkillSession
from app import db

class SkillSessionRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(SkillSession)

    def get_session_by_title(self, title):
        """Get a skill session by its title."""
        return self.model.query.filter_by(title=title).first()

    def session_exists(self, session_id):
        """Check if a skill session exists by its ID."""
        return self.model.query.filter_by(id=session_id).first() is not None

    def get_by_instructor(self, instructor_id):
        """Get all sessions by instructor ID."""
        return self.model.query.filter_by(instructor_id=instructor_id).all()

    def get_active_sessions(self):
        """Get all active sessions."""
        return self.model.query.filter_by(is_active=True).all()

    def get_sessions_by_skill(self, skill_id):
        """Get all sessions associated with a specific skill."""
        return self.model.query.join(SkillSession.skills_r).filter_by(id=skill_id).all()

    def get_by_session_type(self, session_type):
        """Get sessions by type (online, in-person, hybrid)."""
        return self.model.query.filter_by(session_type=session_type).all()

    def get_by_difficulty_level(self, difficulty_level):
        """Get sessions by difficulty level."""
        return self.model.query.filter_by(difficulty_level=difficulty_level).all()
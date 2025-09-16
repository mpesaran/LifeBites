from app.persistence.repository import SQLAlchemyRepository
from app.models.skill import Skill

class SkillRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Skill)

    def get_by_category(self, category):
        """Get all skills by category"""
        return self.get_by_attribute('category', category)
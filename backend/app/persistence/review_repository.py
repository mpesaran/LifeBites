from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_rating(self, rating):
        return self.model.query.filter_by(rating=rating).all()
from flask_restx import Namespace, Resource, fields
# from app.services.facade import HBnBFacade
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        wanted_keys_list = ['text', 'rating', 'user_id', 'place_id']

        # check that required attributes are present
        if not all(name in wanted_keys_list for name in review_data):
            return { 'error': "Invalid input data - required attributes missing" }, 400

        # check that user exists
        user = facade.get_user(str(review_data.get('user_id')))
        if not user:
            return { 'error': "Invalid input data - user does not exist" }, 400

        # check that place exists
        place = facade.get_place(str(review_data.get('place_id')))
        if not place:
            return { 'error': "Invalid input data - place does not exist" }, 400

        # make sure review writer is not place owner
        if place.owner_id == user.id:
            return { 'error': "Invalid input data - review writer is place owner" }, 400

        # finally, create the review
        new_review = None
        try:
            new_review = facade.create_review(review_data)
        except ValueError as error:
            return { 'error': "Setter validation failure: {}".format(error) }, 400

        return {'id': str(new_review.id), 'message': 'Review created successfully'}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        output = []

        for review in all_reviews:
            output.append({
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating
            })

        return output, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        output = {
            'id': str(review.id),
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
        }

        return output, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        wanted_keys_list = ['text', 'rating']

        # check that required attributes are present
        if not all(name in wanted_keys_list for name in review_data):
            return { 'error': "Invalid input data - required attributes missing" }, 400

        # Check that place exists first before updating them
        review = facade.get_review(review_id)
        if review:
            try:
                facade.update_review(review_id, review_data)
            except ValueError as error:
                return { 'error': "Setter validation failure: {}".format(error) }, 400

            return {'message': 'Review updated successfully'}, 200

        return {'error': 'Review not found'}, 404

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
        except ValueError:
            return { 'error': "Review not found" }, 400

        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""

        reviews = facade.get_reviews_by_place(place_id)
        if reviews:
            return {'error': "Place not found"}, 404

        return reviews, 200
    
    @api.expect(review_model)
    @api.response(201, 'Review for place created successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """
        Add a review to a specific place"
        """
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}

        review_data = api.payload
        review_data['place_id'] = place_id

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': place_id,
                'created_at': new_review.created_at,
                'updated_at': new_review.updated_at
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 404
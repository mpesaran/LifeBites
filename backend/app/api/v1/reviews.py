from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.jwt_auth import jwt_required

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the reviewer'),
    'session_id': fields.String(required=True, description='ID of the skill session'),
    'instructor_id': fields.String(required=True, description='ID of the instructor'),
    'booking_id': fields.String(required=True, description='ID of the completed booking')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or validation failed')
    @api.response(401, 'Authentication required')
    @api.response(404, 'User, session, instructor, or booking not found')
    @jwt_required
    def post(self, current_user):
        """Create a new review for a completed session"""
        review_data = api.payload

        # Set user_id from authenticated user
        review_data['user_id'] = current_user.id

        # Validate required fields
        required_fields = ['text', 'rating', 'session_id', 'instructor_id', 'booking_id']
        if not all(field in review_data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        # Validate that session exists
        session = facade.get_skill_session(review_data['session_id'])
        if not session:
            return {'error': 'Skill session does not exist'}, 404

        # Validate that instructor exists and is an instructor
        instructor = facade.get_user(review_data['instructor_id'])
        if not instructor:
            return {'error': 'Instructor does not exist'}, 404
        if not instructor.is_instructor:
            return {'error': 'User is not an instructor'}, 400

        # Validate that booking exists and is completed
        booking = facade.get_booking(review_data['booking_id'])
        if not booking:
            return {'error': 'Booking does not exist'}, 404
        if booking.status != 'completed':
            return {'error': 'Can only review completed sessions'}, 400

        # Validate that the booking belongs to the reviewer
        if booking.user_id != review_data['user_id']:
            return {'error': 'Can only review your own bookings'}, 400

        # Validate that the booking is for the session being reviewed
        if booking.session_id != review_data['session_id']:
            return {'error': 'Booking does not match the session'}, 400

        # Validate that reviewer is not the instructor
        if review_data['user_id'] == review_data['instructor_id']:
            return {'error': 'Instructors cannot review their own sessions'}, 400

        try:
            new_review = facade.create_review(review_data)
        except ValueError as error:
            return {'error': f"Validation failure: {error}"}, 400

        return {
            'id': str(new_review.id),
            'session_id': new_review.session_id,
            'instructor_id': new_review.instructor_id,
            'rating': new_review.rating,
            'message': 'Review created successfully'
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        output = []

        for review in reviews:
            review_data = {
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'session_id': review.session_id,
                'instructor_id': review.instructor_id,
                'booking_id': review.booking_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }

            # Add user details
            if hasattr(review, 'user_r') and review.user_r:
                review_data['user'] = {
                    'first_name': review.user_r.first_name,
                    'last_name': review.user_r.last_name
                }

            # Add session details
            if hasattr(review, 'session_r') and review.session_r:
                review_data['session'] = {
                    'title': review.session_r.title,
                    'session_type': review.session_r.session_type,
                    'difficulty_level': review.session_r.difficulty_level
                }

            # Add instructor details
            if hasattr(review, 'instructor_r') and review.instructor_r:
                review_data['instructor'] = {
                    'first_name': review.instructor_r.first_name,
                    'last_name': review.instructor_r.last_name,
                    'experience_level': review.instructor_r.experience_level
                }

            output.append(review_data)

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
            'session_id': review.session_id,
            'instructor_id': review.instructor_id,
            'booking_id': review.booking_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }

        # Add detailed information
        if hasattr(review, 'user_r') and review.user_r:
            output['user'] = {
                'id': str(review.user_r.id),
                'first_name': review.user_r.first_name,
                'last_name': review.user_r.last_name,
                'email': review.user_r.email
            }

        if hasattr(review, 'session_r') and review.session_r:
            output['session'] = {
                'id': str(review.session_r.id),
                'title': review.session_r.title,
                'description': review.session_r.description,
                'session_type': review.session_r.session_type,
                'difficulty_level': review.session_r.difficulty_level,
                'duration': review.session_r.duration
            }

        if hasattr(review, 'instructor_r') and review.instructor_r:
            output['instructor'] = {
                'id': str(review.instructor_r.id),
                'first_name': review.instructor_r.first_name,
                'last_name': review.instructor_r.last_name,
                'bio': review.instructor_r.bio,
                'experience_level': review.instructor_r.experience_level
            }

        return output, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        try:
            facade.update_review(review_id, review_data)
        except ValueError as error:
            return {'error': f"Validation failure: {error}"}, 400

        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/session/<session_id>')
class SessionReviews(Resource):
    @api.response(200, 'Session reviews retrieved successfully')
    def get(self, session_id):
        """Get all reviews for a specific session"""
        reviews = facade.get_reviews_by_session(session_id)
        output = []

        for review in reviews:
            review_data = {
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'created_at': review.created_at.isoformat()
            }

            # Add user details
            if hasattr(review, 'user_r') and review.user_r:
                review_data['user'] = {
                    'first_name': review.user_r.first_name,
                    'last_name': review.user_r.last_name
                }

            output.append(review_data)

        return output, 200

@api.route('/instructor/<instructor_id>')
class InstructorReviews(Resource):
    @api.response(200, 'Instructor reviews retrieved successfully')
    def get(self, instructor_id):
        """Get all reviews for a specific instructor"""
        reviews = facade.get_reviews_by_instructor(instructor_id)
        output = []

        for review in reviews:
            review_data = {
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'session_id': review.session_id,
                'created_at': review.created_at.isoformat()
            }

            # Add user details
            if hasattr(review, 'user_r') and review.user_r:
                review_data['user'] = {
                    'first_name': review.user_r.first_name,
                    'last_name': review.user_r.last_name
                }

            # Add session details
            if hasattr(review, 'session_r') and review.session_r:
                review_data['session'] = {
                    'title': review.session_r.title,
                    'session_type': review.session_r.session_type
                }

            output.append(review_data)

        return output, 200

@api.route('/user/<user_id>')
class UserReviews(Resource):
    @api.response(200, 'User reviews retrieved successfully')
    def get(self, user_id):
        """Get all reviews written by a specific user"""
        reviews = facade.get_reviews_by_user(user_id)
        output = []

        for review in reviews:
            review_data = {
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'session_id': review.session_id,
                'instructor_id': review.instructor_id,
                'created_at': review.created_at.isoformat()
            }

            # Add session details
            if hasattr(review, 'session_r') and review.session_r:
                review_data['session'] = {
                    'title': review.session_r.title,
                    'session_type': review.session_r.session_type
                }

            # Add instructor details
            if hasattr(review, 'instructor_r') and review.instructor_r:
                review_data['instructor'] = {
                    'first_name': review.instructor_r.first_name,
                    'last_name': review.instructor_r.last_name
                }

            output.append(review_data)

        return output, 200
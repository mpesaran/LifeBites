from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.jwt_auth import jwt_required, instructor_required

api = Namespace('skill-sessions', description='Skill Session operations')

# Define related models
instructor_model = api.model('Instructor', {
    'id': fields.String(description='Instructor ID'),
    'first_name': fields.String(description='First name of the instructor'),
    'last_name': fields.String(description='Last name of the instructor'),
    'email': fields.String(description='Email of the instructor'),
    'bio': fields.String(description='Bio of the instructor'),
    'experience_level': fields.String(description='Experience level'),
    'hourly_rate': fields.Float(description='Hourly rate')
})

skill_model = api.model('Skill', {
    'id': fields.String(description='Skill ID'),
    'name': fields.String(description='Name of the skill'),
    'category': fields.String(description='Category of the skill')
})

review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='ID of the reviewer')
})

# Main skill session model
skill_session_model = api.model('SkillSession', {
    'title': fields.String(required=True, description='Title of the skill session'),
    'description': fields.String(required=True, description='Description of the session'),
    'price': fields.Float(required=True, description='Price per session'),
    'duration': fields.Integer(required=True, description='Duration in minutes'),
    'max_participants': fields.Integer(required=True, description='Maximum number of participants'),
    'session_type': fields.String(required=True, description='Type: online, in-person, or hybrid'),
    'difficulty_level': fields.String(required=True, description='Difficulty: beginner, intermediate, or advanced'),
    'location': fields.String(description='Location for in-person sessions'),
    'latitude': fields.Float(description='Latitude for in-person sessions'),
    'longitude': fields.Float(description='Longitude for in-person sessions'),
    'instructor_id': fields.String(required=True, description='ID of the instructor'),
    'instructor': fields.Nested(instructor_model, description='Instructor details'),
    'skills': fields.List(fields.Nested(skill_model), description='Associated skills'),
    'reviews': fields.List(fields.Nested(review_model), description='Session reviews')
})

@api.route('/')
class SkillSessionList(Resource):
    @api.expect(skill_session_model)
    @api.response(201, 'Skill session successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Instructor privileges required')
    @api.response(404, 'Instructor not found')
    @jwt_required
    @instructor_required
    def post(self, current_user):
        """Create a new skill session"""
        session_data = api.payload

        # Set instructor_id from authenticated user
        session_data['instructor_id'] = current_user.id

        # Validate required fields
        required_fields = ['title', 'description', 'price', 'duration']
        if not all(field in session_data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        try:
            new_session = facade.create_skill_session(session_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': str(new_session.id),
            'title': new_session.title,
            'instructor_id': new_session.instructor_id,
            'message': 'Skill session created successfully'
        }, 201

    @api.response(200, 'List of skill sessions retrieved successfully')
    def get(self):
        """Retrieve all skill sessions"""
        sessions = facade.get_all_skill_sessions()
        output = []

        for session in sessions:
            session_data = {
                'id': str(session.id),
                'title': session.title,
                'description': session.description,
                'price': session.price,
                'duration': session.duration,
                'max_participants': session.max_participants,
                'session_type': session.session_type,
                'difficulty_level': session.difficulty_level,
                'location': session.location,
                'instructor_id': session.instructor_id,
                'is_active': session.is_active,
                'available_spots': session.get_available_spots(),
                'average_rating': session.get_average_rating(),
                'created_at': session.created_at.isoformat()
            }

            # Add instructor details
            if hasattr(session, 'instructor_r') and session.instructor_r:
                session_data['instructor'] = {
                    'id': str(session.instructor_r.id),
                    'first_name': session.instructor_r.first_name,
                    'last_name': session.instructor_r.last_name,
                    'experience_level': session.instructor_r.experience_level
                }

            # Add skills
            if hasattr(session, 'skills_r'):
                session_data['skills'] = [{
                    'id': str(skill.id),
                    'name': skill.name,
                    'category': skill.category
                } for skill in session.skills_r]

            output.append(session_data)

        return output, 200

@api.route('/<session_id>')
class SkillSessionResource(Resource):
    @api.response(200, 'Skill session details retrieved successfully')
    @api.response(404, 'Skill session not found')
    def get(self, session_id):
        """Get skill session details by ID"""
        session = facade.get_skill_session(session_id)
        if not session:
            return {'error': 'Skill session not found'}, 404

        output = {
            'id': str(session.id),
            'title': session.title,
            'description': session.description,
            'price': session.price,
            'duration': session.duration,
            'max_participants': session.max_participants,
            'session_type': session.session_type,
            'difficulty_level': session.difficulty_level,
            'location': session.location,
            'latitude': session.latitude,
            'longitude': session.longitude,
            'instructor_id': session.instructor_id,
            'is_active': session.is_active,
            'available_spots': session.get_available_spots(),
            'average_rating': session.get_average_rating(),
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat()
        }

        # Add instructor details
        if hasattr(session, 'instructor_r') and session.instructor_r:
            output['instructor'] = {
                'id': str(session.instructor_r.id),
                'first_name': session.instructor_r.first_name,
                'last_name': session.instructor_r.last_name,
                'bio': session.instructor_r.bio,
                'experience_level': session.instructor_r.experience_level,
                'hourly_rate': session.instructor_r.hourly_rate,
                'average_rating': session.instructor_r.get_average_rating()
            }

        # Add skills
        if hasattr(session, 'skills_r'):
            output['skills'] = [{
                'id': str(skill.id),
                'name': skill.name,
                'category': skill.category,
                'description': skill.description
            } for skill in session.skills_r]

        # Add reviews
        if hasattr(session, 'reviews_r'):
            output['reviews'] = [{
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'created_at': review.created_at.isoformat()
            } for review in session.reviews_r]

        return output, 200

    @api.expect(skill_session_model)
    @api.response(200, 'Skill session updated successfully')
    @api.response(404, 'Skill session not found')
    @api.response(400, 'Invalid input data')
    def put(self, session_id):
        """Update a skill session"""
        session_data = api.payload

        try:
            facade.update_skill_session(session_id, session_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {'message': 'Skill session updated successfully'}, 200

    @api.response(200, 'Skill session deleted successfully')
    @api.response(404, 'Skill session not found')
    def delete(self, session_id):
        """Delete a skill session"""
        session = facade.get_skill_session(session_id)
        if not session:
            return {'error': 'Skill session not found'}, 404

        facade.delete_skill_session(session_id)
        return {'message': 'Skill session deleted successfully'}, 200

@api.route('/<session_id>/skills/<skill_id>')
class SkillSessionSkillResource(Resource):
    @api.response(200, 'Skill added to session successfully')
    @api.response(404, 'Session or skill not found')
    def post(self, session_id, skill_id):
        """Add a skill to a session"""
        try:
            facade.add_skill_to_session(session_id, skill_id)
        except ValueError as error:
            return {'error': str(error)}, 404

        return {'message': 'Skill added to session successfully'}, 200

@api.route('/instructor/<instructor_id>')
class InstructorSessions(Resource):
    @api.response(200, 'Sessions retrieved successfully')
    def get(self, instructor_id):
        """Get all sessions by instructor"""
        sessions = facade.get_sessions_by_instructor(instructor_id)
        output = []

        for session in sessions:
            output.append({
                'id': str(session.id),
                'title': session.title,
                'price': session.price,
                'duration': session.duration,
                'session_type': session.session_type,
                'difficulty_level': session.difficulty_level,
                'is_active': session.is_active,
                'available_spots': session.get_available_spots(),
                'created_at': session.created_at.isoformat()
            })

        return output, 200

@api.route('/active')
class ActiveSessions(Resource):
    @api.response(200, 'Active sessions retrieved successfully')
    def get(self):
        """Get all active sessions"""
        sessions = facade.get_active_sessions()
        output = []

        for session in sessions:
            output.append({
                'id': str(session.id),
                'title': session.title,
                'description': session.description,
                'price': session.price,
                'duration': session.duration,
                'session_type': session.session_type,
                'difficulty_level': session.difficulty_level,
                'available_spots': session.get_available_spots(),
                'instructor_id': session.instructor_id
            })

        return output, 200
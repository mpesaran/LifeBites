from flask_restx import Namespace, Resource, fields
from app.services import facade
from datetime import datetime

api = Namespace('bookings', description='Booking operations')

# Define models
booking_model = api.model('Booking', {
    'user_id': fields.String(required=True, description='ID of the user making the booking'),
    'session_id': fields.String(required=True, description='ID of the skill session to book'),
    'booking_date': fields.DateTime(required=True, description='Date and time of the session'),
    'participants': fields.Integer(description='Number of participants (default: 1)'),
    'special_requests': fields.String(description='Special requests or notes')
})

booking_update_model = api.model('BookingUpdate', {
    'booking_date': fields.DateTime(description='New date and time of the session'),
    'participants': fields.Integer(description='Number of participants'),
    'special_requests': fields.String(description='Special requests or notes')
})

@api.route('/')
class BookingList(Resource):
    @api.expect(booking_model)
    @api.response(201, 'Booking successfully created')
    @api.response(400, 'Invalid input data or booking validation failed')
    @api.response(404, 'Session not found')
    def post(self):
        """Create a new booking"""
        booking_data = api.payload

        # Validate required fields
        required_fields = ['user_id', 'session_id', 'booking_date']
        if not all(field in booking_data for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        # Convert string date to datetime if needed
        if isinstance(booking_data['booking_date'], str):
            try:
                booking_data['booking_date'] = datetime.fromisoformat(booking_data['booking_date'])
            except ValueError:
                return {'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}, 400

        try:
            new_booking = facade.create_booking(booking_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': str(new_booking.id),
            'user_id': new_booking.user_id,
            'session_id': new_booking.session_id,
            'status': new_booking.status,
            'total_price': new_booking.total_price,
            'message': 'Booking created successfully'
        }, 201

    @api.response(200, 'List of bookings retrieved successfully')
    def get(self):
        """Retrieve all bookings"""
        bookings = facade.get_all_bookings()
        output = []

        for booking in bookings:
            booking_data = {
                'id': str(booking.id),
                'user_id': booking.user_id,
                'session_id': booking.session_id,
                'booking_date': booking.booking_date.isoformat(),
                'status': booking.status,
                'participants': booking.participants,
                'total_price': booking.total_price,
                'special_requests': booking.special_requests,
                'created_at': booking.created_at.isoformat()
            }

            # Add session details
            if hasattr(booking, 'session_r') and booking.session_r:
                booking_data['session'] = {
                    'title': booking.session_r.title,
                    'duration': booking.session_r.duration,
                    'session_type': booking.session_r.session_type
                }

            # Add user details
            if hasattr(booking, 'user_r') and booking.user_r:
                booking_data['user'] = {
                    'first_name': booking.user_r.first_name,
                    'last_name': booking.user_r.last_name,
                    'email': booking.user_r.email
                }

            output.append(booking_data)

        return output, 200

@api.route('/<booking_id>')
class BookingResource(Resource):
    @api.response(200, 'Booking details retrieved successfully')
    @api.response(404, 'Booking not found')
    def get(self, booking_id):
        """Get booking details by ID"""
        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404

        output = {
            'id': str(booking.id),
            'user_id': booking.user_id,
            'session_id': booking.session_id,
            'booking_date': booking.booking_date.isoformat(),
            'status': booking.status,
            'participants': booking.participants,
            'total_price': booking.total_price,
            'special_requests': booking.special_requests,
            'created_at': booking.created_at.isoformat(),
            'updated_at': booking.updated_at.isoformat(),
            'is_editable': booking.is_editable(),
            'is_cancellable': booking.is_cancellable()
        }

        # Add session details
        if hasattr(booking, 'session_r') and booking.session_r:
            output['session'] = {
                'id': str(booking.session_r.id),
                'title': booking.session_r.title,
                'description': booking.session_r.description,
                'price': booking.session_r.price,
                'duration': booking.session_r.duration,
                'session_type': booking.session_r.session_type,
                'difficulty_level': booking.session_r.difficulty_level,
                'location': booking.session_r.location,
                'instructor_id': booking.session_r.instructor_id
            }

        # Add user details
        if hasattr(booking, 'user_r') and booking.user_r:
            output['user'] = {
                'id': str(booking.user_r.id),
                'first_name': booking.user_r.first_name,
                'last_name': booking.user_r.last_name,
                'email': booking.user_r.email
            }

        return output, 200

    @api.expect(booking_update_model)
    @api.response(200, 'Booking updated successfully')
    @api.response(400, 'Invalid input data or booking cannot be edited')
    @api.response(404, 'Booking not found')
    def put(self, booking_id):
        """Update a booking (only if status is pending)"""
        booking_data = api.payload

        # Convert string date to datetime if needed
        if 'booking_date' in booking_data and isinstance(booking_data['booking_date'], str):
            try:
                booking_data['booking_date'] = datetime.fromisoformat(booking_data['booking_date'])
            except ValueError:
                return {'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}, 400

        try:
            facade.update_booking(booking_id, booking_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {'message': 'Booking updated successfully'}, 200

    @api.response(200, 'Booking cancelled successfully')
    @api.response(400, 'Booking cannot be cancelled')
    @api.response(404, 'Booking not found')
    def delete(self, booking_id):
        """Cancel a booking"""
        try:
            facade.cancel_booking(booking_id)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {'message': 'Booking cancelled successfully'}, 200

@api.route('/<booking_id>/confirm')
class BookingConfirm(Resource):
    @api.response(200, 'Booking confirmed successfully')
    @api.response(404, 'Booking not found')
    @api.response(400, 'Booking cannot be confirmed')
    def post(self, booking_id):
        """Confirm a pending booking"""
        try:
            facade.confirm_booking(booking_id)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {'message': 'Booking confirmed successfully'}, 200

@api.route('/<booking_id>/complete')
class BookingComplete(Resource):
    @api.response(200, 'Booking marked as completed')
    @api.response(404, 'Booking not found')
    @api.response(400, 'Booking cannot be completed')
    def post(self, booking_id):
        """Mark a booking as completed"""
        try:
            facade.complete_booking(booking_id)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {'message': 'Booking marked as completed successfully'}, 200

@api.route('/user/<user_id>')
class UserBookings(Resource):
    @api.response(200, 'User bookings retrieved successfully')
    def get(self, user_id):
        """Get all bookings for a specific user"""
        bookings = facade.get_bookings_by_user(user_id)
        output = []

        for booking in bookings:
            booking_data = {
                'id': str(booking.id),
                'session_id': booking.session_id,
                'booking_date': booking.booking_date.isoformat(),
                'status': booking.status,
                'participants': booking.participants,
                'total_price': booking.total_price,
                'created_at': booking.created_at.isoformat()
            }

            # Add session details
            if hasattr(booking, 'session_r') and booking.session_r:
                booking_data['session'] = {
                    'id': str(booking.session_r.id),
                    'title': booking.session_r.title,
                    'duration': booking.session_r.duration,
                    'session_type': booking.session_r.session_type,
                    'instructor_id': booking.session_r.instructor_id
                }

            output.append(booking_data)

        return output, 200

@api.route('/session/<session_id>')
class SessionBookings(Resource):
    @api.response(200, 'Session bookings retrieved successfully')
    def get(self, session_id):
        """Get all bookings for a specific session"""
        bookings = facade.get_bookings_by_session(session_id)
        output = []

        for booking in bookings:
            booking_data = {
                'id': str(booking.id),
                'user_id': booking.user_id,
                'booking_date': booking.booking_date.isoformat(),
                'status': booking.status,
                'participants': booking.participants,
                'total_price': booking.total_price,
                'created_at': booking.created_at.isoformat()
            }

            # Add user details
            if hasattr(booking, 'user_r') and booking.user_r:
                booking_data['user'] = {
                    'first_name': booking.user_r.first_name,
                    'last_name': booking.user_r.last_name,
                    'email': booking.user_r.email
                }

            output.append(booking_data)

        return output, 200
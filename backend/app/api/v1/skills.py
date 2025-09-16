from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('skills', description='Skill operations')

# Define the skill model for input validation and documentation
skill_model = api.model('Skill', {
    'name': fields.String(required=True, description='Name of the skill'),
    'category': fields.String(required=True, description='Category of the skill'),
    'description': fields.String(required=False, description='Description of the skill')
})

@api.route('/')
class SkillList(Resource):
    @api.expect(skill_model)
    @api.response(201, 'Skill successfully created')
    @api.response(400, 'Skill already exists')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    def post(self):
        """Register a new skill"""
        skill_data = api.payload

        # Check if already exists
        existing_skill = facade.get_skill_by_name(skill_data['name'])
        if existing_skill:
            return {'error': 'Skill already exists'}, 400

        # Make sure we passed in exactly what is needed
        required_keys = ['name', 'category']
        optional_keys = ['description']
        allowed_keys = required_keys + optional_keys

        if not all(key in skill_data for key in required_keys):
            return {'error': 'Missing required fields'}, 400

        if not all(key in allowed_keys for key in skill_data):
            return {'error': 'Invalid input data'}, 400

        # Create the skill
        try:
            new_skill = facade.create_skill(skill_data)
        except ValueError as error:
            return {'error': f"Validation failure: {error}"}, 400

        return {
            'id': str(new_skill.id),
            'name': new_skill.name,
            'category': new_skill.category,
            'description': new_skill.description,
            'message': 'Skill created successfully'
        }, 201

    @api.response(200, 'List of skills retrieved successfully')
    def get(self):
        """Retrieve a list of all skills"""
        all_skills = facade.get_all_skills()
        output = []

        for skill in all_skills:
            output.append({
                'id': str(skill.id),
                'name': skill.name,
                'category': skill.category,
                'description': skill.description,
                'created_at': skill.created_at.isoformat(),
                'updated_at': skill.updated_at.isoformat()
            })

        return output, 200

@api.route('/<skill_id>')
class SkillResource(Resource):
    @api.response(200, 'Skill details retrieved successfully')
    @api.response(404, 'Skill not found')
    def get(self, skill_id):
        """Get skill details by ID"""
        skill = facade.get_skill(skill_id)
        if not skill:
            return {'error': 'Skill not found'}, 404

        output = {
            'id': str(skill.id),
            'name': skill.name,
            'category': skill.category,
            'description': skill.description,
            'created_at': skill.created_at.isoformat(),
            'updated_at': skill.updated_at.isoformat()
        }

        return output, 200

    @api.expect(skill_model)
    @api.response(200, 'Skill updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Skill not found')
    def put(self, skill_id):
        """Update a skill's information"""
        skill_data = api.payload

        # Check that skill exists first
        skill = facade.get_skill(skill_id)
        if not skill:
            return {'error': 'Skill not found'}, 404

        try:
            facade.update_skill(skill_id, skill_data)
        except ValueError as error:
            return {'error': f"Validation failure: {error}"}, 400

        return {'message': 'Skill updated successfully'}, 200

    @api.response(200, 'Skill deleted successfully')
    @api.response(404, 'Skill not found')
    def delete(self, skill_id):
        """Delete a skill"""
        skill = facade.get_skill(skill_id)
        if not skill:
            return {'error': 'Skill not found'}, 404

        facade.delete_skill(skill_id)
        return {'message': 'Skill deleted successfully'}, 200

@api.route('/category/<category>')
class SkillsByCategory(Resource):
    @api.response(200, 'Skills by category retrieved successfully')
    def get(self, category):
        """Get all skills in a specific category"""
        skills = facade.get_skills_by_category(category)
        output = []

        for skill in skills:
            output.append({
                'id': str(skill.id),
                'name': skill.name,
                'category': skill.category,
                'description': skill.description
            })

        return output, 200
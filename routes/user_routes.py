from flask import Blueprint, request, jsonify
from models.user import db, User

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'email')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 
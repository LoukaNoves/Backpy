from Flask import Blueprint, request, jsonify
from utils.input_validator import validaite_input

user_bp = blueprint('user', __name__)

@user_bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    return jsonify({"message": f"Hello, {username}"})


@user_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    validate_input(data, ['username'])
    
    return jsonify({"message": "User created successfully"})

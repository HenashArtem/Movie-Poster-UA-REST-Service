from flask import Blueprint, jsonify, request
from utils import api_util


user_api = Blueprint('user_api', __name__)
USERS_FILENAME = 'users'


@user_api.route('/users', methods=['GET'])
def get_users():
    data = api_util.load_data_from_json_file_by_name(USERS_FILENAME)
    return jsonify({'users': data['users']})


@user_api.route('/users', methods=['POST'])
def add_user():
    data = api_util.load_data_from_json_file_by_name(USERS_FILENAME)
    new_user_data = request.json
    new_user = {
        'id': api_util.get_next_id(data, 'users'),
        'username': new_user_data['username'],
        'email': new_user_data['email']
    }
    data['users'].append(new_user)
    api_util.save_data_in_file_by_filename(data, USERS_FILENAME)
    return jsonify({'message': 'User added successfully'}), 201


@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = api_util.load_data_from_json_file_by_name(USERS_FILENAME)
    user = next((user for user in data['users'] if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@user_api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = api_util.load_data_from_json_file_by_name(USERS_FILENAME)
    user_data = request.json
    for user in data['users']:
        if user['id'] == user_id:
            user.update(user_data)
            api_util.save_data_in_file_by_filename(data, USERS_FILENAME)
            return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404


@user_api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = api_util.load_data_from_json_file_by_name(USERS_FILENAME)
    users = data['users']
    filtered_users = [user for user in users if user['id'] == user_id]
    if not filtered_users:
        return jsonify({'message': 'User not found'}), 404
    data['users'] = [user for user in users if user['id'] != user_id]

    for i, user in enumerate(data['users'], start=1):
        user['id'] = i

    api_util.save_data_in_file_by_filename(data, USERS_FILENAME)
    return jsonify({'message': 'User deleted successfully'}), 200

from flask import Blueprint, jsonify, request
from utils import api_util

screening_api = Blueprint('screening_api', __name__)
SCREENINGS_FILENAME = 'screenings'


@screening_api.route('/screenings', methods=['GET'])
def get_screenings():
    data = api_util.load_data_from_json_file_by_name(SCREENINGS_FILENAME)
    return jsonify({'screenings': data['screenings']})


@screening_api.route('/screenings', methods=['POST'])
def add_screening():
    data = api_util.load_data_from_json_file_by_name(SCREENINGS_FILENAME)
    new_screening_data = request.json
    new_screening_id = api_util.get_next_id(data, 'screenings')
    new_screening_data['id'] = new_screening_id
    data['screenings'].append(new_screening_data)
    api_util.save_data_in_file_by_filename(data, SCREENINGS_FILENAME)
    return jsonify({'message': 'Screening added successfully'}), 201


@screening_api.route('/screenings/<int:screening_id>', methods=['GET'])
def get_screening(screening_id):
    data = api_util.load_data_from_json_file_by_name(SCREENINGS_FILENAME)
    screening = next((screening for screening in data['screenings'] if screening['id'] == screening_id), None)
    if screening:
        return jsonify(screening)
    else:
        return jsonify({'message': 'Screening not found'}), 404


@screening_api.route('/screenings/<int:screening_id>', methods=['PUT'])
def update_screening(screening_id):
    data = api_util.load_data_from_json_file_by_name(SCREENINGS_FILENAME)
    screening_data = request.json
    for screening in data['screenings']:
        if screening['id'] == screening_id:
            screening.update(screening_data)
            api_util.save_data_in_file_by_filename(data, SCREENINGS_FILENAME)
            return jsonify({'message': 'Screening updated successfully'}), 200
    return jsonify({'message': 'Screening not found'}), 404


@screening_api.route('/screenings/<int:screening_id>', methods=['DELETE'])
def delete_screening(screening_id):
    data = api_util.load_data_from_json_file_by_name(SCREENINGS_FILENAME)
    screenings = data['screenings']
    filtered_screenings = [screening for screening in screenings if screening['id'] == screening_id]
    if not filtered_screenings:
        return jsonify({'message': 'Screening not found'}), 404
    data['screenings'] = [screening for screening in screenings if screening['id'] != screening_id]

    for i, screening in enumerate(data['screenings'], start=1):
        screening['id'] = i

    api_util.save_data_in_file_by_filename(data, SCREENINGS_FILENAME)
    return jsonify({'message': 'Screening deleted successfully'}), 200

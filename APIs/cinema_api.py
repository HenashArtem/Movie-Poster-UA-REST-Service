from flask import Blueprint, jsonify, request
from utils import api_util

cinema_api = Blueprint('cinema_api', __name__)
CINEMAS_FILENAME = 'cinemas'


@cinema_api.route('/cinemas', methods=['GET'])
def get_cinemas():
    data = api_util.load_data_from_json_file_by_name(CINEMAS_FILENAME)
    return jsonify({'cinemas': data['cinemas']})


@cinema_api.route('/cinemas', methods=['POST'])
def add_cinema():
    data = api_util.load_data_from_json_file_by_name(CINEMAS_FILENAME)
    new_cinema_data = request.json
    new_cinema = {
        'name': new_cinema_data['name'],
        'location': new_cinema_data['location'],
        'movies_playing': new_cinema_data['movies_playing']
    }
    new_cinema['id'] = api_util.get_next_id(data, 'cinemas')
    data['cinemas'].append(new_cinema)
    api_util.save_data_in_file_by_filename(data, CINEMAS_FILENAME)
    return jsonify({'message': 'Cinema added successfully'}), 201


@cinema_api.route('/cinemas/<int:cinema_id>', methods=['GET'])
def get_cinema(cinema_id):
    data = api_util.load_data_from_json_file_by_name(CINEMAS_FILENAME)
    cinema = next((cinema for cinema in data['cinemas'] if cinema['id'] == cinema_id), None)
    if cinema:
        return jsonify(cinema)
    else:
        return jsonify({'message': 'Cinema not found'}), 404


@cinema_api.route('/cinemas/<int:cinema_id>', methods=['PUT'])
def update_cinema(cinema_id):
    data = api_util.load_data_from_json_file_by_name(CINEMAS_FILENAME)
    cinema_data = request.json
    for cinema in data['cinemas']:
        if cinema['id'] == cinema_id:
            cinema.update(cinema_data)
            api_util.save_data_in_file_by_filename(data, CINEMAS_FILENAME)
            return jsonify({'message': 'Cinema updated successfully'}), 200
    return jsonify({'message': 'Cinema not found'}), 404


@cinema_api.route('/cinemas/<int:cinema_id>', methods=['DELETE'])
def delete_cinema(cinema_id):
    data = api_util.load_data_from_json_file_by_name(CINEMAS_FILENAME)
    cinemas = data['cinemas']
    filtered_cinemas = [cinema for cinema in cinemas if cinema['id'] == cinema_id]
    if not filtered_cinemas:
        return jsonify({'message': 'Cinema not found'}), 404
    data['cinemas'] = [cinema for cinema in cinemas if cinema['id'] != cinema_id]

    for i, cinema in enumerate(data['cinemas'], start=1):
        cinema['id'] = i

    api_util.save_data_in_file_by_filename(data, CINEMAS_FILENAME)
    return jsonify({'message': 'Cinema deleted successfully'}), 200

from flask import Blueprint, jsonify, request
from utils.models import Movie
from utils import api_util


movie_api = Blueprint('movie_api', __name__)
MOVIES_FILENAME = 'movies'


@movie_api.route('/movies', methods=['GET'])
def get_movies():
    data = api_util.load_data_from_json_file_by_name(MOVIES_FILENAME)
    return jsonify({'movies': data['movies']})


@movie_api.route('/movies', methods=['POST'])
def add_movie():
    data = api_util.load_data_from_json_file_by_name(MOVIES_FILENAME)
    new_movie_data = request.json
    new_movie = Movie(new_movie_data['title'], new_movie_data['genre'], new_movie_data['duration'])
    new_movie.id = api_util.get_next_id(data, 'movies')
    data['movies'].append(new_movie.__dict__)
    api_util.save_data_in_file_by_filename(data, MOVIES_FILENAME)
    return jsonify({'message': 'Movie added successfully'}), 201


@movie_api.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    data = api_util.load_data_from_json_file_by_name(MOVIES_FILENAME)
    movie = next((movie for movie in data['movies'] if movie['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    else:
        return jsonify({'message': 'Movie not found'}), 404


@movie_api.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = api_util.load_data_from_json_file_by_name(MOVIES_FILENAME)
    movie_data = request.json
    for movie in data['movies']:
        if movie['id'] == movie_id:
            movie.update(movie_data)
            api_util.save_data_in_file_by_filename(data, MOVIES_FILENAME)
            return jsonify({'message': 'Movie updated successfully'}), 200
    return jsonify({'message': 'Movie not found'}), 404


@movie_api.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    data = api_util.load_data_from_json_file_by_name(MOVIES_FILENAME)
    movies = data['movies']
    filtered_movies = [movie for movie in movies if movie['id'] == movie_id]
    if not filtered_movies:
        return jsonify({'message': 'Movie not found'}), 404
    data['movies'] = [movie for movie in movies if movie['id'] != movie_id]

    for i, movie in enumerate(data['movies'], start=1):
        movie['id'] = i

    api_util.save_data_in_file_by_filename(data, MOVIES_FILENAME)
    return jsonify({'message': 'Movie deleted successfully'}), 200
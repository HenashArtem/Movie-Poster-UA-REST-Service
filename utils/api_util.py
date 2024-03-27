import json


def load_data_from_json_file_by_name(filename):
    with open(f'data/{filename}.json', 'r') as file:
        return json.load(file)


def save_data_in_file_by_filename(data, filename):
    with open(f'data/{filename}.json', 'w') as file:
        json.dump(data, file)


def get_next_id(data, entity_type):
    entities = data.get(entity_type, [])
    if entities:
        return max(entity['id'] for entity in entities) + 1
    else:
        return 1
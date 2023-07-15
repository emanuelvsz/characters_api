from flask import jsonify, request
from src.infra.mock.characters import characters

def getCharacters():
    serialized_characters = []
    for character in characters:
        serialized_character = {
            'id': character['id'],
            'name': character['name'],
            'from_where': character['from_where']
        }
        serialized_characters.append(serialized_character)
    return jsonify(serialized_characters)


def getCharacterByID(id):
    for character in characters:
        if character.get('id') == id:
            return jsonify(character)
    return jsonify({'error': 'Character not found'})

def createCharacter():
    new_character = {
        'id': len(characters) + 1,
        'name': request.json.get('name'),
        'from_where': request.json.get('from_where')
    }
    characters.append(new_character)
    return jsonify(new_character), 201

def editCharacter():
    id = request.json.get('id')
    name = request.json.get('name')
    from_where = request.json.get('from_where')

    if id is None:
        return jsonify({'error': 'Missing character ID'})

    for character in characters:
        if character.get('id') == id:
            if name == "":
                name = character.get('name')
            if from_where == "":
                from_where = character.get('from_where')
            character['name'] = name
            character['from_where'] = from_where
            return jsonify(character)
    return jsonify({'error': 'Character not found'})

def deleteCharacter(id):
    for character in characters:
        if character.get('id') == id:
            characters.remove(character)
            return jsonify(characters)
    return jsonify({'error': 'Character not found'})

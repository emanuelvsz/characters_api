from flask import jsonify, request
from src.infra.mock.characters import characters
import psycopg2

# Função para realizar a conexão com o banco de dados
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="default_database",
            user="postgres",
            password="12345678",
            host="localhost",  # Use o endereço IP do container do banco de dados se necessário
            port="5432"        # A porta padrão do PostgreSQL é 5432
        )
        return connection
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

def getCharacters():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Erro ao conectar ao banco de dados"})

        cursor = connection.cursor()
        cursor.execute("SELECT id, name, from_where FROM characters")
        rows = cursor.fetchall()

        serialized_characters = []
        for row in rows:
            serialized_character = {
                'id': row[0],
                'name': row[1],
                'from_where': row[2]
            }
            serialized_characters.append(serialized_character)

        cursor.close()
        connection.close()

        return jsonify(serialized_characters)

    except Exception as e:
        return jsonify({"error": "Erro ao buscar dados do banco de dados", "details": str(e)})


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

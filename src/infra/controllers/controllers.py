from flask import jsonify, request
from src.infra.mock.characters import characters
from src.domain.messages.repository_messages import *
import psycopg2

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="default_database",
            user="postgres",
            password="12345678",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(ERROR_DB_CONNECTION, e)
        return None

def getCharacters():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": ERROR_DB_CONNECTION})

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
        return jsonify({"error": ERROR_DB_SELECT, "details": str(e)})


def getCharacterByID(id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": ERROR_DB_CONNECTION})

        cursor = connection.cursor()
        cursor.execute("SELECT id, name, from_where FROM characters WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row:
            character = {
                'id': row[0],
                'name': row[1],
                'from_where': row[2]
            }
            return jsonify(character)
        else:
            return jsonify({'error': ERROR_CHARACTER_NOT_FOUND})

    except Exception as e:
        return jsonify({"error": ERROR_DB_SELECT, "details": str(e)})

    finally:
        cursor.close()
        connection.close()


def createCharacter():
    try:
        name = request.json.get('name')
        from_where = request.json.get('from_where')

        connection = get_db_connection()
        if not connection:
            return jsonify({"error": ERROR_DB_CONNECTION})

        cursor = connection.cursor()
        cursor.execute("INSERT INTO characters (name, from_where) VALUES (%s, %s)", (name, from_where))
        connection.commit()

        new_character_id = cursor.lastrowid

        cursor.close()
        connection.close()

        new_character = {
            'id': new_character_id,
            'name': name,
            'from_where': from_where
        }

        return jsonify(new_character), 201

    except Exception as e:
        return jsonify({"error": ERROR_DB_INSERT, "details": str(e)})


def editCharacter():
    id = request.json.get('id')
    name = request.json.get('name')
    from_where = request.json.get('from_where')

    if id is None:
        return jsonify({'error': 'Missing character ID'})

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": ERROR_DB_CONNECTION})

        cursor = connection.cursor()
        cursor.execute("SELECT id, name, from_where FROM characters WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row:
            if not name:
                name = row[1]
            if not from_where:
                from_where = row[2]

            cursor.execute("UPDATE characters SET name = %s, from_where = %s WHERE id = %s",
                           (name, from_where, id))
            connection.commit()

            updated_character = {
                'id': id,
                'name': name,
                'from_where': from_where
            }
            return jsonify(updated_character)

        else:
            return jsonify({'error': ERROR_CHARACTER_NOT_FOUND})

    except Exception as e:
        return jsonify({"error": ERROR_DB_UPDATE, "details": str(e)})

    finally:
        cursor.close()
        connection.close()

def deleteCharacter(id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": ERROR_DB_CONNECTION})

        cursor = connection.cursor()
        cursor.execute("SELECT id, name, from_where FROM characters WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row:
            cursor.execute("DELETE FROM characters WHERE id = %s", (id,))
            connection.commit()
            return jsonify({'message': 'Character deleted successfully'})

        else:
            return jsonify({'error': ERROR_CHARACTER_NOT_FOUND})

    except Exception as e:
        return jsonify({"error": ERROR_DB_DELETE, "details": str(e)})

    finally:
        cursor.close()
        connection.close()


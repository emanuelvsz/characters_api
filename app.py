from flask import Flask
from flask_cors import CORS
from src.infra.controllers.controllers import getCharacters, getCharacterByID, createCharacter, editCharacter, deleteCharacter

app = Flask(__name__)
CORS(app)

@app.route('/characters', methods=['GET'])
def handleGetCharacters():
    return getCharacters()

@app.route('/characters/<string:id>', methods=['GET'])
def handleGetCharacterByID(id):
    return getCharacterByID(id)

@app.route('/characters/new', methods=['POST'])
def handleCreateCharacter():
    return createCharacter()

@app.route('/characters/edit', methods=['PUT'])
def handleEditCharacter():
    return editCharacter()

@app.route('/characters/rm/<string:id>', methods=['DELETE'])
def handleDeleteCharacter(id):
    return deleteCharacter(id)

if __name__ == '__main__':
    app.run(port=5010, host='localhost', debug=True)

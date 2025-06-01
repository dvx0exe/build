from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import uuid

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'davi123',
    'database': 'personagens_bd'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE login = %s AND senha = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return jsonify({'user_id': user['id'], 'username': user['login']}), 200
        else:
            return jsonify({'message': 'Usuário ou senha inválidos!'}), 401
    except Error as e:
        return jsonify({'message': 'Erro ao fazer login!'}), 500

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'message': 'Nome de usuário já existe!'}), 400

        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Registro concluído com sucesso!'}), 201
    except Error as e:
        return jsonify({'message': 'Erro ao registrar!'}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({'message': 'Usuário não encontrado!'}), 404
    except Error as e:
        return jsonify({'message': 'Erro ao buscar usuário!'}), 500

@app.route('/api/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO personagens (
            usuario_id, nome, idade, classe, raca, sexo, vigor, mente, fortitude, forca, 
            destreza, inteligencia, fe, arcano, build_escolhida, equipamento, roupas
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['user_id'], data['nome'], data['idade'], data['classe'], data['raca'], data['sexo'],
            data['vigor'], data['mente'], data['fortitude'], data['forca'], data['destreza'],
            data['inteligencia'], data['fe'], data['arcano'], data['build_escolhida'],
            ','.join(data['equipamento']), ','.join(data['roupas'])
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Personagem criado com sucesso!'}), 201
    except Error as e:
        return jsonify({'message': 'Erro ao criar personagem!'}), 500

@app.route('/api/characters', methods=['GET'])
def get_characters():
    user_id = request.args.get('user_id')
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personagens WHERE usuario_id = %s", (user_id,))
        characters = cursor.fetchall()
        cursor.close()
        connection.close()

        for char in characters:
            char['equipamento'] = char['equipamento'].split(',') if char['equipamento'] else []
            char['roupas'] = char['roupas'].split(',') if char['roupas'] else []
        return jsonify(characters), 200
    except Error as e:
        return jsonify({'message': 'Erro ao buscar personagens!'}), 500

@app.route('/api/characters/<int:id>', methods=['GET'])
def get_character(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personagens WHERE id = %s", (id,))
        character = cursor.fetchone()
        cursor.close()
        connection.close()

        if character:
            character['equipamento'] = character['equipamento'].split(',') if character['equipamento'] else []
            character['roupas'] = character['roupas'].split(',') if character['roupas'] else []
            return jsonify(character), 200
        else:
            return jsonify({'message': 'Personagem não encontrado!'}), 404
    except Error as e:
        return jsonify({'message': 'Erro ao buscar personagem!'}), 500

@app.route('/api/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM personagens WHERE id = %s", (id,))
        if cursor.rowcount > 0:
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Personagem excluído com sucesso!'}), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({'message': 'Personagem não encontrado!'}), 404
    except Error as e:
        return jsonify({'message': 'Erro ao excluir personagem!'}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__, static_folder='.')
CORS(app)
bcrypt = Bcrypt(app)

# Configuração via variáveis de ambiente
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'davi123'),
    'database': os.getenv('DB_NAME', 'personagens_bd')
}

# Pool de conexões
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="app_pool",
    pool_size=5,
    **DB_CONFIG
)

def db_connection(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        conn = connection_pool.get_connection()
        try:
            return f(conn, *args, **kwargs)
        except Error as e:
            print(f"Database error: {e}")
            return jsonify({'message': 'Database error'}), 500
        finally:
            conn.close()
    return decorated

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/login', methods=['POST'])
@db_connection
def login(conn):
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Credenciais inválidas'}), 400

    username = data['username']
    password = data['password']

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, login, senha FROM usuarios WHERE login = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['senha'], password):
            return jsonify({
                'user_id': user['id'],
                'username': user['login']
            }), 200
        return jsonify({'message': 'Credenciais inválidas'}), 401
    except Error as e:
        return jsonify({'message': 'Erro de autenticação'}), 500

@app.route('/api/register', methods=['POST'])
@db_connection
def register(conn):
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400

    username = data['username']
    password = data['password']
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE login = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Usuário já existe'}), 400

        cursor.execute(
            "INSERT INTO usuarios (login, senha) VALUES (%s, %s)",
            (username, hashed_pw)
        )
        conn.commit()
        return jsonify({'message': 'Registro realizado com sucesso'}), 201
    except Error as e:
        conn.rollback()
        return jsonify({'message': 'Erro no registro'}), 500
    finally:
        cursor.close()

@app.route('/api/characters', methods=['POST'])
@db_connection
def create_character(conn):
    data = request.get_json()
    required_fields = [
        'user_id', 'nome', 'idade', 'classe', 'raca', 'sexo', 
        'vigor', 'mente', 'fortitude', 'forca', 'destreza', 
        'inteligencia', 'fe', 'arcano', 'build_escolhida'
    ]
    
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Dados incompletos'}), 400

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO personagens (
            usuario_id, nome, idade, classe, raca, sexo, vigor, mente, 
            fortitude, forca, destreza, inteligencia, fe, arcano, 
            build_escolhida, equipamento, roupas
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['user_id'], data['nome'], data['idade'], data['classe'], 
            data['raca'], data['sexo'], data['vigor'], data['mente'], 
            data['fortitude'], data['forca'], data['destreza'], 
            data['inteligencia'], data['fe'], data['arcano'], 
            data['build_escolhida'],
            ','.join(data.get('equipamento', [])),
            ','.join(data.get('roupas', []))
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({
            'message': 'Personagem criado com sucesso',
            'id': cursor.lastrowid
        }), 201
    except Error as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar personagem'}), 500
    finally:
        cursor.close()

@app.route('/api/characters', methods=['GET'])
@db_connection
def get_characters(conn):
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        return jsonify({'message': 'ID de usuário inválido'}), 400

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personagens WHERE usuario_id = %s", (user_id,))
        characters = cursor.fetchall()
        
        for char in characters:
            for field in ['equipamento', 'roupas']:
                if char[field]:
                    char[field] = char[field].split(',')
        
        return jsonify(characters), 200
    except Error as e:
        return jsonify({'message': 'Erro ao buscar personagens'}), 500
    finally:
        cursor.close()

@app.route('/api/characters/<int:id>', methods=['DELETE'])
@db_connection
def delete_character(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personagens WHERE id = %s", (id,))
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Personagem não encontrado'}), 404
            
        conn.commit()
        return jsonify({'message': 'Personagem excluído com sucesso'}), 200
    except Error as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao excluir personagem'}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
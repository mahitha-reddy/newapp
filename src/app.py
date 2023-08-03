from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app,origins='http://localhost:4200')
# MySQL database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'project'

# Create a table for users (you may add more fields as needed)
def create_table():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']

        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return jsonify({'message': 'User already exists'}), 409

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Signup successful'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

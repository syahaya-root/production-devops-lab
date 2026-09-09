from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define the root route
@app.route('/')
def home():
    return "Hello, World! Welcome to your Flask app."

# Define an API route that returns JSON
@app.route('/health')
def get_data():
    return jsonify({
        "status": "healthy",
        "message": "Data retrieved successfully"
    })
#Connection to postgresql

import os
import psycopg2
from dotenv import load_dotenv

# 1. Muat file .env ke dalam sistem environment
load_dotenv()

# 2. Deklarasikan variabel dengan mengambil nilainya dari .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

@app.route('/services')
def get_services():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        print("Koneksi sukses!")

        cursor = connection.cursor()

        cursor.execute("SELECT id, name, status FROM services")

        rows = cursor.fetchall()
        services = []

        for row in rows:
            services.append({
                 "id": row[0],
                 "name": row[1],
                 "status": row[2]
            })
        print(rows)

        cursor.close()
        connection.close()

        return jsonify(services)

    except Exception as error:
        print(f"Gagal koneksi: {error}")
        return jsonify({"error": str(error)}), 500
# Run the app if this file is executed directly
if __name__ == '__main__':
    # debug=True enables live reloading during development
    app.run(host='0.0.0.0', port=8080, debug=True)


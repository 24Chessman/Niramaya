from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt

# Create a Blueprint for register routes
register_bp = Blueprint('register', __name__)
CORS(register_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@register_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        fname = data.get('fname')
        email = data.get('email')
        password = data.get('password')

        if not email or not fname or not password:
            return jsonify({"success": False, "message": "Email, family name and password are required"}), 400

        hashed_psw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("insert into account_tbl(email, password_hash, family_name) values(%s,%s,%s)", (email, hashed_psw.decode('utf-8'),fname))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Registration successful"}), 200

    except psycopg2.IntegrityError:
        return jsonify({"success": False, "message": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
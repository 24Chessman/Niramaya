from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt

# Create a Blueprint for user login routes
login_bp = Blueprint('login', __name__)
CORS(login_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**db_config)

@login_bp.route('/userlogin', methods=['POST'])
def user_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select password_hash,familyname from account_tbl where email=%s", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            stored_password = row[0]
            familyname = row[1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return jsonify({"success": True, "message": "Login successful", "familyname":familyname, "email":email}), 200
            else:
                return jsonify({"success": False, "message": "Incorrect password"}), 400
        else:
            return jsonify({"success": False, "message": "User not found"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
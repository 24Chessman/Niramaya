from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2

# Create a Blueprint for get user routes
get_user_bp = Blueprint('get_user', __name__)
CORS(get_user_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**db_config)

@get_user_bp.route('/getuser', methods=['POST'])
def get_user():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        if not email or not name:
            return jsonify({"success": False, "message": "Email and name are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select * from members_tbl where name=%s and account_id=(select account_id from account_tbl where email=%s)", (name, email))
        row = cursor.fetchone()

        if row:
            gender = row[3]
            age = row[4]
            height = row[5]
            weight = row[6]
            return jsonify({"success": True, "name": str(name), "gender": str(gender), "age": str(age), "height": str(height), "weight": str(weight)}), 200
        else:
            return jsonify({"success": False, "message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
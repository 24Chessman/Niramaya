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
        member_id = data.get('member_id')
        account_id = data.get('account_id')
        if not member_id or not account_id:
            return jsonify({"success": False, "message": "Email and name are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select * from member_tbl where member_id=%s and account_id=%s", (member_id, account_id))
        row = cursor.fetchone()

        if row:
            name = row[2]
            gender = row[3]
            age = row[4]
            height = row[5]
            weight = row[6]
            return jsonify({"success": True, "message": "Profile fetched successfully", "name": str(name), "gender": str(gender), "age": str(age), "height": str(height), "weight": str(weight)}), 200
        else:
            return jsonify({"success": False, "message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2

# Create a Blueprint for add member routes
add_member_bp = Blueprint('add_member', __name__)
CORS(add_member_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@add_member_bp.route('/addmember', methods=['POST'])
def add_member():
    try:
        data = request.json
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        account_id = data.get('accid')

        if not all([name, gender, age, height, weight, account_id]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO member_tbl (account_id, name, gender, age, height, weight) VALUES (%s, %s, %s, %s, %s, %s) RETURNING member_id",
            (account_id, name, gender, age, height, weight)
        )
        new_member_id = cursor.fetchone()[0]
        conn.commit()

        return jsonify({
            "success": True,
            "member_id": new_member_id,
            "message": "Member added successfully"
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
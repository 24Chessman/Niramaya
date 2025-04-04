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
        accid = data.get('accid')
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        if not accid or not name or not gender or not age or not height or not weight:
            return jsonify({"success": False, "message": "All data is required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("insert into member_tbl(account_id, name, gender, age, height, weight) values(%s,%s,%s,%s,%s,%s)", (accid, name, gender, age, height, weight))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Member added successfully"}), 200
    except psycopg2.errors.ForeignKeyViolation as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except psycopg2.errors.InvalidTextRepresentation as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
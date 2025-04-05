from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2

# Create a Blueprint for member-related routes
member_bp = Blueprint('member', __name__)
CORS(member_bp)

# Database configuration
db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@member_bp.route('/getmembers', methods=['POST'])
def get_members():
    conn = None
    cursor = None
    try:
        # Get account_id from the request body
        data = request.json
        account_id = data.get('account_id')

        if not account_id:
            return jsonify({"success": False, "message": "Account ID is required"}), 400

        # Convert account_id to integer if it's a string (e.g., from JSON)
        account_id = int(account_id)

        # Establish database connection
        conn = connect_db()
        cursor = conn.cursor()

        # Query to fetch all members for the given account_id
        cursor.execute("""
            SELECT member_id, name 
            FROM member_tbl 
            WHERE account_id = %s
        """, (account_id,))
        members = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Prepare member data for response
        members_list = [
            {"member_id": str(member[0]), "name": member[1], "account_id": str(account_id)}
            for member in members
        ]

        # Return success response with member information
        return jsonify({
            "success": True,
            "message": "Members retrieved successfully",
            "members": members_list
        }), 200

    except psycopg2.Error as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"success": False, "message": "Invalid account ID format"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Register the Blueprint (to be added in your main app file, e.g., app.py)
# app.register_blueprint(member_bp)
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2

# Create a Blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__)
CORS(chat_bp)

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

@chat_bp.route('/savechat', methods=['POST'])
def save_chat():
    conn = None
    cursor = None
    try:
        # Get data from the request body
        data = request.json
        account_id = data.get('account_id')
        member_id = data.get('member_id')
        user_input = data.get('user_input')
        bot_response = data.get('bot_response')

        if not all([account_id, member_id, user_input, bot_response]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Convert IDs to integers
        account_id = int(account_id)
        member_id = int(member_id)

        # Establish database connection
        conn = connect_db()
        cursor = conn.cursor()

        # Insert chat history into the database
        cursor.execute("""
            INSERT INTO chat_history_tbl (account_id, member_id, user_input, bot_response)
            VALUES (%s, %s, %s, %s)
            RETURNING history_id
        """, (account_id, member_id, user_input, bot_response))
        
        history_id = cursor.fetchone()[0]
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Chat history saved successfully",
            "history_id": history_id
        }), 200

    except psycopg2.Error as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"success": False, "message": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Register the Blueprint in your main app file (e.g., app.py)
# app.register_blueprint(chat_bp)
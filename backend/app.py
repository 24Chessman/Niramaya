from flask import Flask
from flask_cors import CORS
from routes.register_API import register_bp
from routes.user_login_API import login_bp
from routes.add_member_API import add_member_bp
from routes.remove_user_API import remove_user_bp
from routes.disease_predictor_API import disease_bp
from routes.get_user_API import get_user_bp
from routes.get_members_API import member_bp
from routes.chat_API import chat_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Register Blueprints
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(add_member_bp)
app.register_blueprint(remove_user_bp)
app.register_blueprint(disease_bp)
app.register_blueprint(get_user_bp)
app.register_blueprint(member_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
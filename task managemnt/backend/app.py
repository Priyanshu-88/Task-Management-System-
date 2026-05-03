"""
Task Manager - Main Application Entry Point.
Sets up the Flask server, registers route blueprints,
serves the frontend, and initializes the database.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from models import init_db
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.chatbot import chatbot_bp
import os

# Initialize Flask app with the frontend directory as static folder
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend'),
    static_url_path=''
)

# Enable CORS for all routes (allows frontend to make API requests)
CORS(app)

# ── Register API Blueprints ──────────────────────────────────────
# Auth routes: /api/auth/register, /api/auth/login
app.register_blueprint(auth_bp, url_prefix='/api/auth')
# Task routes: /api/tasks (GET, POST, PUT, DELETE)
app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
# Chatbot route: /api/chatbot (POST)
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')


# ── Serve Frontend Static Files ──────────────────────────────────
@app.route('/')
def serve_index():
    """Serve the login page as the default route."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve any frontend file (HTML, CSS, JS, images)."""
    return send_from_directory(app.static_folder, path)


# ── Application Startup ─────────────────────────────────────────
if __name__ == '__main__':
    # Initialize database tables on first run
    init_db()
    print("=" * 50)
    print("  Task Manager API Server")
    print("  Running on: http://localhost:5000")
    print("=" * 50)
    # Run in debug mode for development (auto-reload on changes)
    app.run(debug=True, port=5000)

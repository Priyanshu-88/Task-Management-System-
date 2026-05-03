"""
Configuration settings for the Task Manager application.
Contains JWT secret key, database path, and token expiry settings.
"""

import os

# Secret key used to sign and verify JWT tokens
# In production, use a strong random key stored in environment variables
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'task-manager-super-secret-key-2024')

# SQLite database file path (stored in the backend directory)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taskmanager.db')

# JWT token expiry duration in hours
TOKEN_EXPIRY_HOURS = 24

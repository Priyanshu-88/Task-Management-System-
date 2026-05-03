"""
Authentication Routes - Handles user registration and login.
Endpoints:
    POST /api/auth/register - Create a new user account
    POST /api/auth/login    - Authenticate and receive JWT token
"""

from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from config import SECRET_KEY, TOKEN_EXPIRY_HOURS
from models import get_db

# Create a Blueprint for auth routes (mounted at /api/auth)
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request Body (JSON):
        - email (string, required): User's email address
        - password (string, required): Password (min 6 characters)
    
    Returns:
        201: User created successfully
        400: Validation error or email already exists
        500: Server error
    """
    data = request.get_json()

    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email'].strip().lower()
    password = data['password']

    # Validate password length
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    # Basic email format validation
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Please enter a valid email address'}), 400

    db = get_db()
    try:
        # Check if email already exists
        existing = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            return jsonify({'error': 'An account with this email already exists'}), 400

        # Hash password using bcrypt (generates salt automatically)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store user with hashed password
        db.execute(
            'INSERT INTO users (email, password) VALUES (?, ?)',
            (email, hashed.decode('utf-8'))
        )
        db.commit()

        return jsonify({'message': 'Account created successfully! Please log in.'}), 201

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed. Please try again.'}), 500
    finally:
        db.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Request Body (JSON):
        - email (string, required): User's email address
        - password (string, required): User's password
    
    Returns:
        200: Login successful with JWT token
        400: Missing fields
        401: Invalid credentials
        500: Server error
    """
    data = request.get_json()

    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email'].strip().lower()
    password = data['password']

    db = get_db()
    try:
        # Find user by email
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password against stored bcrypt hash
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate JWT token with user_id, email, and expiry time
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'email': user['email']
        }), 200

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed. Please try again.'}), 500
    finally:
        db.close()

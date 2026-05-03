"""
JWT Authentication Middleware.
Provides a decorator to protect routes that require authentication.
Extracts and validates the JWT token from the Authorization header.
"""

import jwt
from functools import wraps
from flask import request, jsonify
from config import SECRET_KEY


def token_required(f):
    """
    Decorator that protects routes by requiring a valid JWT token.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user_id):
            # current_user_id is extracted from the JWT payload
            pass
    
    The JWT token must be sent in the Authorization header:
        Authorization: Bearer <token>
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from the Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split(' ')
            # Expecting format: "Bearer <token>"
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        # Return 401 if no token is provided
        if not token:
            return jsonify({'error': 'Authentication token is missing. Please log in.'}), 401

        try:
            # Decode and verify the JWT token using the secret key
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            # Token has passed its expiry time
            return jsonify({'error': 'Token has expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            # Token is malformed or tampered with
            return jsonify({'error': 'Invalid token. Please log in again.'}), 401

        # Pass the authenticated user's ID to the route handler
        return f(current_user_id, *args, **kwargs)

    return decorated

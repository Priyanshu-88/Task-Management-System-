"""
Task Routes - CRUD operations for tasks.
All routes are protected by JWT authentication middleware.
Users can only access their own tasks.

Endpoints:
    GET    /api/tasks          - Get all tasks for the logged-in user
    POST   /api/tasks          - Create a new task
    PUT    /api/tasks/<id>     - Update a task (title, completed, due_date)
    DELETE /api/tasks/<id>     - Delete a task
"""

from flask import Blueprint, request, jsonify
from middleware import token_required
from models import get_db

# Create a Blueprint for task routes (mounted at /api/tasks)
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('', methods=['GET'])
@token_required  # JWT middleware injects current_user_id
def get_tasks(current_user_id):
    """
    Fetch all tasks belonging to the authenticated user.
    Tasks are ordered by creation date (newest first).
    
    Returns:
        200: List of task objects
        500: Server error
    """
    db = get_db()
    try:
        # Only fetch tasks that belong to the current user (security)
        tasks = db.execute(
            'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC',
            (current_user_id,)
        ).fetchall()

        # Convert Row objects to dictionaries for JSON serialization
        return jsonify([dict(task) for task in tasks]), 200

    except Exception as e:
        print(f"Fetch tasks error: {e}")
        return jsonify({'error': 'Failed to fetch tasks'}), 500
    finally:
        db.close()


@tasks_bp.route('', methods=['POST'])
@token_required
def create_task(current_user_id):
    """
    Create a new task for the authenticated user.
    
    Request Body (JSON):
        - title (string, required): Task title
        - due_date (string, optional): Due date in YYYY-MM-DD format
    
    Returns:
        201: Created task object
        400: Missing required fields
        500: Server error
    """
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error': 'Task title is required'}), 400

    title = data['title'].strip()
    if not title:
        return jsonify({'error': 'Task title cannot be empty'}), 400

    due_date = data.get('due_date')  # Optional field

    db = get_db()
    try:
        # Insert task with the current user's ID (ensures ownership)
        cursor = db.execute(
            'INSERT INTO tasks (title, due_date, user_id) VALUES (?, ?, ?)',
            (title, due_date, current_user_id)
        )
        db.commit()

        # Fetch and return the newly created task
        task = db.execute('SELECT * FROM tasks WHERE id = ?', (cursor.lastrowid,)).fetchone()

        return jsonify(dict(task)), 201

    except Exception as e:
        print(f"Create task error: {e}")
        return jsonify({'error': 'Failed to create task'}), 500
    finally:
        db.close()


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user_id, task_id):
    """
    Update an existing task (title, completed status, or due date).
    Only the task owner can update it.
    
    URL Parameters:
        - task_id (int): ID of the task to update
    
    Request Body (JSON):
        - title (string, optional): New task title
        - completed (boolean, optional): New completion status
        - due_date (string, optional): New due date
    
    Returns:
        200: Updated task object
        404: Task not found or not owned by user
        500: Server error
    """
    data = request.get_json()

    db = get_db()
    try:
        # Find task and verify ownership (user can only update their own tasks)
        task = db.execute(
            'SELECT * FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user_id)
        ).fetchone()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Use existing values as defaults if not provided in request
        title = data.get('title', task['title'])
        completed = data.get('completed', task['completed'])
        due_date = data.get('due_date', task['due_date'])

        # Update the task
        db.execute(
            'UPDATE tasks SET title = ?, completed = ?, due_date = ? WHERE id = ? AND user_id = ?',
            (title, completed, due_date, task_id, current_user_id)
        )
        db.commit()

        # Fetch and return the updated task
        updated_task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

        return jsonify(dict(updated_task)), 200

    except Exception as e:
        print(f"Update task error: {e}")
        return jsonify({'error': 'Failed to update task'}), 500
    finally:
        db.close()


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user_id, task_id):
    """
    Delete a task. Only the task owner can delete it.
    
    URL Parameters:
        - task_id (int): ID of the task to delete
    
    Returns:
        200: Success message
        404: Task not found or not owned by user
        500: Server error
    """
    db = get_db()
    try:
        # Find task and verify ownership
        task = db.execute(
            'SELECT * FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user_id)
        ).fetchone()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Delete the task
        db.execute(
            'DELETE FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user_id)
        )
        db.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200

    except Exception as e:
        print(f"Delete task error: {e}")
        return jsonify({'error': 'Failed to delete task'}), 500
    finally:
        db.close()

"""
Chatbot Route - Rule-based chatbot for task management assistance.
Uses keyword/pattern matching to understand user intent and respond accordingly.
Can perform task operations (add, list, summarize) and answer usage questions.

Endpoint:
    POST /api/chatbot  - Send a message and get a bot response
"""

import re
from flask import Blueprint, request, jsonify
from middleware import token_required
from models import get_db

chatbot_bp = Blueprint('chatbot', __name__)

# ── Rule Definitions ─────────────────────────────────────────────
# Each rule has: keywords (triggers), an intent name, and a handler function.
# Rules are checked in order — first match wins.

GREETING_WORDS = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'sup', 'yo']
HELP_WORDS = ['help', 'how to', 'how do i', 'guide', 'tutorial', 'instructions', 'what can you do', 'features', 'commands']
ADD_WORDS = ['add task', 'create task', 'new task', 'add a task', 'create a task', 'make a task', 'add todo', 'remind me to']
LIST_WORDS = ['show tasks', 'list tasks', 'my tasks', 'view tasks', 'show my tasks', 'what are my tasks', 'pending tasks', 'all tasks']
SUMMARY_WORDS = ['summary', 'statistics', 'stats', 'how many tasks', 'task count', 'progress', 'overview', 'status', 'report']
COMPLETE_WORDS = ['completed tasks', 'done tasks', 'finished tasks', 'what did i finish', 'what have i completed']
PENDING_WORDS = ['pending', 'incomplete', 'remaining', 'left to do', 'not done', 'unfinished', 'what do i need to do']
DELETE_WORDS = ['delete task', 'remove task', 'delete a task', 'how to delete', 'remove a task']
DUE_WORDS = ['due date', 'deadline', 'overdue', 'due today', 'upcoming', 'due soon', 'what is due']
TIP_WORDS = ['tip', 'tips', 'advice', 'productivity', 'suggest', 'suggestion', 'motivate', 'motivation', 'inspire']
THANKS_WORDS = ['thanks', 'thank you', 'thx', 'appreciate', 'great', 'awesome', 'nice', 'cool']
BYE_WORDS = ['bye', 'goodbye', 'see you', 'later', 'exit', 'quit', 'close']
FILTER_WORDS = ['filter', 'sort', 'organize', 'categorize', 'how to filter']


def match_intent(message):
    """
    Match user message to an intent using keyword-based rules.
    Returns (intent_name, extracted_data) tuple.
    """
    msg = message.lower().strip()

    # Check for task addition with title extraction
    # e.g., "add task Buy groceries" → extracts "Buy groceries"
    for phrase in ADD_WORDS:
        if phrase in msg:
            # Extract the task title after the trigger phrase
            title = msg.split(phrase, 1)[1].strip()
            # Clean up common filler words
            title = re.sub(r'^(called|named|titled|:|\s)+', '', title).strip()
            if title:
                return ('add_task', {'title': title})
            return ('add_task_prompt', {})

    # Check other intents (order matters — more specific first)
    for word in COMPLETE_WORDS:
        if word in msg:
            return ('completed_tasks', {})

    for word in PENDING_WORDS:
        if word in msg:
            return ('pending_tasks', {})

    for word in DUE_WORDS:
        if word in msg:
            return ('due_info', {})

    for word in SUMMARY_WORDS:
        if word in msg:
            return ('summary', {})

    for word in LIST_WORDS:
        if word in msg:
            return ('list_tasks', {})

    for word in DELETE_WORDS:
        if word in msg:
            return ('delete_help', {})

    for word in FILTER_WORDS:
        if word in msg:
            return ('filter_help', {})

    for word in HELP_WORDS:
        if word in msg:
            return ('help', {})

    for word in TIP_WORDS:
        if word in msg:
            return ('tip', {})

    for word in THANKS_WORDS:
        if word in msg:
            return ('thanks', {})

    for word in BYE_WORDS:
        if word in msg:
            return ('bye', {})

    for word in GREETING_WORDS:
        if msg.startswith(word) or msg == word:
            return ('greeting', {})

    return ('unknown', {})


# ── Response Handlers ────────────────────────────────────────────

import random

TIPS = [
    "💡 Break large tasks into smaller sub-tasks — it makes them less overwhelming!",
    "💡 Try the 2-minute rule: if a task takes less than 2 minutes, do it right away.",
    "💡 Set due dates for important tasks so you never miss a deadline.",
    "💡 Review your completed tasks at the end of the day — it boosts motivation!",
    "💡 Tackle your hardest task first thing in the morning when your energy is highest.",
    "💡 Use the Pomodoro technique: 25 min focused work, then a 5 min break.",
    "💡 Prioritize tasks: not everything is equally urgent. Focus on what matters most.",
    "💡 Celebrate small wins — completing tasks deserves recognition! 🎉",
]


def handle_greeting(user_id):
    return "👋 Hello! I'm your Task Manager assistant. I can help you add tasks, check your progress, and stay productive. Type **help** to see what I can do!"


def handle_help(user_id):
    return (
        "🤖 **Here's what I can help you with:**\n\n"
        "• **\"Add task [title]\"** — Create a new task\n"
        "• **\"Show my tasks\"** — List your current tasks\n"
        "• **\"Summary\"** — Get task statistics\n"
        "• **\"Pending tasks\"** — See incomplete tasks\n"
        "• **\"Completed tasks\"** — See finished tasks\n"
        "• **\"Due dates\"** — Check upcoming deadlines\n"
        "• **\"Tips\"** — Get productivity advice\n"
        "• **\"How to delete\"** — Learn to delete tasks\n"
        "• **\"How to filter\"** — Learn to filter tasks\n\n"
        "Just type naturally — I'll do my best to understand! 😊"
    )


def handle_add_task(user_id, title):
    """Actually create a task via the chatbot."""
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO tasks (title, user_id) VALUES (?, ?)',
            (title, user_id)
        )
        db.commit()
        return f"✅ Task created: **\"{title}\"**\n\nYour task list will refresh automatically."
    except Exception as e:
        return "❌ Sorry, I couldn't create that task. Please try again."
    finally:
        db.close()


def handle_add_task_prompt(user_id):
    return "📝 Sure! What's the task title? Say something like:\n**\"Add task Buy groceries\"**"


def handle_list_tasks(user_id):
    db = get_db()
    try:
        tasks = db.execute(
            'SELECT title, completed, due_date FROM tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT 10',
            (user_id,)
        ).fetchall()

        if not tasks:
            return "📋 You don't have any tasks yet. Try saying **\"Add task [title]\"** to create one!"

        lines = ["📋 **Your recent tasks:**\n"]
        for t in tasks:
            status = "✅" if t['completed'] else "⬜"
            due = f" (due: {t['due_date']})" if t['due_date'] else ""
            lines.append(f"{status} {t['title']}{due}")

        return "\n".join(lines)
    finally:
        db.close()


def handle_summary(user_id):
    db = get_db()
    try:
        total = db.execute('SELECT COUNT(*) as c FROM tasks WHERE user_id = ?', (user_id,)).fetchone()['c']
        completed = db.execute('SELECT COUNT(*) as c FROM tasks WHERE user_id = ? AND completed = 1', (user_id,)).fetchone()['c']
        pending = total - completed

        if total == 0:
            return "📊 You have no tasks yet. Start by adding some tasks!"

        pct = round((completed / total) * 100) if total > 0 else 0
        bar_filled = round(pct / 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)

        return (
            f"📊 **Task Summary:**\n\n"
            f"Total tasks: **{total}**\n"
            f"Completed: **{completed}** ✅\n"
            f"Pending: **{pending}** ⏳\n\n"
            f"Progress: [{bar}] **{pct}%**\n\n"
            f"{'🎉 Great job! You are making excellent progress!' if pct >= 75 else '💪 Keep going! You can do it!' if pct >= 25 else '🚀 Time to get started — you got this!'}"
        )
    finally:
        db.close()


def handle_completed_tasks(user_id):
    db = get_db()
    try:
        tasks = db.execute(
            'SELECT title FROM tasks WHERE user_id = ? AND completed = 1 ORDER BY created_at DESC LIMIT 10',
            (user_id,)
        ).fetchall()

        if not tasks:
            return "You haven't completed any tasks yet. Keep pushing! 💪"

        lines = ["✅ **Completed tasks:**\n"]
        for t in tasks:
            lines.append(f"• {t['title']}")
        lines.append(f"\n🎉 You've completed **{len(tasks)}** task(s)! Nice work!")
        return "\n".join(lines)
    finally:
        db.close()


def handle_pending_tasks(user_id):
    db = get_db()
    try:
        tasks = db.execute(
            'SELECT title, due_date FROM tasks WHERE user_id = ? AND completed = 0 ORDER BY created_at DESC LIMIT 10',
            (user_id,)
        ).fetchall()

        if not tasks:
            return "🎉 No pending tasks — you're all caught up! Time to relax or add new goals."

        lines = ["⏳ **Pending tasks:**\n"]
        for t in tasks:
            due = f" *(due: {t['due_date']})*" if t['due_date'] else ""
            lines.append(f"• {t['title']}{due}")
        lines.append(f"\nYou have **{len(tasks)}** task(s) to complete. You got this! 💪")
        return "\n".join(lines)
    finally:
        db.close()


def handle_due_info(user_id):
    db = get_db()
    try:
        tasks = db.execute(
            "SELECT title, due_date FROM tasks WHERE user_id = ? AND due_date IS NOT NULL AND completed = 0 ORDER BY due_date ASC LIMIT 10",
            (user_id,)
        ).fetchall()

        if not tasks:
            return "📅 No upcoming deadlines! You can set due dates when adding tasks from the dashboard."

        lines = ["📅 **Upcoming deadlines:**\n"]
        for t in tasks:
            lines.append(f"• **{t['due_date']}** — {t['title']}")
        return "\n".join(lines)
    finally:
        db.close()


def handle_delete_help(user_id):
    return (
        "🗑️ **How to delete a task:**\n\n"
        "1. Hover over the task in your task list\n"
        "2. Click the 🗑 (trash) icon that appears on the right\n"
        "3. Confirm the deletion in the popup\n\n"
        "Note: Deleted tasks cannot be recovered."
    )


def handle_filter_help(user_id):
    return (
        "🔍 **How to filter tasks:**\n\n"
        "Use the filter buttons above your task list:\n"
        "• **All** — Shows all your tasks\n"
        "• **Pending** — Shows only incomplete tasks\n"
        "• **Completed** — Shows only finished tasks\n\n"
        "This helps you focus on what needs attention!"
    )


def handle_tip(user_id):
    return random.choice(TIPS)


def handle_thanks(user_id):
    responses = [
        "You're welcome! Happy to help! 😊",
        "Glad I could assist! Keep up the great work! 🌟",
        "Anytime! Let me know if you need anything else. 💪",
        "No problem! You're doing great! 🎉"
    ]
    return random.choice(responses)


def handle_bye(user_id):
    return "👋 Goodbye! Stay productive and come back anytime you need help!"


def handle_unknown(user_id):
    responses = [
        "🤔 I'm not sure I understand. Type **help** to see what I can do!",
        "Hmm, I didn't catch that. Try asking about your **tasks**, **summary**, or say **help**!",
        "I'm still learning! Try saying things like **\"add task\"**, **\"show tasks\"**, or **\"tips\"**."
    ]
    return random.choice(responses)


# ── Intent → Handler Mapping ─────────────────────────────────────
HANDLERS = {
    'greeting': handle_greeting,
    'help': handle_help,
    'add_task_prompt': handle_add_task_prompt,
    'list_tasks': handle_list_tasks,
    'summary': handle_summary,
    'completed_tasks': handle_completed_tasks,
    'pending_tasks': handle_pending_tasks,
    'due_info': handle_due_info,
    'delete_help': handle_delete_help,
    'filter_help': handle_filter_help,
    'tip': handle_tip,
    'thanks': handle_thanks,
    'bye': handle_bye,
    'unknown': handle_unknown,
}


# ── Chatbot API Endpoint ─────────────────────────────────────────

@chatbot_bp.route('', methods=['POST'])
@token_required
def chat(current_user_id):
    """
    Process a user message and return a bot response.
    
    Request Body (JSON):
        - message (string, required): The user's message
    
    Returns:
        200: { reply: "bot response text", intent: "detected_intent", task_added: bool }
    """
    data = request.get_json()

    if not data or not data.get('message'):
        return jsonify({'error': 'Message is required'}), 400

    message = data['message'].strip()
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Match user intent from the message
    intent, extracted = match_intent(message)

    # Special case: add_task with extracted title
    if intent == 'add_task':
        reply = handle_add_task(current_user_id, extracted['title'])
        return jsonify({
            'reply': reply,
            'intent': intent,
            'task_added': True  # Signal frontend to refresh task list
        }), 200

    # Handle all other intents
    handler = HANDLERS.get(intent, handle_unknown)
    reply = handler(current_user_id)

    return jsonify({
        'reply': reply,
        'intent': intent,
        'task_added': False
    }), 200

# Task Manager — Full-Stack Application

A full-stack task management app built with **Flask**, **SQLite**, **Vanilla JS**, and **JWT authentication**.

## Features

- 🔐 User registration & login with JWT authentication
- 🔒 Passwords hashed with bcrypt
- ✅ Create, read, update, delete tasks (CRUD)
- 📅 Due date support for tasks
- 🎯 Filter tasks: All / Pending / Completed
- 📊 Dashboard with task statistics
- 🚪 Logout functionality
- 🤖 Rule-based chatbot assistant
- 🎨 Premium dark-themed UI with glassmorphism

## Project Structure

```
task managemnt/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py           # JWT secret, DB config
│   ├── models.py           # Database schema & helpers
│   ├── middleware.py        # JWT auth decorator
│   ├── requirements.txt    # Python dependencies
│   └── routes/
│       ├── __init__.py
│       ├── auth.py         # /api/auth/register, /api/auth/login
│       ├── tasks.py        # /api/tasks CRUD
│       └── chatbot.py      # Rule-based chatbot logic
├── frontend/
│   ├── index.html          # Login page
│   ├── register.html       # Signup page
│   ├── dashboard.html      # Task dashboard
│   ├── css/
│   │   └── style.css       # Premium dark theme
│   └── js/
│       ├── auth.js         # Login/register logic
│       ├── dashboard.js    # Task CRUD & filtering
│       └── chatbot.js      # Floating chat widget
└── README.md
```

## How to Run

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the server

```bash
python app.py
```

### 3. Open in browser

Visit: **http://localhost:5000**

## API Endpoints

| Method | Endpoint             | Auth | Description          |
|--------|----------------------|------|----------------------|
| POST   | /api/auth/register   | ❌   | Register new user    |
| POST   | /api/auth/login      | ❌   | Login, get JWT token |
| GET    | /api/tasks           | ✅   | Get user's tasks     |
| POST   | /api/tasks           | ✅   | Create a task        |
| PUT    | /api/tasks/:id       | ✅   | Update a task        |
| DELETE | /api/tasks/:id       | ✅   | Delete a task        |
| POST   | /api/chatbot         | ✅   | Chat with assistant  |

## Chatbot Assistant

The app includes a **rule-based chatbot** accessible via the 💬 floating button on the dashboard. It helps users:

| Command | What it does |
|---|---|
| `help` | Lists all available commands |
| `add task Buy groceries` | Creates a task directly from chat |
| `show my tasks` | Lists your recent tasks |
| `summary` / `stats` | Shows task completion stats with progress bar |
| `pending tasks` | Shows only incomplete tasks |
| `completed tasks` | Shows only finished tasks |
| `due dates` | Shows upcoming deadlines |
| `tips` | Get a random productivity tip |
| `how to delete` | Explains how to delete tasks |
| `how to filter` | Explains how to use filters |

## Security

- JWT tokens expire after 24 hours
- Passwords are hashed using bcrypt
- Users can only access their own tasks
- Token is sent via `Authorization: Bearer <token>` header

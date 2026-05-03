🚀 Task Manager — Full-Stack Productivity App

A modern full-stack task management application built using Flask, SQLite, and Vanilla JavaScript, featuring secure JWT authentication and an interactive chatbot assistant to improve user productivity.

📌 Table of Contents
Features
Tech Stack
Project Structure
Installation & Setup
API Endpoints
Chatbot Commands
Security
Screenshots (optional)
Future Improvements
✨ Features
🔐 User Authentication (JWT-based login & signup)
🔒 Secure password hashing using bcrypt
📋 Task Management (Create, Read, Update, Delete)
📅 Due date support for tasks
🎯 Task filtering (All / Pending / Completed)
📊 Dashboard with task statistics
🤖 Rule-based chatbot assistant
🚪 Logout functionality
🎨 Modern dark UI with glassmorphism
🛠️ Tech Stack

Frontend:

HTML
CSS
JavaScript

Backend:

Flask (Python)

Database:

SQLite

Authentication & Security:

JWT (JSON Web Tokens)
bcrypt
📁 Project Structure
task-manager/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── middleware.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       ├── tasks.py
│       └── chatbot.py
│
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       ├── dashboard.js
│       └── chatbot.js
│
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/task-manager.git
cd task-manager
2️⃣ Setup backend
cd backend
pip install -r requirements.txt
3️⃣ Run the server
python app.py
4️⃣ Open in browser
http://localhost:5000
🔗 API Endpoints
Method	Endpoint	Auth	Description
POST	/api/auth/register	❌	Register user
POST	/api/auth/login	❌	Login & get token
GET	/api/tasks	✅	Fetch tasks
POST	/api/tasks	✅	Create task
PUT	/api/tasks/:id	✅	Update task
DELETE	/api/tasks/:id	✅	Delete task
POST	/api/chatbot	✅	Chat with assistant
🤖 Chatbot Commands
Command	Description
help	Show all commands
add task <task>	Create a new task
show my tasks	List tasks
pending tasks	Show incomplete tasks
completed tasks	Show completed tasks
summary / stats	Show task statistics
due dates	Show upcoming deadlines
tips	Get productivity tips
how to delete	Help with deleting tasks
how to filter	Help with filtering
🔐 Security
JWT tokens expire after 24 hours
Passwords are hashed using bcrypt
Protected routes using authentication middleware
Users can only access their own tasks
Token passed via Authorization: Bearer <token>
📸 Screenshots (Optional)

Add screenshots or GIFs here to showcase UI

🚀 Future Improvements
🤖 AI-powered chatbot (NLP-based)
🔄 Real-time updates using WebSockets
🔔 Task reminders & notifications
📱 Mobile responsiveness
☁️ Deployment (Docker / Cloud)

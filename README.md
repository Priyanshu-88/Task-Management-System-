<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Task Manager — Full-Stack App</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      line-height: 1.6;
      padding: 20px;
    }
    h1, h2, h3 {
      color: #38bdf8;
    }
    code, pre {
      background: #1e293b;
      padding: 10px;
      border-radius: 8px;
      display: block;
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    table, th, td {
      border: 1px solid #334155;
    }
    th, td {
      padding: 10px;
      text-align: left;
    }
    ul {
      margin-left: 20px;
    }
  </style>
</head>
<body>

<h1>🚀 Task Manager — Full-Stack Productivity App</h1>

<p>
A modern full-stack task management application built using 
<strong>Flask, SQLite, and Vanilla JavaScript</strong>, featuring secure 
<strong>JWT authentication</strong> and an interactive chatbot assistant.
</p>

<hr>

<h2>✨ Features</h2>
<ul>
  <li>🔐 User Authentication (JWT-based login & signup)</li>
  <li>🔒 Secure password hashing using bcrypt</li>
  <li>📋 Task Management (CRUD)</li>
  <li>📅 Due date support</li>
  <li>🎯 Task filtering (All / Pending / Completed)</li>
  <li>📊 Dashboard with statistics</li>
  <li>🤖 Rule-based chatbot assistant</li>
  <li>🚪 Logout functionality</li>
  <li>🎨 Modern dark UI</li>
</ul>

<h2>🛠️ Tech Stack</h2>

<h3>Frontend</h3>
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Flask (Python)</li>
</ul>

<h3>Database</h3>
<ul>
  <li>SQLite</li>
</ul>

<h3>Authentication</h3>
<ul>
  <li>JWT</li>
  <li>bcrypt</li>
</ul>

<h2>📁 Project Structure</h2>

<pre>
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
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── css/style.css
│   └── js/
│       ├── auth.js
│       ├── dashboard.js
│       └── chatbot.js
└── README.md
</pre>

<h2>⚙️ Installation & Setup</h2>

<h3>1. Clone Repository</h3>
<pre>
git clone https://github.com/your-username/task-manager.git
cd task-manager
</pre>

<h3>2. Setup Backend</h3>
<pre>
cd backend
pip install -r requirements.txt
</pre>

<h3>3. Run Server</h3>
<pre>
python app.py
</pre>

<h3>4. Open Browser</h3>
<pre>
http://localhost:5000
</pre>

<h2>🔗 API Endpoints</h2>

<table>
<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Auth</th>
<th>Description</th>
</tr>
<tr><td>POST</td><td>/api/auth/register</td><td>❌</td><td>Register user</td></tr>
<tr><td>POST</td><td>/api/auth/login</td><td>❌</td><td>Login & get token</td></tr>
<tr><td>GET</td><td>/api/tasks</td><td>✅</td><td>Fetch tasks</td></tr>
<tr><td>POST</td><td>/api/tasks</td><td>✅</td><td>Create task</td></tr>
<tr><td>PUT</td><td>/api/tasks/:id</td><td>✅</td><td>Update task</td></tr>
<tr><td>DELETE</td><td>/api/tasks/:id</td><td>✅</td><td>Delete task</td></tr>
<tr><td>POST</td><td>/api/chatbot</td><td>✅</td><td>Chat with assistant</td></tr>
</table>

<h2>🤖 Chatbot Commands</h2>

<ul>
  <li><code>help</code> — Show commands</li>
  <li><code>add task &lt;task&gt;</code> — Create task</li>
  <li><code>show my tasks</code> — List tasks</li>
  <li><code>pending tasks</code></li>
  <li><code>completed tasks</code></li>
  <li><code>summary / stats</code></li>
  <li><code>due dates</code></li>
  <li><code>tips</code></li>
</ul>

<h2>🔐 Security</h2>
<ul>
  <li>JWT tokens expire after 24 hours</li>
  <li>Password hashing with bcrypt</li>
  <li>Protected routes using middleware</li>
  <li>User-specific data access</li>
</ul>

<h2>🚀 Future Improvements</h2>
<ul>
  <li>AI-powered chatbot</li>
  <li>Real-time updates (WebSockets)</li>
  <li>Notifications & reminders</li>
  <li>Mobile responsiveness</li>
  <li>Cloud deployment</li>
</ul>

</body>
</html>

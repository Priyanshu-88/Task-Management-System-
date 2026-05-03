/**
 * dashboard.js - Task Dashboard Logic
 * Handles: fetching tasks, adding, toggling, deleting, and filtering.
 * All API calls include the JWT token in the Authorization header.
 */

const API_BASE = window.location.origin + '/api';
const token = localStorage.getItem('token');
const userEmail = localStorage.getItem('userEmail');

// ── Auth Guard: redirect to login if no token ──────
if (!token) {
    window.location.href = 'index.html';
}

// ── Display user email in navbar ────────────────────
document.getElementById('userEmail').textContent = '👤 ' + (userEmail || 'User');

// ── State ───────────────────────────────────────────
let allTasks = [];
let currentFilter = 'all';

// ── Helper: Auth Headers ────────────────────────────
function authHeaders() {
    // Send JWT token in Authorization header: Bearer <token>
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// ── Helper: Show Dashboard Alert ────────────────────
function showDashAlert(message, type = 'error') {
    const alert = document.getElementById('dashAlert');
    alert.textContent = message;
    alert.className = `alert show alert-${type}`;
    setTimeout(() => { alert.classList.remove('show'); }, 4000);
}

// ── Logout ──────────────────────────────────────────
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = 'index.html';
}

// ── Update Stats Cards ──────────────────────────────
function updateStats() {
    const total = allTasks.length;
    const completed = allTasks.filter(t => t.completed).length;
    const pending = total - completed;
    document.getElementById('totalCount').textContent = total;
    document.getElementById('completedCount').textContent = completed;
    document.getElementById('pendingCount').textContent = pending;
}

// ── Format Date ─────────────────────────────────────
function formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function isOverdue(dateStr) {
    if (!dateStr) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return new Date(dateStr + 'T00:00:00') < today;
}

// ── Render Tasks ────────────────────────────────────
function renderTasks() {
    const taskList = document.getElementById('taskList');
    let filtered = allTasks;

    // Apply filter
    if (currentFilter === 'completed') {
        filtered = allTasks.filter(t => t.completed);
    } else if (currentFilter === 'pending') {
        filtered = allTasks.filter(t => !t.completed);
    }

    // Empty state
    if (filtered.length === 0) {
        const msg = currentFilter === 'all' ? 'No tasks yet. Add one above!' :
                    currentFilter === 'completed' ? 'No completed tasks.' : 'No pending tasks.';
        taskList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <h3>${msg}</h3>
                <p>Your tasks will appear here</p>
            </div>`;
        updateStats();
        return;
    }

    // Build task HTML
    taskList.innerHTML = filtered.map(task => {
        const overdue = !task.completed && isOverdue(task.due_date);
        return `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <input type="checkbox" class="task-checkbox" 
                ${task.completed ? 'checked' : ''} 
                onchange="toggleTask(${task.id}, ${task.completed ? 0 : 1})"
                title="Mark as ${task.completed ? 'pending' : 'complete'}">
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-meta">
                    ${task.due_date ? `<span class="task-due ${overdue ? 'overdue' : ''}">📅 ${formatDate(task.due_date)}${overdue ? ' (Overdue)' : ''}</span>` : ''}
                </div>
            </div>
            <div class="task-actions">
                <button class="btn-icon delete" onclick="deleteTask(${task.id})" title="Delete task">🗑</button>
            </div>
        </div>`;
    }).join('');

    updateStats();
}

// ── Escape HTML to prevent XSS ──────────────────────
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ── Fetch All Tasks (GET /api/tasks) ────────────────
async function fetchTasks() {
    try {
        const res = await fetch(`${API_BASE}/tasks`, {
            headers: authHeaders()
        });

        if (res.status === 401) {
            logout(); // Token expired or invalid
            return;
        }

        const data = await res.json();
        if (res.ok) {
            allTasks = data;
            renderTasks();
        } else {
            showDashAlert(data.error || 'Failed to fetch tasks');
        }
    } catch (err) {
        showDashAlert('Network error. Is the server running?');
    }
}

// ── Add Task (POST /api/tasks) ──────────────────────
document.getElementById('addTaskForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const titleInput = document.getElementById('taskTitle');
    const dueDateInput = document.getElementById('taskDueDate');
    const title = titleInput.value.trim();
    const due_date = dueDateInput.value || null;

    if (!title) return;

    const btn = document.getElementById('addTaskBtn');
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({ title, due_date })
        });

        if (res.status === 401) { logout(); return; }

        const data = await res.json();
        if (res.ok) {
            allTasks.unshift(data); // Add to beginning of list
            renderTasks();
            titleInput.value = '';
            dueDateInput.value = '';
            showDashAlert('Task added!', 'success');
        } else {
            showDashAlert(data.error || 'Failed to add task');
        }
    } catch (err) {
        showDashAlert('Network error');
    } finally {
        btn.disabled = false;
    }
});

// ── Toggle Task Completion (PUT /api/tasks/:id) ─────
async function toggleTask(taskId, newStatus) {
    try {
        const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PUT',
            headers: authHeaders(),
            body: JSON.stringify({ completed: newStatus })
        });

        if (res.status === 401) { logout(); return; }

        if (res.ok) {
            const updated = await res.json();
            const idx = allTasks.findIndex(t => t.id === taskId);
            if (idx !== -1) allTasks[idx] = updated;
            renderTasks();
        } else {
            showDashAlert('Failed to update task');
        }
    } catch (err) {
        showDashAlert('Network error');
    }
}

// ── Delete Task (DELETE /api/tasks/:id) ─────────────
async function deleteTask(taskId) {
    if (!confirm('Delete this task?')) return;

    try {
        const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: authHeaders()
        });

        if (res.status === 401) { logout(); return; }

        if (res.ok) {
            allTasks = allTasks.filter(t => t.id !== taskId);
            renderTasks();
            showDashAlert('Task deleted', 'success');
        } else {
            showDashAlert('Failed to delete task');
        }
    } catch (err) {
        showDashAlert('Network error');
    }
}

// ── Filter Tasks ────────────────────────────────────
function setFilter(filter) {
    currentFilter = filter;
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    renderTasks();
}

// ── Initialize Dashboard ────────────────────────────
fetchTasks();

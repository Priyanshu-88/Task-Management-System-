/**
 * chatbot.js - Floating Chat Widget for Task Manager
 * Sends messages to POST /api/chatbot and displays bot responses.
 * If the bot creates a task, it signals the dashboard to refresh.
 */

const CHAT_API = window.location.origin + '/api/chatbot';

// ── Build Chat Widget HTML ──────────────────────────
function initChatWidget() {
    const widget = document.createElement('div');
    widget.innerHTML = `
    <div class="chat-fab" id="chatFab" onclick="toggleChat()" title="Chat Assistant">
        <span class="chat-fab-icon" id="chatFabIcon">💬</span>
    </div>
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <div class="chat-header-info">
                <span class="chat-avatar">🤖</span>
                <div>
                    <div class="chat-header-title">Task Assistant</div>
                    <div class="chat-header-status">Online — Ask me anything</div>
                </div>
            </div>
            <button class="chat-close" onclick="toggleChat()">&times;</button>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="chat-msg bot">
                <div class="chat-bubble">
                    Hi! I'm your task assistant. I can help you manage tasks, view your progress, or give productivity tips.<br><br>
                    Type <strong>help</strong> to see what I can do!
                </div>
            </div>
        </div>
        <form class="chat-input-area" id="chatForm" onsubmit="sendChatMessage(event)">
            <input type="text" id="chatInput" placeholder="Type a message..." autocomplete="off">
            <button type="submit" class="chat-send-btn">➤</button>
        </form>
    </div>`;
    document.body.appendChild(widget);
}

// ── Toggle Chat Open/Close ──────────────────────────
function toggleChat() {
    const win = document.getElementById('chatWindow');
    const fab = document.getElementById('chatFab');
    const icon = document.getElementById('chatFabIcon');
    const isOpen = win.classList.toggle('open');
    fab.classList.toggle('active', isOpen);
    icon.textContent = isOpen ? '✕' : '💬';
    if (isOpen) {
        document.getElementById('chatInput').focus();
    }
}

// ── Add Message to Chat ─────────────────────────────
function addMessage(text, sender) {
    const body = document.getElementById('chatBody');
    const div = document.createElement('div');
    div.className = `chat-msg ${sender}`;

    // Convert markdown-like bold (**text**) to <strong>
    const formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

    div.innerHTML = `<div class="chat-bubble">${formatted}</div>`;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
}

// ── Show Typing Indicator ───────────────────────────
function showTyping() {
    const body = document.getElementById('chatBody');
    const div = document.createElement('div');
    div.className = 'chat-msg bot typing-indicator';
    div.id = 'typingIndicator';
    div.innerHTML = `<div class="chat-bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>`;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
}

// ── Send Message to Backend ─────────────────────────
async function sendChatMessage(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    // Show user message
    addMessage(message, 'user');
    input.value = '';

    // Show typing animation
    showTyping();

    try {
        const res = await fetch(CHAT_API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ message })
        });

        hideTyping();

        if (res.status === 401) {
            addMessage('Session expired. Please log in again.', 'bot');
            return;
        }

        const data = await res.json();
        addMessage(data.reply, 'bot');

        // If chatbot added a task, refresh the task list on dashboard
        if (data.task_added && typeof fetchTasks === 'function') {
            fetchTasks();
        }
    } catch (err) {
        hideTyping();
        addMessage('Network error. Please make sure the server is running.', 'bot');
    }
}

// ── Initialize on page load ─────────────────────────
initChatWidget();

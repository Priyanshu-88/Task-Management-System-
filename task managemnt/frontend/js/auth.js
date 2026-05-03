/**
 * auth.js - Handles Login and Registration form submissions.
 * Uses the Fetch API to communicate with the Flask backend.
 * Stores JWT token in localStorage on successful login.
 */

const API_BASE = window.location.origin + '/api';

// ── Helper: Show Alert Message ──────────────────────
function showAlert(message, type = 'error') {
    const alert = document.getElementById('alert');
    alert.textContent = message;
    alert.className = `alert show alert-${type}`;
    // Auto-hide after 5 seconds
    setTimeout(() => { alert.classList.remove('show'); }, 5000);
}

// ── Redirect if already logged in ───────────────────
if (localStorage.getItem('token')) {
    window.location.href = 'dashboard.html';
}

// ── Login Form Handler ──────────────────────────────
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const btn = document.getElementById('loginBtn');

        // Disable button and show loading state
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Signing in...';

        try {
            // POST /api/auth/login with email and password
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                // Store JWT token and user email in localStorage
                localStorage.setItem('token', data.token);
                localStorage.setItem('userEmail', data.email);
                // Redirect to dashboard
                window.location.href = 'dashboard.html';
            } else {
                showAlert(data.error || 'Login failed');
            }
        } catch (err) {
            showAlert('Network error. Is the server running?');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Sign In';
        }
    });
}

// ── Register Form Handler ───────────────────────────
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const btn = document.getElementById('registerBtn');

        // Client-side validation: passwords must match
        if (password !== confirmPassword) {
            showAlert('Passwords do not match');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Creating account...';

        try {
            // POST /api/auth/register with email and password
            const res = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                showAlert(data.message || 'Account created! Redirecting...', 'success');
                // Redirect to login page after short delay
                setTimeout(() => { window.location.href = 'index.html'; }, 1500);
            } else {
                showAlert(data.error || 'Registration failed');
            }
        } catch (err) {
            showAlert('Network error. Is the server running?');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Create Account';
        }
    });
}

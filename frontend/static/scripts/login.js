const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const messageBox = document.getElementById('messageBox');

const VALID_USERS = [
    {
        email: 'admin@flashai.com',
        password: 'Password123',
        name: 'Admin User'
    },
    {
        email: 'guest@flashai.com',
        password: 'guest',
        name: 'Guest'
    }
];

function getStoredUser() {
    try {
        return JSON.parse(localStorage.getItem('flashaiUser'));
    } catch {
        return null;
    }
}

function redirectToDashboard() {
    window.location.href = 'dashboard.html';
}

function showMessage(text, isError = false) {
    messageBox.textContent = text;
    messageBox.className = isError ? 'message error' : 'message success';
}

function handleLogin(event) {
    event.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
        showMessage('Please enter both email and password.', true);
        return;
    }

    const user = VALID_USERS.find(
        user => user.email === email && user.password === password
    );

    if (!user) {
        showMessage('Invalid credentials. Try admin@flashai.com / Password123.', true);
        return;
    }

    localStorage.setItem(
        'flashaiUser',
        JSON.stringify({ email: user.email, name: user.name })
    );

    showMessage('Login successful. Redirecting...', false);

    setTimeout(redirectToDashboard, 700);
}

function initialize() {
    const storedUser = getStoredUser();
    if (storedUser && storedUser.email) {
        redirectToDashboard();
        return;
    }

    loginForm.addEventListener('submit', handleLogin);
}

initialize();

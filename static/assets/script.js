function login() {
    const form = document.getElementById('loginForm');
    const formData = new FormData(form);

    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.error) {
            messageDiv.style.display = 'block';
            messageDiv.innerHTML = `<span class="error-message">${data.error}</span>`;
        } else if (data.message === 'Login successful') {
            window.location.href = '/dashboard';
        }
    })
    .catch(error => console.error('Error:', error));
}

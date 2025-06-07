"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
// CSRF token helper configuration
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (const cookie in cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }
    return null;
}
function submitRegistrationForm(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        const form = event.target;
        const username = form.querySelector('[name="username"]').value;
        const email = form.querySelector('[name="email"]').value;
        const password = form.querySelector('[name="password"]').value;
        const payload = {
            username, email, password
        };
        try {
            // To later fetch from .env file instead
            const response = yield fetch("http://localhost:8000/auth/register/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'X-CSRFToken':getCSRFToken() || '' // activate when using CSRF protection
                },
                body: JSON.stringify(payload),
            });
            const data = yield response.json();
            if (response.ok) {
                alert(data.message || 'SUCCESS: Registration was successful!');
            }
            else {
                alert(data.error || 'ERROR: Registration failed');
            }
        }
        catch (error) {
            alert('INTERNAL SERVER ERROR: An error occurred during registration attempt: ' + error.message);
        }
    });
}
// Event listener for when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm') || null;
    if (form) {
        form.addEventListener('submit', submitRegistrationForm);
    }
    else {
        console.error('ERROR: Registration form not found in DOM!');
    }
});

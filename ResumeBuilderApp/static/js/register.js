// register.js
const passwordInput = document.getElementById('inputPassword');
const confirmPasswordInput = document.getElementById('inputConfirmPassword');
const passwordRequirements = document.getElementById('password-requirements').children;
const form = document.getElementById('registration-form');

passwordInput.addEventListener('input', () => {
    const password = passwordInput.value;

    for (let i = 0; i < passwordRequirements.length; i++) {
        const requirement = passwordRequirements[i];

        if (requirement.id === 'length-requirement') {
            if (password.length >= 8) {
                requirement.classList.add('text-success');
            } else {
                requirement.classList.remove('text-success');
            }
        } else if (requirement.id === 'uppercase-requirement') {
            if (/[A-Z]/.test(password)) {
                requirement.classList.add('text-success');
            } else {
                requirement.classList.remove('text-success');
            }
        } else if (requirement.id === 'number-requirement') {
            if (/\d/.test(password)) {
                requirement.classList.add('text-success');
            } else {
                requirement.classList.remove('text-success');
            }
        }
    }
});

form.addEventListener('submit', (event) => {
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (password !== confirmPassword) {
        event.preventDefault(); // Prevent form submission
        alert('Passwords do not match'); // Display an error message
    }
});
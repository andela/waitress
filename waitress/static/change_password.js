const changePasswordForm = document.getElementById('change_passwd_form');
const password = document.getElementById('password');
const verifyPassword = document.getElementById('verifyPassword');

const URL = '/change_password';

const resetPasswordInput = () => {
    password.value = '';
    verifyPassword.value = '';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showSpinner() {
    const spinner = `<div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status">
    <span class="sr-only">Loading...</span>
  </div>`;

  $('#change_passwd_form').hide();
  $("h1").after(spinner);
}

function hideSpinner() {
    $('.spinner-grow').hide();
    $('#change_passwd_form').show();
}

const changePasswordHandler = async (e) => {
    e.preventDefault();
    $(".alert").hide();

    const passwordText = password.value.trim();
    const verifyPasswordText = verifyPassword.value.trim();

    if (passwordText !== verifyPasswordText) {
        // passwords don't match
        const message = 'Passwords entered do not match!';
        const alertElement = `<div class="alert alert-danger" role="alert">${message}</div>`;
        $("h1").after(alertElement);
        resetPasswordInput();
        return false;
    }

    if (passwordText.length < 6) {
        const message = 'Password must contain atleast 6 characters';
        const alertElement = `<div class="alert alert-danger" role="alert">${message}</div>`;
        $("h1").after(alertElement);
        resetPasswordInput();
        return false;
    }

    const payload = { passwordText, verifyPasswordText };
    const csrftoken = getCookie('csrftoken');

    const options = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(payload)
    }

    try {
        showSpinner();
        const res = await fetch(URL, options);
        hideSpinner();

        if (!res.ok) {
            const message = res.statusText;
            const alertElement = `<div class="alert alert-danger" role="alert">${message}</div>`;
            $("h1").after(alertElement);
            resetPasswordInput();
            console.error(message);
            return false;
        }
        const message = 'Password successfully changed.'
        const successAlertElement = `<div class="alert alert-success" role="alert">${message}</div>`;
        $("h1").after(successAlertElement);
        resetPasswordInput();
        window.location.replace('/logout')
    } catch(error) {
        hideSpinner();
        const message = 'Error changing password!';
        const alertElement = `<div class="alert alert-danger" role="alert">${message}</div>`;
        $("h1").after(alertElement);
        resetPasswordInput();
        console.error(error.message)
    }
}

changePasswordForm.addEventListener('submit', changePasswordHandler);

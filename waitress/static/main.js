// html elements
const deleteBtn = document.getElementById('btn-delete');
const notificationContainer = document.getElementById('dashboard__notify__container');
const notificationMessage = document.getElementById('notification__message');
const fetchUsersBtn = document.getElementById('fetch__users');
const addUserBtn = document.getElementById('add__user');
const deactivateUserBtn = document.getElementById('deactivate__user');
const generateReportBtn = document.getElementById('generate__report');
const refreshUsersBtn = document.getElementById('refresh__users');
const fetchUserBtn = document.getElementById('fetch__user');

// event listeners
deleteBtn.addEventListener('click', () => {
    notificationContainer.style.display = 'none';
});

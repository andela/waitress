const FETCH_ALL_USERS = '/v2/fetch_users';
const REFRESH_SLACK_USERS = '/v2/refresh_users';
const ADD_USER = '/v2/add_user';

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
const mainView = document.getElementById('main__view');
const notifyMainContent = document.getElementById('notify__main');

// functions
const hideNotification = () => {
    notificationContainer.style.display = 'none';
}

const showNotification = (message = '', status = 'success') => {
    notificationContainer.style.display = 'flex';
    notificationMessage.innerHTML = message;
    const bgColor = status = 'success' ? 'green' : 'red';
    notifyMainContent.style.background = bgColor;
    setTimeout(hideNotification, 2000);
}

const refreshSlackUsers = async () => {
    const res = await fetch(REFRESH_SLACK_USERS);
    const response = await res.json()
    console.log(response);
}

const displaySpinner = () => {
    mainView.innerHTML = '<progress class="progress is-small is-primary" max="100">15%</progress>';
}

const mountView = (snippet) => {
    mainView.innerHTML = snippet;
}

const fetchUsers = async () => {
    displaySpinner();
    try {
        const res = await fetch(FETCH_ALL_USERS);
        const response = await res.json()
        const _userRows = response.map((user, index) => constructUserRow(user, index))
        const userRows = _userRows.join('')
        const outputTable = constructTable(userRows);
        mountView(outputTable)
        showNotification('Done fetching all users!')
    } catch (error) {
        console.log('==>', error.message)
        showNotification(error.message)
    }
}

const constructTable = (userRows) => (`
<table class="table full__width">
    <thead>
        <tr>
            <th>No</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email Address</th>
            <th>Active Status</th>
            <th>User Type</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
        ${userRows}
    </tbody>
</table>
`);

const constructUserRow = ({
    firstname,
    lastname,
    email,
    is_active,
    user_type
}, index) => (`
    <tr class="user__row">
        <th>${index + 1}</th>
        <td>${firstname}</td>
        <td>${lastname}</td>
        <td>${email}</td>
        <td>${is_active}</td>
        <td>${user_type}</td>
        <td>${is_active ? '❌' : '✅'}</td>
    </tr>
`);

const addUserForm = () => (`
<form method='POST' action=${ADD_USER}>
    <
</form>
`);

// event listeners
deleteBtn.addEventListener('click', hideNotification);
refreshUsersBtn.addEventListener('click', refreshSlackUsers);
fetchUsersBtn.addEventListener('click', fetchUsers);

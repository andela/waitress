const FETCH_ALL_USERS = '/v2/fetch_users';
const REFRESH_SLACK_USERS = '/v2/refresh_users';
const ADD_USER = '/v2/add_guest';
const RETRIEVE_SINGLE_USER = '/v2/retrieve_user';
const DEACTIVATE_USER = '/v2/deactivate_user';

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
const addUserForm = document.getElementById('add_user_form');

// variables
const spinnerText = '<progress class="progress is-small is-primary" max="100">15%</progress>';
let users = [];

// functions
const hideNotification = () => {
    notificationContainer.style.display = 'none';
}

const showNotification = (message = '', status = 'success') => {
    notificationContainer.style.display = 'flex';
    notificationMessage.innerHTML = message;
    const bgColor = (status == 'success') ? 'green' : 'red';
    notifyMainContent.style.background = bgColor;
    setTimeout(hideNotification, 2000);
}

const refreshSlackUsers = async () => {
    const res = await fetch(REFRESH_SLACK_USERS);
    const response = await res.json()
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
        users = await res.json()
        const _userRows = users.map((user, index) => constructUserRow(user, index))
        const userRows = _userRows.join('')
        const outputTable = constructTable(userRows, users.length, 'users');
        mountView(outputTable);
        const sortUsersForm = document.getElementById('sort_all_users');
        // sortUsersForm.addEventListener('submit', sortUsers);
        showNotification('Done fetching all users!')
    } catch (error) {
        showNotification(error.message)
    }
}

const sortUsers = (e) => {
    e.preventDefault();
    const sortUsersForm = document.getElementById('sort_all_users');
    user_type = sortUsersForm.user_type.value;
    let sortedUsers;
    if (user_type === 'All') {
        sortedUsers = users;
    } else if (user_type === 'Staff') {
        sortedUsers = users.filter(user => user.user_type == 'staff' || user.user_type == 'employee');
    } else {
        sortedUsers = users.filter(user => user.user_type == user_type)
    }
    const _userRows = sortedUsers.map((user, index) => constructUserRow(user, index))
    const userRows = _userRows.join('');
    const userType = (user_type === 'All') ? 'users' : user_type;
    const outputTable = constructTable(userRows, sortedUsers.length, userType);
    mountView(outputTable);
}

const constructTable = (userRows, count, user_type) => (`
<p class="title">There are ${count} ${user_type} on waitress.</p>
<form id="sort_all_users" method="POST">
    <div class="select">
        <select class="sort_all_users" name="user_type">
            <option value='All'>All</option>
            <option value='staff'>Staff/Employee</option>
            <option value='guest'>Guest</option>
            <option value='cleaner'>Cleaner</option>
            <option value='security'>Security</option>
        </select>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link" type="submit">Sort Users</button>
        </div>
    </div>
</form>
<table class="table full__width">
    <thead>
        <tr>
            <th>id</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email Address</th>
            <th>Active Status</th>
            <th>User Type</th>
        </tr>
    </thead>
    <tbody>
        ${userRows}
    </tbody>
</table>
`);

const constructUserRow = ({
    id,
    firstname,
    lastname,
    email,
    is_active,
    user_type
}) => (`
    <tr class="user__row">
        <th>${id}</th>
        <td>${firstname}</td>
        <td>${lastname}</td>
        <td>${email}</td>
        <td>${is_active ? '✅' : '❌'}</td>
        <td>${user_type}</td>
    </tr>
`);

const ADD_USER_FORM = (`
<h2 class="title">Add New User</h2>
<p>Leave firstname and lastname fields blank if user type is guest</p>
<form method='POST' class="add_user_form" id="add_user_form">
    <div class="field">
        <div class="control">
            <input class="input" type="text" placeholder="first name" name="firstname" id="firstname">
        </div>
    </div>

    <div class="field">
        <div class="control">
            <input class="input" type="text" placeholder="last name" name="lastname" id="lastname">
        </div>
    </div>

    <div class="field">
        <div class="control">
            <input class="input" type="email" placeholder="email address" name="email" id="email">
        </div>
    </div>

    <div class="select">
        <select class="user_type_select" name="user_type">
            <option value='guest'>Guest</option>
            <option value='cleaner'>Cleaner</option>
            <option value='security'>Security</option>
        </select>
    </div>

    <div class="field is-grouped center_flex">
        <div class="control">
            <button class="button is-link" type="submit" id="add_user_cta">Submit</button>
        </div>
    </div>
</form>
`);

const constructAddUserForm = () => {
    mountView(ADD_USER_FORM)
    const addUserForm = document.getElementById('add_user_form');
    addUserForm.addEventListener('submit', handleAddUser);
}

const handleAddUser = async (e) => {
    e.preventDefault();
    const addUserForm = document.getElementById('add_user_form');
    const payload = {
        firstname: addUserForm.firstname.value,
        lastname: addUserForm.lastname.value,
        email: addUserForm.email.value,
        user_type: addUserForm.user_type.value,
    }
    mainView.insertBefore(spinnerNode, mainView.firstChild);
    const addUserCta = document.getElementById('add_user_cta');
    addUserCta.setAttribute('disabled', true);
    let fetchStatus, response;
    const fetchQuery = {
        method: 'POST',
        body: JSON.stringify(payload),
        credentials: 'same-origin',
        mode: 'cors',
        cache: 'no-cache',
        headers: { 'Content-Type': 'application/json' }
    };
    try {
        const res = await fetch(ADD_USER, fetchQuery);
        response = await res.json();
        fetchStatus = res.status;
    } catch (error) {
        showNotification(error.message, 'failure');
    }

    if (fetchStatus === 200) {
        showNotification('User successfully added.');
        const userCardText = createUserCard(response);

        const existingUserCards = document.getElementsByClassName('user__card_container');
        if (existingUserCards.length > 0) {
            existingUserCards[0].remove();
        }
        const userCardNode = convertStringToNode(userCardText);
        mainView.insertAdjacentElement('beforeend', userCardNode);
    } else {
        showNotification(response, 'failure');
    }

    // remove spinner
    addUserCta.removeAttribute('disabled');
    mainView.removeChild(mainView.firstChild);
}

const convertStringToNode = (str) => {
    const parsedText = new DOMParser().parseFromString(str, 'text/html');
    return parsedText.body.firstChild;
}

const spinnerNode = convertStringToNode(spinnerText);

const createUserCard = ({ firstname, email, slack_id, id, is_active, lastname, photo }, extras='') => (`
<section class="user__card_container">
    <img src='${photo}' />
    <p><strong>User ID:</strong> ${id}</p>
    <p><strong>Slack ID:</strong> ${slack_id}</p>
    <p><strong>First Name:</strong> ${firstname}</p>
    <p><strong>Last Name:</strong> ${lastname}</p>
    <p><strong>Email Address:</strong> ${email}</p>
    <p><strong>isUserActive:</strong> ${is_active}</p>
    ${extras}
</section>
`);

const retrieveUserHandler = () => {
    const retrieveUserForm = `<div class="retrieve_user_container">
        <div class="field">
            <div class="control">
                <input class="input" type="text" placeholder="Search by first name" name="firstname" id="retrieve_input">
            </div>
        </div>

        <div class="field is-grouped">
            <div class="control">
                <button class="button is-link" type="submit" id="retrieve_user_btn">Submit</button>
            </div>
        </div>
    </div>
    <section id="retrieve_response_container">
    </section>
`;
    mountView(retrieveUserForm);
    const retrieveUserBtn = document.getElementById('retrieve_user_btn');
    retrieveUserBtn.addEventListener('click', retrieveUser);
}

const retrieveUser = async () => {
    const retrieveUserInput = document.getElementById('retrieve_input');
    firstname = retrieveUserInput.value;

    const url = `${RETRIEVE_SINGLE_USER}/${firstname}`;
    const res = await fetch(url);
    const response = await res.json();

    const resultContainer = document.getElementById('retrieve_response_container');
    const userCards = response.map(constructUserCard);
    resultContainer.innerHTML = userCards;
}

const deactivateUser = async (id) => {
    const url = `${DEACTIVATE_USER}/${id}`;
    const res = await fetch(url);
    const response = await res.json();

    if (res.status === 200) {
        const action = response.is_active ? 'activated' : 'deactivated';
        showNotification(`User successfully ${action}.`);
        const userCardText = constructUserCard(response);
        retrieve_response_container.innerHTML = userCardText;
    } else {
        showNotification(response, 'failure');
    }
};

const constructUserCard = (user) => {
    const btnClass = user.is_active ? 'button red' : 'button blue';
    const btnText = user.is_active ? 'Deactivate' : 'Activate';
    const deactivateBtn = `<button class="deactivate__user ${btnClass}" onclick="deactivateUser(${user.id})">${btnText}</button>`;
    const userCardText = createUserCard(user, deactivateBtn);
    return userCardText;
}

const createReportPage = () => {
    mountView()
}

// event listeners
deleteBtn.addEventListener('click', hideNotification);
refreshUsersBtn.addEventListener('click', refreshSlackUsers);
fetchUsersBtn.addEventListener('click', fetchUsers);
addUserBtn.addEventListener('click', constructAddUserForm);
fetchUserBtn.addEventListener('click', retrieveUserHandler);
generateReportBtn.addEventListener('click', createReportPage);

// DOM elements
const modalBody = document.getElementById('modal-body');
const refreshSlackUserBtn = document.getElementById('refresh-slack-btn');


const notyConfig = {
    timeout: 1000,
    closeWith: ['click'],
    theme: 'relax'
};

const SPINNER_HTML = `<section class="d-flex justify-content-center align-items-center w-100">
<div class="spinner-grow text-dark"></div>
</section>`;

const REFRESH_HTML = '<i class="fas fa-sync-alt"></i>';

export async function refreshSlackUser() {
    try {
        refreshSlackUserBtn.innerHTML = `${SPINNER_HTML} Loading...`;
        refreshSlackUserBtn.disabled = true;
        await axios.put('/users/update-users/');
        sendNotification('Slack users Refreshed Successfully');
        refreshSlackUserBtn.innerHTML = REFRESH_HTML;
        refreshSlackUserBtn.disabled = false;
    } catch(error) {
        sendNotification('error', error.message);
        console.log(error.message);
        refreshSlackUserBtn.innerHTML = REFRESH_HTML;
        refreshSlackUserBtn.disabled = false;
    }
}

function sendNotification(text, type = 'success') {
    return new Noty({ text, type, ...notyConfig }).show();
}

function generateModalHeader(title) {
    return `<!-- Modal Header -->
<div class="modal-header">
    <h4 class="modal-title">${title}</h4>
    <button type="button" class="close" data-dismiss="modal">&times;</button>
</div>`;
}

const updateModalFooter = `<!-- Modal footer -->
<div class="modal-footer">
    <button type="button" class="btn btn-primary">Update</button>
    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
</div>`;

export function updateUserInfo(userId, firstname, lastname, is_active) {
    const isActive = (is_active === 'True');
    const modalHeader = generateModalHeader('Update User Info');
    modalBody.innerHTML = `${modalHeader}
<!-- Modal body -->
<div class="modal-body">
    <div class="form-group">
        <label for="usr">User ID:</label>
        <input type="text" class="form-control" id="usr" disabled value="${userId}" />
    </div>

    <div class="form-group">
        <label for="usr">First name:</label>
        <input type="text" class="form-control" id="update_user_firstname" value="${firstname}" />
    </div>

    <div class="form-group">
        <label for="usr">Last name:</label>
        <input type="text" class="form-control" id="update_user_lastname" value="${lastname}" />
    </div>

    <div class="form-check">
        <label class="form-check-label">
            <input type="checkbox" class="form-check-input" ${isActive ? 'checked': ''} id="update_user_is_active" />
            <span>isActive</span>
        </label>
    </div>
</div>
${updateModalFooter}`;

    $("#modal").modal('show');
}

function fetchAllUsers() {
    try {
        console.log('')
    } catch (error) {
        console.log('')
    }
}

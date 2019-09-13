const reportBtn = document.getElementById('report__date_btn');
let dataTable = null;

const fetchReport = async () => {
    try {
        const reportDate = document.getElementById('daily_report_date_picker').value;
        if (!reportDate) {
            $('p#error-message').text('Please select a date.');
            return;
        }
        $('p#error-message').hide();
        if (dataTable) dataTable.destroy();
        const url = `/reports/daily?date=${reportDate}`;
        const result = await fetch(url);
        const resultJson = await result.json()
        dataTable = $('table#report__table').DataTable({
            data: resultJson.data,
            columns: [
                { data: 'firstname', title: 'First Name' },
                { data: 'lastname', title: 'Last Name' },
                { data: 'email', title: 'Email' },
                { data: 'hadBreakfast', title: 'Breakfast' },
                { data: 'hadLunch', title: 'Lunch' }
            ],
        });
    } catch (error) {
        $('p#error-message').text(error.message);
        $('p#error-message').show()
    }
}
reportBtn.addEventListener('click', fetchReport)

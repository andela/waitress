// default actions
document.querySelector('.report_details').style.display = 'none';

const dailyReportBtn = document.getElementById('report__date_btn');
const weeklyReportBtn = document.getElementById('weekly_report__date_btn');
let dataTable = null;

const fetchDailyReport = async () => {
    try {
        const reportDate = document.getElementById('daily_report_date_picker').value;
        const reportType = document.getElementById('daily_report_type').value;

        if (document.querySelector('.report_details')) {
            document.querySelector('.report_details').style.display = 'none';
        }

        if (!reportDate) {
            $('p#error-message').text('Please select a date.');
            return;
        }
        $('p#error-message').hide();
        if (dataTable) dataTable.destroy();
        const url = `/reports/daily?date=${reportDate}&reportType=${reportType}`;
        const result = await fetch(url);
        const resultJson = await result.json();

        const columns = [
            { data: 'firstname', title: 'First Name' },
            { data: 'lastname', title: 'Last Name' },
            { data: 'email', title: 'Email' },
            { data: 'hadBreakfast', title: 'Breakfast' },
            { data: 'hadLunch', title: 'Lunch' },
            { data: 'userId', title: 'User ID' }
        ];

        dataTable = $('table#report__table').DataTable({
            data: resultJson.data,
            columns,
            dom: 'fBrltip',
            buttons: {
                buttons: ['csv', 'pdf']
            },
            processing: true
        });

        if (reportType !== 'both') {
            const columnIndexToHide = reportType === 'breakfast' ? 4 : 3;
            const column = dataTable.column(columnIndexToHide);
            // Toggle the visibility
            column.visible(false);
        } else {
            document.querySelector('.report_details').style.display = 'block';

            document.getElementById('report__breakfast_count').textContent = resultJson.breakfast_count;
            document.getElementById('report__lunch_count').textContent = resultJson.lunch_count;
        }
    } catch (error) {
        $('p#error-message').text(error.message);
        $('p#error-message').show();
    }
}

const fetchWeeklyReport = async () => {
    try {
        $('p#error-message').hide();
        const from = document.getElementById('weekly_report_from_date_picker').value;
        const to = document.getElementById('weekly_report_to_date_picker').value;

        const fromDate = new Date(from);
        const toDate = new Date(to);

        if (fromDate > toDate) {
            $('p#error-message').text('The from date must be greater than the to date.');
            $('p#error-message').show();
            return;
        }

        if (from && to) {
            const url = `/reports/weekly?from=${from}&to=${to}`;
            return;
        }
        $('p#error-message').text('The from date and to date must be supplied');
        $('p#error-message').show();
    } catch (error) {
        $('p#error-message').text(error.message);
        $('p#error-message').show();
    }
}

// event listeners
currentLocation = window.location.pathname;
if (currentLocation === '/reports/daily') {
    dailyReportBtn.addEventListener('click', fetchDailyReport);
} else if (currentLocation === '/reports/weekly') {
    weeklyReportBtn.addEventListener('click', fetchWeeklyReport);
}

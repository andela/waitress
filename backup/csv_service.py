from datetime import datetime
import csv


def generate_file_name():
    now = datetime.now()

    MONTH_INT = (now.month - 1) if (now.month > 1) else 12
    YEAR = now.year if (now.month > 1) else (now.year - 1)

    MONTH_ARR = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    MONTH = MONTH_ARR[MONTH_INT - 1]

    return f"backup_{MONTH}_{YEAR}"


def create_csv(payload):
    FILENAME = generate_file_name()
    CSV_PATH = f"backup/csvs/{FILENAME}.csv"

    with open(CSV_PATH, mode="w") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        header = [
            "DATE",
            "DATE_MODIFIED",
            "USER_ID",
            "FIRSTNAME",
            "LASTNAME",
            "USER_TYPE",
            "BREAKFAST",
            "LUNCH",
        ]
        writer.writerow(header)
        import pdb; pdb.set_trace()
        writer.writerows(payload)
    return CSV_PATH, FILENAME

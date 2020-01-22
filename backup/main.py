#!/usr/bin/python3
import os
from datetime import date

from sql_queries import (
    FETCH_MEAL_RECORDS,
    DELETE_MEAL_RECORDS,
    FETCH_PANTRY_RECORDS,
    DELETE_PANTRY_RECORDS,
)
from slack_service import send_message
from csv_service import create_csv
from db import execute_query
from gdrive import upload_to_drive


def handle_ops(fetch_query, delete_query):
    records = execute_query(fetch_query)
    print(fetch_query)

    if records:
        print('There are records.')
        csv_path, filename = create_csv(records)
        execute_query(delete_query)
        upload_to_drive(csv_path, filename)
        os.remove(csv_path)
    else:
        print('There are no records for this query.')
        send_message('There are no records for this query.')


def run():
    try:
        today = date.today()

        if today.day > 1:
            # fail silently because it's not the first of the month
            send_message("It's not yet time for backup")
            return

        handle_ops(FETCH_MEAL_RECORDS, DELETE_MEAL_RECORDS)
        handle_ops(FETCH_PANTRY_RECORDS, DELETE_PANTRY_RECORDS)
    except Exception as error:
        raise error
        errorMessage = f"""An error occured while pushing backup to Google Drive.

Error information ====> ```{error.args[0] if error.args else 'weird error'}```
"""
        send_message(errorMessage)


if __name__ == "__main__":
    run()

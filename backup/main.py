#!/usr/bin/python3
import os
from datetime import date

import psycopg2
from dotenv import find_dotenv, load_dotenv

import csv_service
import db
import gdrive
import slack_service
from sql_queries import (DELETE_MEAL_RECORDS, DELETE_PANTRY_RECORDS,
                         FETCH_MEAL_RECORDS, FETCH_PANTRY_RECORDS)

load_dotenv(find_dotenv())


def handle_ops(db_connection, fetch_query, delete_query):
    print("Executing fetch_query...")
    records = db.execute_query(db_connection, fetch_query, fetch=True)

    if records:
        print(f"{len(records)} records found.")
        csv_path, filename = csv_service.create_csv(records)
        print("Executing delete_query...")
        db.execute_query(db_connection, delete_query)
        print("Uploading csv file to GoogleDrive...")
        gdrive.upload_to_drive(csv_path, filename)
        print("Cleaning up csv files...")
        os.remove(csv_path)
    else:
        print("There are no records for this query.")
        slack_service.send_message("There are no records for this query.")


def run():
    try:
        today = date.today()

        if today.day > os.getenv('BACKUP_DAY'):
            # fail silently because it's not the 1st of the month
            slack_service.send_message("It's not yet time for backup")
            return

        DATABASE_URL = os.getenv("DATABASE_URL")
        with psycopg2.connect(DATABASE_URL) as conn:
            handle_ops(conn, FETCH_MEAL_RECORDS, DELETE_MEAL_RECORDS)
            handle_ops(conn, FETCH_PANTRY_RECORDS, DELETE_PANTRY_RECORDS)

    except Exception as error:
        error_message = f"""An error occurred while pushing backup to Google Drive.

Error information ====> ```{error.args[0] if error.args else 'weird error'}```
"""
        slack_service.send_message(error_message)
        raise error


if __name__ == "__main__":
    run()

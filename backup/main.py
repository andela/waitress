#!/usr/bin/python3
import os
from datetime import date

import psycopg2
from dotenv import find_dotenv, load_dotenv

import csv_service
import db
import gdrive
from slack_service import SlackService, make_slack_client
from sql_queries import (DELETE_MEAL_RECORDS, DELETE_PANTRY_RECORDS,
                         FETCH_MEAL_RECORDS, FETCH_PANTRY_RECORDS)

load_dotenv(find_dotenv())


def handle_ops(db_connection, fetch_query, delete_query, **kwargs):
    print("Executing fetch_query...")
    records = db.execute_query(db_connection, fetch_query, fetch=True)
    slack_service = kwargs.get("slack_service")
    if records:
        print(f"{len(records)} records found.")
        print("writing records to csv file...")
        csv_path, filename = csv_service.create_csv(records)
        # enable/disable the delete action
        if kwargs.get("enable_delete", False) is True:
            print("Executing delete_query...")
            db.execute_query(db_connection, delete_query)
        else:
            print("skipping delete, it is a dangerous action :)")
        # enable/disable gdrive upload
        if kwargs.get("enable_gdrive_upload") is True:
            print("Uploading csv file to GoogleDrive...")
            gdrive.upload_to_drive(csv_path, filename)
        else:
            print("skipping gdrive upload, no GDRIVE_TOKEN set")
        print("Cleaning up csv files...")
        os.remove(csv_path)
    else:
        print("There are no records for this query.")
        slack_service.send_message("There are no records for this query.")


def local_chat_post_message(**kwargs):
    """Dummy function that does nothing when SLACK_TOKEN is not set."""
    return {}


def run():
    try:
        today = date.today()
        enable_delete = os.getenv("ENABLE_BACKUP_DELETE_ACTION")
        enable_gdrive_upload = os.getenv("GDRIVE_TOKEN", "") != ""

        channel = os.getenv("SLACK_CHANNEL")
        client = make_slack_client(local_chat_post_message)
        slack_service = SlackService(client, channel)

        if today.day > int(os.getenv("BACKUP_DAY")):
            # fail silently because it's not the 1st of the month
            slack_service.send_message("It's not yet time for backup")
            return

        DATABASE_URL = os.getenv("DATABASE_URL")
        with psycopg2.connect(DATABASE_URL) as conn:
            handle_ops(
                conn,
                FETCH_MEAL_RECORDS,
                DELETE_MEAL_RECORDS,
                enable_delete=enable_delete,
                enable_gdrive_upload=enable_gdrive_upload,
                slack_service=slack_service,
            )
            handle_ops(
                conn,
                FETCH_PANTRY_RECORDS,
                DELETE_PANTRY_RECORDS,
                enable_delete=enable_delete,
                enable_gdrive_upload=enable_gdrive_upload,
                slack_service=slack_service,
            )

    except Exception as error:
        error_message = f"""An error occurred while pushing backup to Google Drive.

Error information ====> ```{error.args[0] if error.args else 'weird error'}```
"""
        slack_service.send_message(error_message)
        raise error


if __name__ == "__main__":
    run()

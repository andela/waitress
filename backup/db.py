import os

import psycopg2
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


def execute_query(query, fetch=False):
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(DATABASE_URL)
    db_connection = psycopg2.connect(DATABASE_URL)

    cursor = db_connection.cursor()

    cursor.execute(query)

    return cursor.fetchall() if fetch else None

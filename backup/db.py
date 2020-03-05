def execute_query(db_connection, query, fetch=False):
    """Execute query using the DB connection and return result set or None.

    Args:
        db_connection: the postgres database connection object
        query(str): the SQL query
        fetch(Optional[bool]): should i consume the cursor
    Returns:
        list(tuple): Returning value
    """
    with db_connection.cursor() as curs:
        curs.execute(query)
        return curs.fetchall() if fetch else None

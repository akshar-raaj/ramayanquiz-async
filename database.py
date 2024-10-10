"""
This module creates services/helpers to interact with PostgreSQL database.

The functions shouldn't make any assumptions about the application layer classes and objects.
It should deal with raw SQL statements.

Had we been using ORM, it would deal with ORM statements.
"""

from constants import DB_CONNECTION_STRING

import psycopg2
from psycopg2.errors import OperationalError

connection = None


def get_database_connection(force: bool = False):
    """
    Creates a database connection if needed and keeps it cached on a global variable.
    We don't want to create a database connection, each time this function gets invoked.

    We possibly want to reuse the connection throughout the lifecycle of the application
    unless the server closes the connection, in which case we will use `force` and recreate the connection.
    """
    global connection
    if connection is None or force:
        try:
            connection = psycopg2.connect(DB_CONNECTION_STRING)
        except OperationalError as e:
            # TODO: Add logger.error
            print(f"Exception {e}")
            return None
    return connection


def retry_with_new_connection(func):
    def wrapper(*args, **kwargs):
        try:
            # For idle connections, the connection might be closed by the server
            # In such cases, executing the query will raise psycopg2.OperationError.
            # OperationError is handled by psycopg2. But connection.closed is set True then.
            # Running the query again will raise psycopg2.InterfaceError
            # which we are handling here
            return func(*args, **kwargs)
        except psycopg2.InterfaceError:
            print("handling interface error")
            get_database_connection(force=True)
            return func(*args, **kwargs)
    return wrapper


@retry_with_new_connection
def fetch_question(question_id: int) -> dict[str, str | int]:
    result = None
    columns = None
    connection = get_database_connection()
    with connection:
        with connection.cursor() as cursor:
            statement = "SELECT id, question from questions WHERE id=%s"
            cursor.execute(statement, (question_id,))
            result = cursor.fetchone()
            columns = [col.name for col in cursor.description]
    if result is None:
        return {}
    row = {k: v for k, v in zip(columns, result)}
    return row


@retry_with_new_connection
def fetch_question_answers(question_id: int) -> list[dict[str, str | int]]:
    rows = []
    columns = None
    connection = get_database_connection()
    with connection:
        with connection.cursor() as cursor:
            statement = "SELECT a.id, a.answer from answers a WHERE a.question_id=%s"
            cursor.execute(statement, (question_id,))
            rows = cursor.fetchall()
            columns = [col.name for col in cursor.description]
    if rows == []:
        return []
    result = []
    for row in rows:
        result.append({k: v for k, v in zip(columns, row)})
    return result


@retry_with_new_connection
def update_column_value(table_name: str, _id: int, column_name: str, column_value) -> bool:
    is_completed = False
    connection = get_database_connection()
    with connection:
        with connection.cursor() as cursor:
            statement = f'UPDATE {table_name} SET {column_name}=%s where id=%s'
            cursor.execute(statement, (column_value, _id,))
            is_completed = True
    return is_completed

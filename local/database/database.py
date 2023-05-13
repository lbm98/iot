import time
import mysql.connector
from mysql.connector import Error

HOST_NAME = 'db'
PORT = '3306'
USER_NAME = 'root'
USER_PASSWORD = 'iot'
DATABASE_NAME = 'iot_db'
TABLE_NAME = 'sensor'


def create_connection():
    """
    Create a connection to a MySQL server.

    Note that MySQL is a server-based DBMS,
    so we first connect to a server,
    and then we create a database.

    This function blocks until a connection is made.
    """
    while True:
        try:
            connection = mysql.connector.connect(
                host=HOST_NAME,
                port=PORT,
                user=USER_NAME,
                passwd=USER_PASSWORD
            )
            print("Connecting to MySQL success")
            return connection
        except Error as e:
            print(f"Connecting to MySQL fail: {e}")
            time.sleep(1)


def create_database_if_not_exists(connection):
    cursor = connection.cursor()

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

        cursor.execute(f"USE {DATABASE_NAME}")

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            humidity INT
        )
        """)

        connection.commit()

        print('Create table success')

    except Error as e:
        print(f'Create table fail: {e}')
        exit(1)

    finally:
        cursor.close()


def insert_data(connection, humidity):
    cursor = connection.cursor()

    try:
        cursor.execute(f"USE {DATABASE_NAME}")

        cursor.execute(f"INSERT INTO {TABLE_NAME} (humidity) VALUES ({humidity})")

        connection.commit()

        print("Insert success")

    except Error as e:
        print(f"Insert fail: {e}")
        exit(1)

    finally:
        cursor.close()


if __name__ == '__main__':
    conn = create_connection()
    create_database_if_not_exists(conn)
    insert_data(conn)

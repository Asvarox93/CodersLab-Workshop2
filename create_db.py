from config import config
from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable
import re

cnx = None
cursor = None

def create_db(db):
    """
    Create db with given name.

    :param str db: name of db
    """
    sql = f"CREATE DATABASE {db};"
    try:
        params = config()
        cnx = connect(**params)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        print("Baza założona")
    except OperationalError:
        print("Błąd!")
    except DuplicateDatabase:
        print("Ostrzeżenie: baza już istniała.")
    else:
        cursor.close()
        cnx.close()
        print('Database connection closed!')


def execute_sql(sql_code, db='workshop'):
    """
    Run given sql code with psycopg2.

    :param str sql_code: sql code to run
    :param str db: name of db,

    :rtype: list
    :return: data from psycobg2 cursor as a list (can be None) if nothing to fetch.
    """
    result = None

    try:
        params = config(section=db)
        cnx = connect(**params)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
        if re.match(r'select', sql_code, re.I):  # select/SELECT itp.
            result = cursor.fetchall()
        print("Sukces.")
    except OperationalError as e:
        print("Błąd połączenia!", e)
    except DuplicateTable as e:
        print("Ostrzeżenie: Tabela już istniała.", e)
    except DuplicateDatabase as e:
        print("Ostrzeżenie: baza już istniała.", e)
    else:
        cursor.close()
        cnx.close()

    return result

def connect_db(db='workshop'):
    try:
        params = config(section=db)
        cnx = connect(**params)
        cnx.autocommit = True
        cursor = cnx.cursor()     
        return cursor
    except OperationalError as e:
        print("Błąd połączenia!", e)

def close_connect_db():
    if cursor is not None and cnx is not None:
        cursor.close()
        cnx.close()
        


if __name__ == '__main__':
    create_db('workshop')
    execute_sql(sql_code="CREATE TABLE Users (id SERIAL PRIMARY KEY, username VARCHAR(255), hashed_password VARCHAR(80))")
    execute_sql(sql_code="CREATE TABLE Messages (id SERIAL PRIMARY KEY, from_id INT REFERENCES users(id), to_id INT REFERENCES users(id), creation_date TIMESTAMP NOT NULL DEFAULT NOW(), text TEXT)")

    
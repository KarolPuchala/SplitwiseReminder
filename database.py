import sqlite3

class Database:
    def __init__(self, database) -> None:
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor() 
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

def setup(database):
    with Database(database) as database:
        database.cursor.execute('''CREATE TABLE debtors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            debt_amount FLOAT,
            debt_incurred_from DATE)''')

def if_table_exist(db_name, table_name):
    with Database(db_name) as database:
        database.cursor.execute('SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name=?);', (table_name,))
        result = database.cursor.fetchone()
    return result[0]

def if_user_exist(db_name, table_name, user_id):
    with Database(db_name) as database:
        database.cursor.execute(f'SELECT EXISTS(SELECT 1 FROM {table_name} WHERE id=?);', (user_id,))
        result = database.cursor.fetchone()
    return result[0]

def insert_data(db_name, table_name, data):
    with Database(db_name) as database:
        database.cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)', data)

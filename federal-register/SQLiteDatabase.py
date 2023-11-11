import sqlite3

class SQLiteDatabase:
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_file)
        self.cursor = self.connection.cursor()

    def create_publications_database(self):
        self.connect()
        create_table_sql = """
        CREATE TABLE government_publications (
            citation TEXT PRIMARY KEY NOT NULL,
            publication_date TEXT NOT NULL,
            effective_date TEXT NOT NULL,
            end_of_comment TEXT NOT NULL,
            title TEXT NOT NULL
        );
        """
        # execute the SQL statement
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def execute_query(self, query: str, results: bool = False):
        # Execute the SQL statement
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall() if results else None
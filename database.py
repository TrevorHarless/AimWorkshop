import sqlite3

class Database:
    _instance = None

    # Ensures that one and only one instance of Database is created and reused throughout the program
    def __new__(cls, game_mode=None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect('data/Scores.db')
            
            # Creates tables for each of the four game modes
            cls._instance.create_table('radiating')
            cls._instance.create_table('gravity')
            cls._instance.create_table('no_gravity')
            cls._instance.create_table('static')
        return cls._instance
    
    # Creates a table for a specific game mode, each table includes an id and a score
    def create_table(self, game_mode):
        try:
            cur = self._instance.conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {game_mode}_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL
                )
            """)
            self._instance.conn.commit()
            print(f"Table {game_mode}_scores created/connected successfully!")
        except sqlite3.Error as e:
            print("Error creating table:", e)

    # Inserts a score into a given table
    def insert_score(self, game_mode, score):
        try:
            cur = self._instance.conn.cursor()
            cur.execute(f"INSERT INTO {game_mode}_scores (score) VALUES (?)", (score,))
            self._instance.conn.commit()
            print(f"Score inserted into {game_mode}_scores successfully!")
        except sqlite3.Error as e:
            print("Error inserting score:", e)

    # Checks if a table exists. Helpful to avoid errors where application attempts to
    # modify a table that does not exist
    def table_exists(self, table_name):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            return cur.fetchone() is not None
        except sqlite3.Error as e:
            print("Error checking if table exists:", e)
            return False
    
    # Get scores from the radiating_scores table
    def get_radiating_scores(self):
        try:
            table_name = 'radiating_scores'
            if self.table_exists(table_name):
                cur = self._instance.conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} ORDER BY score DESC")
                return cur.fetchall()
            else:
                return []
        except sqlite3.Error as e:
            print("Error fetching scores:", e)
            return []

    # Get scores from the gravity_scores table
    def get_gravity_scores(self):
        try:
            table_name = 'gravity_scores'
            if self.table_exists(table_name):
                cur = self._instance.conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} ORDER BY score DESC")
                return cur.fetchall()
            else:
                return []
        except sqlite3.Error as e:
            print("Error fetching scores:", e)
            return []
    # Get scores from the no_gravity_scores table
    def get_no_gravity_scores(self):
        try:
            table_name = 'no_gravity_scores'
            if self.table_exists(table_name):
                cur = self._instance.conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} ORDER BY score DESC")
                return cur.fetchall()
            else:
                return []
        except sqlite3.Error as e:
            print("Error fetching scores:", e)
            return []

    # Get scores from the static_scores table
    def get_static_scores(self):
        try:
            table_name = 'static_scores'
            if self.table_exists(table_name):
                cur = self._instance.conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} ORDER BY score DESC")
                return cur.fetchall()
            else:
                return []
        except sqlite3.Error as e:
            print("Error fetching scores:", e)
            return []

    # Closes the current database instance connection
    def close_connection(self):
        print("Database closed")
        self._instance.conn.close()
    
    # Clears the database table
    def clear_table(self, table_name):
        try:
            cur = self._instance.conn.cursor()

            # SQL command to delete all rows from the table
            delete_query = f"DELETE FROM {table_name}"

            # Execute the delete query
            cur.execute(delete_query)

            # Commit the changes and close the connection
            self._instance.conn.commit()
            cur.close()
            print(f"Data in table {table_name} has been cleared.")
        except sqlite3.Error as error:
            print(f"Error clearing data: {error}")

    # If accidentally created a table that is not being used, call this function after any instance of Database is created
    def drop_table(self, table_name):
        try:
            cur = self._instance.conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self._instance.conn.commit()
            print(f"{table_name} dropped successfully!")
        except sqlite3.Error as e:
            print("Error dropping table:", e)

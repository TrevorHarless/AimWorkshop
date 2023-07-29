import sqlite3

class Database:
    _instance = None

    # Ensures that one and only one instance of Database is created and reused throughout the program
    def __new__(cls, game_mode=None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect('data/Scores.db')
            # if game_mode is not None:
            #     cls._instance.create_table(game_mode)
            cls._instance.create_table('radiating')
            cls._instance.create_table('gravity')
            cls._instance.create_table('no_gravity')
            cls._instance.create_table('static')
        return cls._instance
    
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

    def insert_score(self, game_mode, score):
        try:
            cur = self._instance.conn.cursor()
            cur.execute(f"INSERT INTO {game_mode}_scores (score) VALUES (?)", (score,))
            self._instance.conn.commit()
            print(f"Score inserted into {game_mode}_scores successfully!")
        except sqlite3.Error as e:
            print("Error inserting score:", e)

    def table_exists(self, table_name):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            return cur.fetchone() is not None
        except sqlite3.Error as e:
            print("Error checking if table exists:", e)
            return False
    
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

    def close_connection(self):
        print("Database closed")
        self._instance.conn.close()

    # If accidentally created a table that is not being used, call this function after any instance of Database is created
    def drop_table(self, table_name):
        try:
            cur = self._instance.conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self._instance.conn.commit()
            print(f"{table_name} dropped successfully!")
        except sqlite3.Error as e:
            print("Error dropping table:", e)

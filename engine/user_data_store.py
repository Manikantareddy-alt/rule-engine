import sqlite3

class UserDataStore:
    def __init__(self):
        # Connects to or creates SQLite database
        self.conn = sqlite3.connect('rule_engine.db')
        self.create_tables()

    def create_tables(self):
        # Creates the users table if not already present
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                age INTEGER,
                income REAL,
                spend REAL,
                department TEXT
            )''')

    def add_user(self, user_id, user_data):
        # Inserts user data into the table
        with self.conn:
            self.conn.execute('''INSERT INTO users (user_id, age, income, spend, department)
                VALUES (?, ?, ?, ?, ?)''', (user_id, user_data['age'], user_data['income'],
                                            user_data['spend'], user_data['department']))

    def get_user_data(self, user_id):
        # Retrieves user data for a given user_id
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return {"user_id": row[0], "age": row[1], "income": row[2], "spend": row[3], "department": row[4]}
        return None

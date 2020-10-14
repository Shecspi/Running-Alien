import sqlite3


class Database:
    def __init__(self):
        self.connect = sqlite3.connect('resources/database.sqlite')
        self.cursor = self.connect.cursor()
        query = self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                score INTEGER)
        """)

    def get_best_result(self):
        query = self.cursor.execute("""SELECT MAX(score) FROM score LIMIT 1""")
        result = query.fetchone()[0]

        if not result:
            return 0
        else:
            return result

    def reset(self):
        query = self.cursor.execute("""
            DELETE FROM score
        """)
        self.connect.commit()

    def insert_new_score(self, score):
        query = self.cursor.execute(f"""
            INSERT INTO score (time, score) VALUES ('1', '{score}')
        """)
        self.connect.commit()

#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import sqlite3


class Database:
    def __init__(self):
        self.__connect = sqlite3.connect('resources/database.sqlite')
        self.__cursor = self.__connect.cursor()
        query = self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                score INTEGER)
        """)

    def get_best_result(self):
        query = self.__cursor.execute("""SELECT MAX(score) FROM score LIMIT 1""")
        result = query.fetchone()[0]

        if not result:
            return 0
        else:
            return result

    def reset(self):
        query = self.__cursor.execute("""
            DELETE FROM score
        """)
        self.__connect.commit()

    def insert_new_score(self, score):
        query = self.__cursor.execute(f"""
            INSERT INTO score (time, score) VALUES ('1', '{score}')
        """)
        self.__connect.commit()

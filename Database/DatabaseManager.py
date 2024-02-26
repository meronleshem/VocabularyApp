import sqlite3
from Utils.DiffucltyEnum import Difficulty
from Utils.Translator import translate_to_heb


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('Database\\vocabulary.db')
        self.cur = self.conn.cursor()
        self.table_name = "vocabulary"

    def create_db(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS vocabulary
                       (id INTEGER PRIMARY KEY,
                        engWord TEXT,
                        hebWord TEXT,
                        difficulty TEXT)''')

        raw_data1 = (1, "Remorse", translate_to_heb("Remorse"), Difficulty.EASY.name)
        raw_data2 = (2, "Chore", translate_to_heb("Chore"), Difficulty.EASY.name)

        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, difficulty) VALUES (?, ?, ?, ?)", raw_data1)
        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, difficulty) VALUES (?, ?, ?, ?)", raw_data2)
        self.conn.commit()

    def print_db_data(self):

        data = self.cur.execute(f"SELECT * FROM {self.table_name}")

        for item in data:
            print(item)

    def add_word(self, eng_word):
        num_of_words = self.get_table_size()
        word_id = num_of_words + 1
        heb_word = translate_to_heb(eng_word)

        word_data = (word_id, eng_word.lower(), heb_word, Difficulty.EASY.name)
        self.cur.execute(f"INSERT INTO {self.table_name}"
                         f" (id, engWord, hebWord, difficulty) VALUES (?, ?, ?, ?)", word_data)

        self.conn.commit()

    def get_table_size(self):
        self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.cur.fetchone()[0]

    def close_db_connection(self):
        self.cur.close()
        self.conn.close()



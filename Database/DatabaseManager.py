import sqlite3
from Utils.DiffucltyEnum import Difficulty
from Utils.Translator import translate_to_heb, get_word_examples
from Utils.FileHandler import read_words_from_file

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
                        examples TEXT,
                        difficulty TEXT)''')

        raw_data1 = (1, "remorse", translate_to_heb("remorse"), get_word_examples("remorse"), Difficulty.EASY.name)
        raw_data2 = (2, "chore", translate_to_heb("chore"), get_word_examples("chore"), Difficulty.EASY.name)

        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty)"
                         " VALUES (?, ?, ?, ?, ?)", raw_data1)
        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty)"
                         " VALUES (?, ?, ?, ?, ?)", raw_data2)
        self.conn.commit()

    def print_db_data(self):
        data = self.cur.execute(f"SELECT * FROM {self.table_name}")

        for item in data:
            print(item)

    def get_data(self):
        return self.cur.execute(f"SELECT engWord, hebWord FROM {self.table_name}")

    def add_word(self, eng_word):
        if self.is_word_exists(eng_word):
            print(f"{eng_word} is already exists. Abort adding")
            return

        heb_word = translate_to_heb(eng_word)
        if heb_word is None:
            print(f"{eng_word} is not a valid word. Abort adding")
            return

        num_of_words = self.get_table_size()
        word_id = num_of_words + 1
        examples = get_word_examples(eng_word)

        word_data = (word_id, eng_word.lower(), heb_word, examples, Difficulty.EASY.name)
        self.cur.execute(f"INSERT INTO {self.table_name}"
                         f" (id, engWord, hebWord, examples, difficulty) VALUES (?, ?, ?, ?, ?)", word_data)

        self.conn.commit()

        print(f"{eng_word} was added!")

    def add_from_file(self):
        words_to_add = read_words_from_file()
        for word in words_to_add:
            self.add_word(word)

    def update_difficulty(self, eng_word, difficulty):
        self.cur.execute(f"UPDATE {self.table_name}"
                         f" SET difficulty = ? WHERE engWord = ?", (difficulty, eng_word))

        self.conn.commit()

    def delete_word(self, eng_word):
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))

        self.conn.commit()

    def is_word_exists(self, eng_word):
        data = self.cur.execute(f"SELECT engWord FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))
        res = data.fetchone()

        return res is not None

    def get_table_size(self):
        self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.cur.fetchone()[0]

    def close_db_connection(self):
        self.cur.close()
        self.conn.close()



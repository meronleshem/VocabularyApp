import sqlite3
from Utils.DiffucltyEnum import Difficulty
from Utils.Translator import translate_to_heb, get_word_examples
from Utils.FileHandler import read_words_from_file, extract_highlight_words_from_pdf


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
                        difficulty TEXT,
                        group_name TEXT)''')

        raw_data1 = (1, "remorse", translate_to_heb("remorse"), get_word_examples("remorse"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data2 = (2, "chore", translate_to_heb("chore"), get_word_examples("chore"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data3 = (3, "more", translate_to_heb("more"), get_word_examples("more"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data4 = (4, "vigour", translate_to_heb("vigour"), get_word_examples("vigour"), Difficulty.EASY.name, "The_Silent_Patient_1")

        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data1)
        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data2)
        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data3)
        self.cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data4)
        self.conn.commit()

    def print_db_data(self):
        data = self.cur.execute(f"SELECT * FROM {self.table_name}")

        for item in data:
            print(item)

    def get_data(self):
        return self.cur.execute(f"SELECT engWord, hebWord FROM {self.table_name}")

    def get_full_data(self):
        return self.cur.execute(f"SELECT engWord, hebWord, difficulty, group_name FROM {self.table_name}")

    def add_word(self, eng_word, group_name="New_Words"):
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

        word_data = (word_id, eng_word.lower(), heb_word, examples, Difficulty.NEW_WORD.name, group_name)
        self.cur.execute(f"INSERT INTO {self.table_name}"
                         f" (id, engWord, hebWord, examples, difficulty, group_name) VALUES (?, ?, ?, ?, ?, ?)", word_data)

        self.conn.commit()

        print(f"{eng_word} was added!")

    def add_from_file(self, filepath, group_name):
        words_to_add = read_words_from_file(filepath)
        for word in words_to_add:
            self.add_word(word, group_name)

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

    def add_highlight_words_from_pdf(self, filepath):
        words_to_add = extract_highlight_words_from_pdf(filepath)
        for word, pack in words_to_add:
            group_name = f"The Blade Itself {pack}"
            self.add_word(word, group_name)

    def get_table_size(self):
        self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.cur.fetchone()[0]

    def get_word_details(self, eng_word):
        data = self.cur.execute(f"SELECT * FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))

        for item in data:
            return item

    def get_words_by_groups(self, selected_groups):
        query = f"SELECT engWord, hebWord, difficulty, group_name FROM vocabulary WHERE group_name IN ({','.join('?' for _ in selected_groups)})"
        self.cur.execute(query, selected_groups)
        return self.cur.fetchall()

    def get_all_groups_names(self):
        self.cur.execute("SELECT DISTINCT group_name FROM vocabulary")
        return self.cur.fetchall()

    def close_db_connection(self):
        self.cur.close()
        self.conn.close()



import sqlite3
from DiffucltyEnum import Difficulty
from Translator import translate_to_heb


def create_db():
    conn = sqlite3.connect('vocabulary.db')

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS vocabulary
                   (id INTEGER PRIMARY KEY,
                    engWord TEXT,
                    hebWord TEXT,
                    difficulty TEXT)''')

    raw_data1 = (1, "Remorse", translate_to_heb("Remorse"), Difficulty.EASY.name)
    raw_data2 = (2, "Chore", translate_to_heb("Chore"), Difficulty.EASY.name)

    cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, difficulty) VALUES (?, ?, ?, ?)", raw_data1)
    cur.execute("INSERT INTO vocabulary (id, engWord, hebWord, difficulty) VALUES (?, ?, ?, ?)", raw_data2)
    conn.commit()

    cur.close()
    conn.close()


def print_db_data():
    conn = sqlite3.connect('vocabulary.db')
    cur = conn.cursor()

    data = cur.execute("SELECT * FROM vocabulary")

    for item in data:
        print(item)


class DatabaseManager:
    pass
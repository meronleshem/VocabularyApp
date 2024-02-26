from Utils.Translator import translate_to_heb
from Utils.DiffucltyEnum import Difficulty
from Database.DatabaseManager import *


if __name__ == '__main__':
    db = DatabaseManager()

    db.print_db_data()
    db.get_table_size()
   # db.add_word("Faze")

    db.close_db_connection()


from Utils.Translator import translate_to_heb, get_word_examples
from Utils.DiffucltyEnum import Difficulty
from Utils.FileHandler import read_words_from_file
from Database.DatabaseManager import *


if __name__ == '__main__':
    db = DatabaseManager()

   # db.add_word("AA")

    #data = read_words_from_file()
    #for w in data:
     #   db.add_word(w)
    #db.create_db()
    db.print_db_data()
    #db.get_table_size()
    #db.add_word("Faze")
    #db.update_difficulty("faze", Difficulty.MEDIUM.name)

    # words_dict = {}
    # data = db.get_data()
    #
    # for item in data:
    #     print(item[3])

    db.close_db_connection()


    #print(get_word_examples("suspicious"))

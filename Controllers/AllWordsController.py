from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager


class AllWordsController:
    def __init__(self, model: DatabaseManager, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["all_words_page"]
        self.bind()

    def bind(self):
        self.page.button.config(command=self.switch_page)

    def show_words(self):
        words_list = self.model.get_full_data()
        self.page.show_words(words_list)

    def switch_page(self):
        self.view.show_page(self.view.pages["add_word_page"])

from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from View.QuizPage import DifficultyDialog
from Utils.DiffucltyEnum import Difficulty


class AllWordsController:
    def __init__(self, model: DatabaseManager, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["all_words_page"]
        self.bind()

    def bind(self):
        self.page.add_word_btn.config(command=self.switch_page)
        self.page.tree.bind("<Double-Button-1>", self.show_word_details)

    def show_words(self):
        words_list = self.model.get_full_data()
        self.page.show_words(words_list)

    def show_word_details(self, event):
        item = self.page.tree.selection()[0]
        values = self.page.tree.item(item, 'values')
        details = self.model.get_word_details(values[0])
        #self.page.word_expand_label.config(text=details[3])
        dialog = DifficultyDialog(self.page)
        new_difficulty = dialog.result
        if new_difficulty == "Easy":
            new_difficulty = Difficulty.EASY.name
        elif new_difficulty == "Medium":
            new_difficulty = Difficulty.MEDIUM.name
        elif new_difficulty == "Hard":
            new_difficulty = Difficulty.HARD.name
        else:
            return

        self.model.update_difficulty(details[1], new_difficulty)

    def switch_page(self):
        self.view.show_page(self.view.pages["add_word_page"])

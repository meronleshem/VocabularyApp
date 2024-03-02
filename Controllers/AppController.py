from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Controllers.AddWordController import AddWordController
from Controllers.AllWordsController import AllWordsController


class AppController:
    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.add_word_controller = AddWordController(model, view)
        self.all_words_controller = AllWordsController(model, view)






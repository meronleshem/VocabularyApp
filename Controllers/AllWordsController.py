from View.View import ViewManager


class AllWordsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["all_words_page"]
        self.bind()

    def bind(self):
        self.page.button.config(command=self.switch_page)

    def add_word(self):
        eng_word = self.page.word_entry.get()
        self.model.add_word(eng_word)

    def switch_page(self):
        self.view.show_page(self.view.pages["add_word_page"])
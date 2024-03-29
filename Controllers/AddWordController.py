from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Utils.Translator import translate_to_heb, get_word_examples


class AddWordController:
    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.page = self.view.pages["add_word_page"]
        self.bind()

    def bind(self):
        self.page.add_word_btn.config(command=self.add_word)
        self.page.all_words_btn.config(command=self.switch_page)
        self.page.translate_btn.config(command=self.translate)
        self.page.add_from_file_btn.config(command=self.add_from_file)
        self.page.quiz_btn.config(command=self.switch_to_quiz)

    def translate(self):
        eng_word = self.page.word_entry.get()
        heb_word = translate_to_heb(eng_word)
        examples = get_word_examples(eng_word)

        self.page.translate_word_label.config(text=f"{eng_word}\n{heb_word}", anchor="w")
        self.page.translate_word_examples.config(text=examples, anchor="w")

    def add_word(self):
        eng_word = self.page.word_entry.get()
        self.model.add_word(eng_word)

    def add_from_file(self):
        self.model.add_from_file()

    def switch_to_quiz(self):
        self.view.show_page(self.view.pages["quiz_page"])

    def switch_page(self):
        words_list = self.model.get_data()
        sorted_list = sorted(words_list, key=lambda x: x[0])
        self.view.pages["all_words_page"].show_words(sorted_list)
        self.view.show_page(self.view.pages["all_words_page"])

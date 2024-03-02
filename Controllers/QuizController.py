from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Utils.Translator import translate_to_heb, get_word_examples
import random


class QuizController:
    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.page = self.view.pages["quiz_page"]
        self.words_dict = {}
        self.curr_ans =""

        self.init_words_dict()
        self.bind()

    def bind(self):
        self.page.next_btn.config(command=self.new_word_quiz)
        self.page.submit_btn.config(command=self.check_answer)

    def init_words_dict(self):
        words_list = self.model.get_data()
        for eng_word, heb_word in words_list:
            self.words_dict[eng_word] = heb_word

    def check_answer(self):
        if self.page.choice.get() == self.curr_ans:
            self.page.change_color()
        else:
            print("Mistake")

    def new_word_quiz(self):
        eng_word = random.choice(list(self.words_dict.keys()))
        self.curr_ans = self.words_dict[eng_word]

        # Get three other random values
        other_options = random.sample(list(self.words_dict.values()), 3)
        other_options.append(self.curr_ans)

        while len(set(other_options)) != 4:
            other_options = random.sample(list(self.words_dict.values()), 3)
            other_options.append(self.curr_ans)

        random.shuffle(other_options)

        self.page.show_options(eng_word, self.curr_ans, other_options)
from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
import random


class QuizController:
    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.page = self.view.pages["quiz_page"]
        self.words_dict = {}
        self.curr_ans = ""

        self.init_words_dict()
        self.bind()
        self.new_word_quiz()

    def bind(self):
        self.page.next_btn.config(command=self.new_word_quiz)
        self.page.submit_btn.config(command=self.check_answer)

    def init_words_dict(self):
        words_list = self.model.get_data()
        for eng_word, heb_word, difficulty in words_list:
            self.words_dict[eng_word] = (heb_word, difficulty)

    def check_answer(self):
        if self.page.choice.get() == self.curr_ans:
            self.page.res_label.config(text="Correct!", bootstyle="success")
        else:
            self.page.res_label.config(text="Mistake! Try Again", bootstyle="danger")

    def new_word_quiz(self):
        self.page.res_label.config(text="")
        eng_word = random.choice(list(self.words_dict.keys()))
        self.curr_ans = self.words_dict[eng_word][0]
        difficuly_word = self.words_dict[eng_word][1]
        # Get three other random values
        other_options = random.sample(list(self.words_dict.values()), 3)
        other_options_words = [heb_word[0] for heb_word in other_options]
        other_options_words.append(self.curr_ans)

        while len(set(other_options_words)) != 4:
            other_options = random.sample(list(self.words_dict.values()), 3)
            other_options_words = [heb_word[0] for heb_word in other_options]
            other_options_words.append(self.curr_ans)

        random.shuffle(other_options)

        self.page.show_options(eng_word, self.curr_ans, other_options_words)

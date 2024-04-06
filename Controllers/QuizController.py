from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Utils.DiffucltyEnum import Difficulty
import random


class QuizController:
    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.page = self.view.pages["quiz_page"]
        self.words_dict = {}
        self.curr_ans = ""
        self.curr_eng_word = ""

        self.difficulties = []
        self.init_words_dict()
        self.bind()
        self.new_word_quiz()

    def bind(self):
        self.page.next_btn.config(command=self.new_word_quiz)
        self.page.submit_btn.config(command=self.check_answer)
        self.page.update_btn.config(command=self.update_difficulty)

    def update_difficulty(self):
        new_difficulty = ""
        if self.page.difficulty_choice.get() == "Easy":
            new_difficulty = Difficulty.EASY.name
        elif self.page.difficulty_choice.get() == "Medium":
            new_difficulty = Difficulty.MEDIUM.name
        elif self.page.difficulty_choice.get() == "Hard":
            new_difficulty = Difficulty.HARD.name
        else:
            return

        self.model.update_difficulty(self.curr_eng_word, new_difficulty)

    def init_words_dict(self):
        words_list = self.model.get_full_data()
        for eng_word, heb_word, difficulty in words_list:
            self.words_dict[eng_word] = (heb_word, difficulty)

    def check_answer(self):
        if self.page.choice.get() == self.curr_ans:
            self.page.res_label.config(text="Correct!", bootstyle="success")
        else:
            self.page.res_label.config(text="Mistake! Try Again", bootstyle="danger")

    def filter_difficulties(self):
        self.difficulties.clear()
        if self.page.choice_new.get() == 1:
            self.difficulties.append(Difficulty.NEW_WORD.name)
        if self.page.choice_easy.get() == 1:
            self.difficulties.append(Difficulty.EASY.name)
        if self.page.choice_medium.get() == 1:
            self.difficulties.append(Difficulty.MEDIUM.name)
        if self.page.choice_hard.get() == 1:
            self.difficulties.append(Difficulty.HARD.name)

    def color_label_by_difficulty(self, difficulty):
        color = ""
        if difficulty == Difficulty.EASY.name:
            color = "successes"
        elif difficulty == Difficulty.MEDIUM.name:
            color = "warning"
        else:
            color = "danger"

        self.page.eng_word_label.config(bootstyle=color)

    def new_word_quiz(self):
        self.filter_difficulties()
        self.page.res_label.config(text="")
        filtered_words = list(self.words_dict.keys())
        filtered_words = [word for word in filtered_words if self.words_dict[word][1] in self.difficulties]
        if len(filtered_words) == 0:
            return

        self.curr_eng_word = random.choice(filtered_words)
        self.curr_ans = self.words_dict[self.curr_eng_word][0]
        difficulty_word = self.words_dict[self.curr_eng_word][1]
        self.color_label_by_difficulty(difficulty_word)
        # Get three other random values
        other_options = random.sample(list(self.words_dict.values()), 3)
        other_options_words = [value[0] for value in other_options]
        other_options_words.append(self.curr_ans)

        while len(set(other_options_words)) != 4:
            other_options = random.sample(list(self.words_dict.values()), 3)
            other_options_words = [value[0] for value in other_options]
            other_options_words.append(self.curr_ans)

        random.shuffle(other_options_words)

        self.page.show_options(self.curr_eng_word, self.curr_ans, other_options_words)

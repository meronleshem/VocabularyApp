import tkinter as tk
from ttkbootstrap import Style
from View.AddWordPage import AddWordPage
from View.AllWordsPage import AllWordsPage
from View.QuizPage import QuizPage


class ViewManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eden")
        self.geometry("700x500")

        self.style = Style("yeti")

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {
            "add_word_page": AddWordPage(self.container),
            "all_words_page": AllWordsPage(self.container),
            "quiz_page": QuizPage(self.container)
        }

        self.curr_page = None
        self.show_page(self.pages["quiz_page"])

    def show_page(self, page):
        self.curr_page = page
        self.curr_page.grid(row=0, column=0, sticky="nsew")

        self.curr_page.tkraise()

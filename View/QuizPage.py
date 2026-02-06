# import tkinter as tk
# from tkinter import ttk
# import ttkbootstrap as tb
from tkinter import simpledialog


class GroupSelectionDialog(simpledialog.Dialog):
    def __init__(self, parent, groups):
        self.groups = groups
        self.group_vars = {}
        super().__init__(parent, title="Select Groups")

    def body(self, master):
        for group in self.groups:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(master, text=group, variable=var)
            checkbox.pack(anchor='w')
            self.group_vars[group] = var

    def apply(self):
        self.selected_groups = [group for group, var in self.group_vars.items() if var.get()]

class DifficultyDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Choose difficulty:").pack(pady=10)

        self.result = None

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        easy_button = tb.Button(button_frame, bootstyle="success-outline-toolbutton", text="Easy", width=10, command=lambda: self.set_result("Easy"))
        easy_button.pack(side=tk.LEFT, padx=5)

        medium_button = tb.Button(button_frame,bootstyle="warning-outline-toolbutton", text="Medium", width=10, command=lambda: self.set_result("Medium"))
        medium_button.pack(side=tk.LEFT, padx=5)

        hard_button = tb.Button(button_frame,bootstyle="danger-outline-toolbutton", text="Hard", width=10, command=lambda: self.set_result("Hard"))
        hard_button.pack(side=tk.LEFT, padx=5)

    def set_result(self, value):
        self.result = value
        self.ok()

    def buttonbox(self):
        # Override this method to do nothing, effectively removing the default OK and Cancel buttons
        pass

    def apply(self):
        pass

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from tkinter import simpledialog


class QuizPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ================= LEFT: QUIZ =================
        quiz_frame = ttk.Frame(self)
        quiz_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        quiz_frame.columnconfigure(0, weight=1)

        title = ttk.Label(
            quiz_frame,
            text="Quiz",
            font=("Segoe UI", 18, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.eng_word_label = ttk.Label(
            quiz_frame,
            text="",
            font=("Segoe UI", 16, "bold")
        )
        self.eng_word_label.grid(row=1, column=0, sticky="w", pady=(0, 15))

        # Options
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                quiz_frame,
                text="",
                wraplength=600,
                justify="left",
                anchor="w",
                padx=10,
                pady=6
            )
            btn.grid(row=2 + i, column=0, sticky="ew", pady=6)
            self.option_buttons.append(btn)

        self.option1_btn, self.option2_btn, self.option3_btn, self.option4_btn = self.option_buttons

        # Result
        self.res_label = ttk.Label(
            quiz_frame,
            text="",
            font=("Segoe UI", 12)
        )
        self.res_label.grid(row=6, column=0, sticky="w", pady=(15, 10))

        self.next_btn = tb.Button(
            quiz_frame,
            text="Next",
            bootstyle="primary"
        )
        self.next_btn.grid(row=7, column=0, sticky="w")

        # ================= RIGHT: SETTINGS =================
        settings = ttk.LabelFrame(self, text="Filters")
        settings.grid(row=0, column=1, sticky="nsew")
        settings.columnconfigure(0, weight=1)

        self.choice_new = tk.IntVar(value=1)
        self.choice_easy = tk.IntVar(value=1)
        self.choice_medium = tk.IntVar(value=1)
        self.choice_hard = tk.IntVar(value=1)

        ttk.Checkbutton(settings, text="New", variable=self.choice_new).grid(sticky="w", pady=4)
        ttk.Checkbutton(settings, text="Easy", variable=self.choice_easy).grid(sticky="w", pady=4)
        ttk.Checkbutton(settings, text="Medium", variable=self.choice_medium).grid(sticky="w", pady=4)
        ttk.Checkbutton(settings, text="Hard", variable=self.choice_hard).grid(sticky="w", pady=4)

        self.update_btn = tb.Button(
            settings,
            text="Update Difficulty",
            bootstyle="warning-outline"
        )
        self.update_btn.grid(sticky="ew", pady=(10, 5))

        self.select_groups_btn = tb.Button(
            settings,
            text="Select Groups",
            bootstyle="secondary-outline"
        )
        self.select_groups_btn.grid(sticky="ew")

    # ===== API used by controller =====
    def show_options(self, eng_word, heb_ans, options_list):
        self.eng_word_label.config(text=eng_word)

        self.option1_btn.config(text=options_list[0])
        self.option2_btn.config(text=options_list[1])
        self.option3_btn.config(text=options_list[2])
        self.option4_btn.config(text=options_list[3])

    def change_color(self):
        pass


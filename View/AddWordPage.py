import tkinter as tk
from tkinter import ttk


class AddWordPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(sticky="nsew", padx=20, pady=20)

        # ===== Layout config =====
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # ===== LEFT SIDE =====
        left = ttk.Frame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        left.columnconfigure(0, weight=1)

        # --- Add word section ---
        add_frame = ttk.LabelFrame(left, text="Add New Word")
        add_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        add_frame.columnconfigure(0, weight=1)

        self.word_entry = ttk.Entry(add_frame, font=("Segoe UI", 11))
        self.word_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_row = ttk.Frame(add_frame)
        btn_row.grid(row=1, column=0, pady=(0, 10))

        self.add_word_btn = ttk.Button(btn_row, text="Add Word")
        self.add_word_btn.grid(row=0, column=0, padx=5)

        self.translate_btn = ttk.Button(btn_row, text="Translate")
        self.translate_btn.grid(row=0, column=1, padx=5)

        # --- Actions section ---
        actions_frame = ttk.LabelFrame(left, text="Actions")
        actions_frame.grid(row=1, column=0, sticky="ew")
        actions_frame.columnconfigure(0, weight=1)

        self.add_from_text_file_btn = ttk.Button(
            actions_frame, text="Add Words from Text File"
        )
        self.add_from_text_file_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.add_from_pdf_btn = ttk.Button(
            actions_frame, text="Add Words from PDF"
        )
        self.add_from_pdf_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.all_words_btn = ttk.Button(
            actions_frame, text="Show All Words"
        )
        self.all_words_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.quiz_btn = ttk.Button(actions_frame, text="Quiz")
        self.quiz_btn.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")

        # ===== RIGHT SIDE =====
        right = ttk.LabelFrame(self, text="Translation")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.translate_word_label = ttk.Label(
            right,
            text="",
            font=("Segoe UI", 12, "bold"),
            wraplength=400,
            justify="left",
        )
        self.translate_word_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.translate_word_examples = ttk.Label(
            right,
            text="",
            font=("Segoe UI", 11),
            wraplength=400,
            justify="left",
        )
        self.translate_word_examples.grid(
            row=1, column=0, padx=10, pady=(0, 10), sticky="w"
        )

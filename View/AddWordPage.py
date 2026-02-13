"""
Add Word Page - Modern Professional Design

Features:
- Gradient background
- Modern card-based layout
- Beautiful buttons with icons
- Professional color scheme
"""
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


class AddWordPage(tk.Frame):
    """
    Modern home page for adding words.

    Features:
    - Beautiful gradient background
    - Card-based sections
    - Modern button styling
    - Professional design
    """

    def __init__(self, parent):
        super().__init__(parent, bg="#e8eaf6")  # Light purple gradient background

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Create layout
        self._create_left_panel()
        self._create_right_panel()

    def _create_left_panel(self):
        """Create left panel with add word and actions."""
        # Left container
        left = tk.Frame(self, bg="#e8eaf6")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left.columnconfigure(0, weight=1)

        # Add word card
        self._create_add_word_card(left)

        # Actions card
        self._create_actions_card(left)

    def _create_add_word_card(self, parent):
        """Create modern add word card."""
        # Card frame with elevation
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        card.columnconfigure(0, weight=1)

        # Header
        header = tk.Frame(card, bg="#3f51b5", height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="Add New Word",
                 font=("Segoe UI", 13, "bold"),
                 bg="#3f51b5", fg="#ffffff").pack(side="left", padx=15, pady=12)

        # Content
        content = tk.Frame(card, bg="#ffffff")
        content.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        content.columnconfigure(0, weight=1)

        # Entry with modern styling
        tk.Label(content, text="Enter word:", font=("Segoe UI", 9),
                 bg="#ffffff", fg="#666").grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.word_entry = tb.Entry(content, font=("Segoe UI", 12))
        self.word_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Buttons row
        btn_row = tk.Frame(content, bg="#ffffff")
        btn_row.grid(row=2, column=0, sticky="ew")

        self.add_word_btn = tb.Button(btn_row, text="➕ Add Word",
                                      bootstyle="success", width=15)
        self.add_word_btn.pack(side="left", padx=(0, 8))

        self.translate_btn = tb.Button(btn_row, text="Translate",
                                       bootstyle="info-outline", width=15)
        self.translate_btn.pack(side="left")

        self.sound_btn = tb.Button(btn_row, text="sound",
                                       bootstyle="info-outline", width=15)
        self.sound_btn.pack(side="left")

    def _create_actions_card(self, parent):
        """Create modern actions card."""
        # Card frame
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=1, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        # Header
        header = tk.Frame(card, bg="#5e35b1", height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="🚀 Quick Actions",
                 font=("Segoe UI", 13, "bold"),
                 bg="#5e35b1", fg="#ffffff").pack(side="left", padx=15, pady=12)

        # Content
        content = tk.Frame(card, bg="#ffffff")
        content.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        content.columnconfigure(0, weight=1)

        # Modern action buttons
        self.add_from_text_file_btn = tb.Button(
            content,
            text="Add from Text File",
            bootstyle="primary-outline",
            width=25
        )
        self.add_from_text_file_btn.grid(row=0, column=0, sticky="ew", pady=4)

        self.add_from_pdf_btn = tb.Button(
            content,
            text="Add from PDF",
            bootstyle="primary-outline",
            width=25
        )
        self.add_from_pdf_btn.grid(row=1, column=0, sticky="ew", pady=4)

        # Divider
        tk.Frame(content, bg="#e0e0e0", height=1).grid(
            row=2, column=0, sticky="ew", pady=12
        )

        self.all_words_btn = tb.Button(
            content,
            text="Show All Words",
            bootstyle="info",
            width=25
        )
        self.all_words_btn.grid(row=3, column=0, sticky="ew", pady=4)

        self.quiz_btn = tb.Button(
            content,
            text="Start Quiz",
            bootstyle="success",
            width=25
        )
        self.quiz_btn.grid(row=4, column=0, sticky="ew", pady=4)

    def _create_right_panel(self):
        """Create right panel with translation display."""
        # Right container
        right = tk.Frame(self, bg="#e8eaf6")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        # Translation card
        card = tk.Frame(right, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)

        # Header
        header = tk.Frame(card, bg="#00897b", height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="Translation",
                 font=("Segoe UI", 13, "bold"),
                 bg="#00897b", fg="#ffffff").pack(side="left", padx=15, pady=12)

        # Content area with scroll
        content = tk.Frame(card, bg="#ffffff")
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        # Scrollable area
        canvas = tk.Canvas(content, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Translation content
        translation_content = tk.Frame(scrollable_frame, bg="#ffffff")
        translation_content.pack(fill="both", expand=True, padx=20, pady=20)

        # Word label
        tk.Label(translation_content, text="Hebrew Translation:",
                 font=("Segoe UI", 9), bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 5))

        self.translate_word_label = tk.Label(
            translation_content,
            text="Translation will appear here",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg="#283593",
            wraplength=400,
            justify="left"
        )
        self.translate_word_label.pack(anchor="w", pady=(0, 20))

        # Examples label
        tk.Label(translation_content, text="Usage Examples:",
                 font=("Segoe UI", 9), bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 5))

        self.translate_word_examples = tk.Label(
            translation_content,
            text="Enter a word and click 'Translate' to see examples",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#37474f",
            wraplength=400,
            justify="left"
        )
        self.translate_word_examples.pack(anchor="w")

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

"""
Quiz Page - Modern UI for Vocabulary Quiz

This module provides an improved quiz interface with:
- Card-based design
- Better visual feedback
- Progress tracking
- Smooth animations
- Responsive layout
"""
import tkinter as tk
from tkinter import ttk, simpledialog
import ttkbootstrap as tb
from typing import List, Optional


# ==================== Dialogs ====================

class GroupSelectionDialog(simpledialog.Dialog):
    """Dialog for selecting multiple groups for quiz filtering."""

    def __init__(self, parent, groups: List[str]):
        self.groups = groups
        self.group_vars = {}
        self.selected_groups = []
        super().__init__(parent, title="Select Quiz Groups")

    def body(self, master):
        """Create dialog body with checkboxes."""
        # Title
        title = tk.Label(
            master,
            text="Select groups to include in quiz:",
            font=("Segoe UI", 11, "bold")
        )
        title.pack(pady=(0, 15))

        # Scrollable frame for many groups
        canvas = tk.Canvas(master, height=300)
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add checkboxes
        for group in sorted(self.groups):
            var = tk.BooleanVar(value=True)  # Default: all selected
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=group,
                variable=var
            )
            cb.pack(anchor="w", padx=10, pady=3)
            self.group_vars[group] = var

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Select/Deselect all buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="Select All",
            command=self._select_all
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Deselect All",
            command=self._deselect_all
        ).pack(side="left", padx=5)

    def _select_all(self):
        """Select all groups."""
        for var in self.group_vars.values():
            var.set(True)

    def _deselect_all(self):
        """Deselect all groups."""
        for var in self.group_vars.values():
            var.set(False)

    def apply(self):
        """Called when OK is pressed."""
        self.selected_groups = [
            group for group, var in self.group_vars.items() if var.get()
        ]


class DifficultyDialog(simpledialog.Dialog):
    """Dialog for changing word difficulty."""

    def __init__(self, parent):
        self.result = None
        super().__init__(parent, title="Update Difficulty")

    def body(self, master):
        """Create dialog body with difficulty buttons."""
        # Title
        tk.Label(
            master,
            text="Select new difficulty level:",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(0, 20))

        # Button frame
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        # Difficulty buttons with colors
        tb.Button(
            button_frame,
            text="Easy",
            bootstyle="success-outline",
            width=12,
            command=lambda: self.set_result("Easy")
        ).pack(side=tk.LEFT, padx=8)

        tb.Button(
            button_frame,
            text="Medium",
            bootstyle="warning-outline",
            width=12,
            command=lambda: self.set_result("Medium")
        ).pack(side=tk.LEFT, padx=8)

        tb.Button(
            button_frame,
            text="Hard",
            bootstyle="danger-outline",
            width=12,
            command=lambda: self.set_result("Hard")
        ).pack(side=tk.LEFT, padx=8)

    def set_result(self, value: str):
        """Set result and close dialog."""
        self.result = value
        self.ok()

    def buttonbox(self):
        """Override to hide default OK/Cancel buttons."""
        pass


# ==================== Main Quiz Page ====================

class QuizPage(tk.Frame):
    """
    Modern quiz page with improved UI/UX.

    Features:
    - Card-based layout
    - Visual progress bar
    - Difficulty color coding
    - Better button styling
    - Responsive design
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Configure main grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Main content area

        # Colors for difficulty
        self.difficulty_colors = {
            "NEW_WORD": "#6c757d",  # Gray
            "EASY": "#28a745",  # Green
            "MEDIUM": "#ffc107",  # Yellow
            "HARD": "#dc3545"  # Red
        }

        # Initialize filters
        self.choice_new = tk.IntVar(value=1)
        self.choice_easy = tk.IntVar(value=1)
        self.choice_medium = tk.IntVar(value=1)
        self.choice_hard = tk.IntVar(value=1)

        # Create UI sections
        self._create_header()
        self._create_main_content()
        self._create_sidebar()

    def _create_header(self):
        """Create header with title and back button."""
        header_frame = tk.Frame(self, bg="#f8f9fa", height=70)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.grid_propagate(False)

        # Content container
        header_content = tk.Frame(header_frame, bg="#f8f9fa")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)

        # Back button
        self.back_btn = tb.Button(
            header_content,
            text="← Back",
            bootstyle="secondary-outline",
            width=10
        )
        self.back_btn.pack(side="left")

        # Title
        title = tk.Label(
            header_content,
            text="Vocabulary Quiz",
            font=("Segoe UI", 20, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        title.pack(side="left", padx=30)

        # Progress indicator
        self.progress_label = tk.Label(
            header_content,
            text="Question 0 of 0",
            font=("Segoe UI", 12),
            bg="#f8f9fa",
            fg="#6c757d"
        )
        self.progress_label.pack(side="right")

    def _create_main_content(self):
        """Create main quiz content area."""
        # Main container
        main_container = tk.Frame(self, bg="#ffffff")
        main_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        main_container.columnconfigure(0, weight=1)

        # Question card
        self._create_question_card(main_container)

        # Answer options
        self._create_answer_options(main_container)

        # Result and Next button
        self._create_result_section(main_container)

    def _create_question_card(self, parent):
        """Create the question display card."""
        # Card frame with border
        card_frame = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#dee2e6",
            highlightthickness=2
        )
        card_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))

        # Card content
        card_content = tk.Frame(card_frame, bg="#ffffff")
        card_content.pack(fill="both", expand=True, padx=30, pady=30)

        # Label above word
        question_label = tk.Label(
            card_content,
            text="Translate this word:",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#6c757d"
        )
        question_label.pack(pady=(0, 15))

        # English word display
        self.eng_word_label = tk.Label(
            card_content,
            text="",
            font=("Segoe UI", 32, "bold"),
            bg="#ffffff",
            fg="#212529",
            wraplength=600
        )
        self.eng_word_label.pack()

        # Difficulty badge
        self.difficulty_badge = tk.Label(
            card_content,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#ffffff",
            padx=12,
            pady=4
        )
        self.difficulty_badge.pack(pady=(15, 0))

    def _create_answer_options(self, parent):
        """Create answer option buttons."""
        # Container for options
        options_frame = tk.Frame(parent, bg="#ffffff")
        options_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        options_frame.columnconfigure(0, weight=1)

        # Create 4 option buttons
        self.option_buttons = []

        for i in range(4):
            # Button frame
            btn_frame = tk.Frame(
                options_frame,
                bg="#ffffff",
                highlightbackground="#dee2e6",
                highlightthickness=1,
                height=70
            )
            btn_frame.grid(row=i, column=0, sticky="ew", pady=6)
            btn_frame.grid_propagate(False)
            btn_frame.columnconfigure(0, weight=1)

            # Option button
            btn = tk.Button(
                btn_frame,
                text="",
                font=("Segoe UI", 14),
                bg="#ffffff",
                fg="#212529",
                activebackground="#e9ecef",
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=20
            )
            btn.grid(row=0, column=0, sticky="nsew")

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#f8f9fa"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#ffffff"))

            self.option_buttons.append(btn)

    def _create_result_section(self, parent):
        """Create result display and next button."""
        result_frame = tk.Frame(parent, bg="#ffffff")
        result_frame.grid(row=2, column=0, sticky="ew")
        result_frame.columnconfigure(0, weight=1)

        # Result label
        self.res_label = tk.Label(
            result_frame,
            text="",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff"
        )
        self.res_label.grid(row=0, column=0, pady=(0, 15))

        # Next button
        self.next_btn = tb.Button(
            result_frame,
            text="Next Question →",
            bootstyle="primary",
            width=20
        )
        self.next_btn.grid(row=1, column=0)

    def _create_sidebar(self):
        """Create sidebar with filters and controls."""
        # Sidebar container
        sidebar = tk.Frame(self, bg="#f8f9fa", width=280)
        sidebar.grid(row=1, column=1, sticky="ns", padx=(0, 30), pady=20)
        sidebar.grid_propagate(False)

        # Padding frame
        sidebar_content = tk.Frame(sidebar, bg="#f8f9fa")
        sidebar_content.pack(fill="both", expand=True, padx=20, pady=20)

        # Filters section
        self._create_filters_section(sidebar_content)

        # Actions section
        self._create_actions_section(sidebar_content)

        # Statistics section (optional)
        self._create_stats_section(sidebar_content)

    def _create_filters_section(self, parent):
        """Create difficulty filters section."""
        # Section title
        title = tk.Label(
            parent,
            text="Filter by Difficulty",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        title.pack(anchor="w", pady=(0, 15))

        # Filter checkboxes
        filters_frame = tk.Frame(parent, bg="#f8f9fa")
        filters_frame.pack(fill="x", pady=(0, 25))

        # New words
        cb_new = ttk.Checkbutton(
            filters_frame,
            text="New Words",
            variable=self.choice_new
        )
        cb_new.pack(anchor="w", pady=3)

        # Easy
        cb_easy = ttk.Checkbutton(
            filters_frame,
            text="Easy",
            variable=self.choice_easy
        )
        cb_easy.pack(anchor="w", pady=3)

        # Medium
        cb_medium = ttk.Checkbutton(
            filters_frame,
            text="Medium",
            variable=self.choice_medium
        )
        cb_medium.pack(anchor="w", pady=3)

        # Hard
        cb_hard = ttk.Checkbutton(
            filters_frame,
            text="Hard",
            variable=self.choice_hard
        )
        cb_hard.pack(anchor="w", pady=3)

    def _create_actions_section(self, parent):
        """Create action buttons section."""
        # Section title
        title = tk.Label(
            parent,
            text="Actions",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        title.pack(anchor="w", pady=(0, 15))

        # Action buttons
        actions_frame = tk.Frame(parent, bg="#f8f9fa")
        actions_frame.pack(fill="x", pady=(0, 25))

        # Select groups button
        self.select_groups_btn = tb.Button(
            actions_frame,
            text="📚 Select Groups",
            bootstyle="info-outline",
            width=22
        )
        self.select_groups_btn.pack(fill="x", pady=5)

        # Update difficulty button
        self.update_btn = tb.Button(
            actions_frame,
            text="✏️ Update Difficulty",
            bootstyle="warning-outline",
            width=22
        )
        self.update_btn.pack(fill="x", pady=5)

        # Start new quiz button
        self.new_quiz_btn = tb.Button(
            actions_frame,
            text="🔄 New Quiz",
            bootstyle="success-outline",
            width=22
        )
        self.new_quiz_btn.pack(fill="x", pady=5)

    def _create_stats_section(self, parent):
        """Create statistics section."""
        # Section title
        title = tk.Label(
            parent,
            text="Session Stats",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        title.pack(anchor="w", pady=(0, 15))

        # Stats container
        stats_frame = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#dee2e6",
            highlightthickness=1
        )
        stats_frame.pack(fill="x")

        stats_content = tk.Frame(stats_frame, bg="#ffffff")
        stats_content.pack(fill="both", padx=15, pady=15)

        # Correct answers
        self.correct_label = tk.Label(
            stats_content,
            text="Correct: 0",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#28a745"
        )
        self.correct_label.pack(anchor="w", pady=2)

        # Wrong answers
        self.wrong_label = tk.Label(
            stats_content,
            text="Wrong: 0",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#dc3545"
        )
        self.wrong_label.pack(anchor="w", pady=2)

        # Accuracy
        self.accuracy_label = tk.Label(
            stats_content,
            text="Accuracy: 0%",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#212529"
        )
        self.accuracy_label.pack(anchor="w", pady=(8, 2))

    # ==================== Public Methods ====================

    def show_options(self, eng_word: str, heb_ans: str, options_list: List[str]):
        """
        Display a new question with answer options.

        Args:
            eng_word: English word to translate
            heb_ans: Correct Hebrew answer
            options_list: List of 4 Hebrew options
        """
        # Update question
        self.eng_word_label.config(text=eng_word)

        # Update option buttons
        for btn, text in zip(self.option_buttons, options_list):
            btn.config(
                text=text,
                bg="#ffffff",
                fg="#212529",
                state="normal"
            )

        # Clear result
        self.res_label.config(text="")

    def show_result(self, is_correct: bool, correct_answer: Optional[str] = None):
        """
        Show result after answer selection.

        Args:
            is_correct: Whether answer was correct
            correct_answer: The correct answer (optional)
        """
        if is_correct:
            self.res_label.config(
                text="✓ Correct!",
                fg="#28a745"
            )
        else:
            text = "✗ Wrong!"
            if correct_answer:
                text += f" (Correct: {correct_answer})"
            self.res_label.config(
                text=text,
                fg="#dc3545"
            )

    def update_difficulty_badge(self, difficulty: str):
        """
        Update the difficulty badge color and text.

        Args:
            difficulty: Difficulty level name
        """
        color = self.difficulty_colors.get(difficulty, "#6c757d")

        # Format text
        display_text = difficulty.replace("_", " ").title()

        self.difficulty_badge.config(
            text=display_text,
            bg=color
        )

    def update_progress(self, current: int, total: int):
        """
        Update progress display.

        Args:
            current: Current question number
            total: Total questions
        """
        self.progress_label.config(
            text=f"Question {current} of {total}"
        )

    def update_stats(self, correct: int, wrong: int):
        """
        Update session statistics.

        Args:
            correct: Number of correct answers
            wrong: Number of wrong answers
        """
        total = correct + wrong
        accuracy = (correct / total * 100) if total > 0 else 0

        self.correct_label.config(text=f"Correct: {correct}")
        self.wrong_label.config(text=f"Wrong: {wrong}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")

    def reset_button_colors(self):
        """Reset all option buttons to default state."""
        for btn in self.option_buttons:
            btn.config(
                bg="#ffffff",
                fg="#212529",
                state="normal"
            )

    def highlight_answer(self, button_index: int, is_correct: bool):
        """
        Highlight a button as correct or incorrect.

        Args:
            button_index: Index of button to highlight
            is_correct: Whether this is the correct answer
        """
        btn = self.option_buttons[button_index]

        if is_correct:
            btn.config(bg="#d4edda", fg="#155724")
        else:
            btn.config(bg="#f8d7da", fg="#721c24")

"""
Quiz Controller
"""
import random
from typing import Dict, Tuple, List, Optional
from tkinter import messagebox
from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Utils.DiffucltyEnum import Difficulty
from View.QuizPage import DifficultyDialog, GroupSelectionDialog
from View.QuizSetupDialog import QuizSetupDialog
from View.QuizResultsDialog import QuizResultsDialog
from Utils.SoundUtil import play_sound

class QuizController:
    """
    Controller for Quiz page.
    """

    def __init__(self, model: DatabaseManager, view: ViewManager):
        self.model = model
        self.view = view
        self.page = self.view.pages["quiz_page"]

        # Word storage
        self.words_dict: Dict[str, Tuple[str, str]] = {}
        self.all_words_dict: Dict[str, Tuple[str, str]] = {}

        # Quiz state
        self.curr_ans: str = ""
        self.curr_eng_word: str = ""
        self.filtered_words: List[str] = []
        self.word_index: int = 0
        self.total_questions: int = 0
        self.new_quiz: bool = True
        self.answer_selected: bool = False
        self.difficulties: List[str] = []
        self.quiz_configured: bool = False  # Track if quiz has been configured

        # Statistics
        self.correct_count: int = 0
        self.wrong_count: int = 0

        # Mistake tracking - List of (english, user_answer, correct_answer)
        self.mistakes: List[Tuple[str, str, str]] = []

        # Quiz configuration
        self.max_questions: Optional[int] = None

        # Initialize
        self.init_words_dict()
        self.bind()

        # Show welcome message
        self._show_welcome_message()

        # HOOK: Show dialog when page becomes visible
        self.page.bind("<Visibility>", self._on_page_visible)

    def _on_page_visible(self, event):
        """
        Called when quiz page becomes visible.
        Shows setup dialog on first visit.
        """
        # Only show dialog once per session
        if not self.quiz_configured:
            # Delay slightly to ensure page is fully shown
            self.page.after(100, self._show_initial_setup)

    def _show_initial_setup(self):
        """Show setup dialog for first-time configuration."""
        if not self.quiz_configured:
            self.show_setup_dialog()

    def _show_welcome_message(self):
        """Show welcome message before quiz starts."""
        self.page.eng_word_label.config(text="Welcome to Quiz!")
        self.page.res_label.config(
            text="Configuring your quiz...",
            fg="#666"
        )
        self.page.next_btn.config(state="disabled")

        for btn in self.page.option_buttons:
            btn.config(text="", state="disabled")

    def bind(self):
        """Bind UI events."""
        self.page.back_btn.config(command=self.go_back)
        self.page.next_btn.config(command=self.next_question)

        # Answer buttons
        for i, btn in enumerate(self.page.option_buttons):
            btn.config(command=lambda idx=i, b=btn: self.check_answer(idx, b))

        # Control buttons
        self.page.update_btn.config(command=self.update_difficulty)
        self.page.select_groups_btn.config(command=self.select_groups)

        # New Quiz button - show setup dialog
        if hasattr(self.page, 'new_quiz_btn'):
            self.page.new_quiz_btn.config(command=self.start_new_quiz_with_dialog)

        # Filter changes
        self.page.choice_new.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_easy.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_medium.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_hard.trace('w', lambda *args: self._on_filter_change())

    def _on_filter_change(self):
        """Handle filter changes."""
        if self.quiz_configured:
            self.new_quiz = True

    # ==================== Initialization ====================

    def init_words_dict(self):
        """Load words from database."""
        try:
            words_list = self.model.get_full_data()
            for eng_word, heb_word, difficulty, group_name in words_list:
                self.words_dict[eng_word] = (heb_word, difficulty)
                self.all_words_dict[eng_word] = (heb_word, difficulty)
        except Exception as e:
            print(f"Error loading words: {e}")

    def show_setup_dialog(self):
        """Show quiz setup dialog."""
        try:
            # Get available groups
            groups_data = self.model.get_all_groups_names()
            groups = [row[0] for row in groups_data] if groups_data else []

            # Show setup dialog
            dialog = QuizSetupDialog(self.view, groups)

            if dialog.result:
                # Mark as configured
                self.quiz_configured = True

                # Apply configuration
                config = dialog.result

                # Set difficulties
                self._apply_difficulty_filters(config['difficulties'])

                # Set groups filter if selected
                if config['groups']:
                    self._filter_by_groups(config['groups'])

                # Set question limit
                self.max_questions = config['question_count']

                # Start quiz
                self.start_quiz()

                return True
            else:
                # User cancelled - go back to home
                self.go_back()
                return False

        except Exception as e:
            print(f"Error in setup dialog: {e}")
            messagebox.showerror("Error", f"Failed to start quiz: {e}")
            self.go_back()
            return False

    def _apply_difficulty_filters(self, difficulties: List[str]):
        """Apply difficulty filters from setup dialog."""
        self.page.choice_new.set(1 if "NEW_WORD" in difficulties else 0)
        self.page.choice_easy.set(1 if "EASY" in difficulties else 0)
        self.page.choice_medium.set(1 if "MEDIUM" in difficulties else 0)
        self.page.choice_hard.set(1 if "HARD" in difficulties else 0)

    def start_quiz(self):
        """Start quiz with current settings."""
        self.new_quiz = True
        self.correct_count = 0
        self.wrong_count = 0
        self.mistakes = []  # Reset mistakes
        self.page.update_stats(0, 0)
        self.new_word_quiz()

    def start_new_quiz_with_dialog(self):
        """
        Start a new quiz by showing the setup dialog.
        This is called when the 'New Quiz' button is clicked.
        """
        # Reset configuration flag so dialog shows again
        self.quiz_configured = False

        # Show setup dialog
        self.show_setup_dialog()

    # ==================== Navigation ====================

    def go_back(self):
        """Go back to home page."""
        self.quiz_configured = False  # Reset for next time
        self.view.show_page(self.view.pages["add_word_page"])

    # ==================== Quiz Flow ====================

    def new_word_quiz(self):
        """Load and display new question."""
        # Initialize if needed
        if self.new_quiz or self.word_index >= self.total_questions:
            self._initialize_quiz()

        # Check if words available
        if not self.filtered_words:
            self._show_no_words()
            return

        # Reset state
        self.page.res_label.config(text="")
        self.page.reset_button_colors()
        self.answer_selected = False

        # Get word
        self.curr_eng_word = self.filtered_words[self.word_index]
        self.curr_ans = self.words_dict[self.curr_eng_word][0]
        difficulty = self.words_dict[self.curr_eng_word][1]

        # Update UI
        self.page.update_difficulty_badge(difficulty)
        options = self._generate_options()
        self.word_index += 1
        self.page.update_progress(self.word_index, self.total_questions)
        self.page.show_options(self.curr_eng_word, self.curr_ans, options)
        play_sound(self.curr_eng_word)
        self.page.next_btn.config(state="enabled")

    def next_question(self):
        """Move to next question."""
        if not self.answer_selected:
            self.wrong_count += 1
            self.page.update_stats(self.correct_count, self.wrong_count)

        self.new_word_quiz()

    def _initialize_quiz(self):
        """Initialize quiz with filtered words."""
        self.filter_difficulties()
        self.page.res_label.config(text="")

        # Filter words
        self.filtered_words = [
            word for word in self.words_dict.keys()
            if self.words_dict[word][1] in self.difficulties
        ]

        # Apply question limit if set
        if self.max_questions and len(self.filtered_words) > self.max_questions:
            random.shuffle(self.filtered_words)
            self.filtered_words = self.filtered_words[:self.max_questions]
        else:
            random.shuffle(self.filtered_words)

        self.new_quiz = False
        self.word_index = 0
        self.total_questions = len(self.filtered_words)

    def _generate_options(self) -> List[str]:
        """Generate 4 answer options."""
        attempts = 0
        while attempts < 10:
            others = random.sample(list(self.all_words_dict.values()), 3)
            options = [v[0] for v in others]
            options.append(self.curr_ans)

            if len(set(options)) == 4:
                random.shuffle(options)
                return options
            attempts += 1

        options = [self.curr_ans, "---", "---", "---"]
        random.shuffle(options)
        return options

    def _show_no_words(self):
        """Show no words message."""
        self.page.eng_word_label.config(text="No words available")
        self.page.res_label.config(text="Check your filters or add more words", fg="#666")
        for btn in self.page.option_buttons:
            btn.config(text="", state="disabled")
        self.page.next_btn.config(state="disabled")

    # ==================== Answer Checking ====================

    def check_answer(self, button_index: int, button):
        """Check if answer is correct."""
        if self.answer_selected:
            return

        self.answer_selected = True
        selected = button.cget("text")
        is_correct = (selected == self.curr_ans)

        # Update stats
        if is_correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1
            # Track mistake: (english_word, user_answer, correct_answer)
            self.mistakes.append((self.curr_eng_word, selected, self.curr_ans))

        self.page.update_stats(self.correct_count, self.wrong_count)

        # Visual feedback
        self.page.highlight_answer(button_index, is_correct)

        # Highlight correct answer if wrong
        if not is_correct:
            for i, btn in enumerate(self.page.option_buttons):
                if btn.cget("text") == self.curr_ans:
                    self.page.highlight_answer(i, True)
                    break

        # Disable buttons
        for btn in self.page.option_buttons:
            btn.config(state="disabled")

        # Show result
        self.page.show_result(is_correct, self.curr_ans if not is_correct else None)

        # Check if quiz is finished
        if self.word_index >= self.total_questions:
            # Schedule results dialog to show after current question result is visible
            self.page.after(1500, self._show_results_dialog)

    # ==================== Difficulty ====================

    def filter_difficulties(self):
        """Apply difficulty filters."""
        self.difficulties.clear()

        if self.page.choice_new.get() == 1:
            self.difficulties.append(Difficulty.NEW_WORD.name)
        if self.page.choice_easy.get() == 1:
            self.difficulties.append(Difficulty.EASY.name)
        if self.page.choice_medium.get() == 1:
            self.difficulties.append(Difficulty.MEDIUM.name)
        if self.page.choice_hard.get() == 1:
            self.difficulties.append(Difficulty.HARD.name)

    def update_difficulty(self):
        """Update current word difficulty."""
        if not self.curr_eng_word:
            return

        dialog = DifficultyDialog(self.page)
        if not dialog.result:
            return

        difficulty_map = {
            "Easy": Difficulty.EASY.name,
            "Medium": Difficulty.MEDIUM.name,
            "Hard": Difficulty.HARD.name
        }

        new_diff = difficulty_map.get(dialog.result)
        if new_diff:
            try:
                self.model.update_difficulty(self.curr_eng_word, new_diff)
                heb = self.words_dict[self.curr_eng_word][0]
                self.words_dict[self.curr_eng_word] = (heb, new_diff)
                self.all_words_dict[self.curr_eng_word] = (heb, new_diff)
                self.page.res_label.config(text=f"Updated to {dialog.result}!", fg="#28a745")
            except Exception as e:
                print(f"Error: {e}")
                self.page.res_label.config(text="Update failed", fg="#dc3545")

    # ==================== Group Filtering ====================

    def select_groups(self):
        """Select groups for filtering."""
        try:
            groups_data = self.model.get_all_groups_names()
            groups = [row[0] for row in groups_data]

            if not groups:
                self.page.res_label.config(text="No groups available", fg="#666")
                return

            dialog = GroupSelectionDialog(self.page, groups)
            selected = getattr(dialog, 'selected_groups', [])

            if selected:
                self._filter_by_groups(selected)
                # Restart quiz with new groups
                if self.quiz_configured:
                    self.start_quiz()

        except Exception as e:
            print(f"Error: {e}")
            self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")

    def _filter_by_groups(self, selected_groups: List[str]):
        """Filter words by groups."""
        try:
            words_data = self.model.get_words_by_groups(selected_groups)
            self.words_dict = {}

            for eng, heb, diff, grp in words_data:
                self.words_dict[eng] = (heb, diff)

            self.new_quiz = True

            group_names = ", ".join(selected_groups[:3])
            if len(selected_groups) > 3:
                group_names += f" +{len(selected_groups) - 3} more"

            self.page.res_label.config(text=f"Filtered to: {group_names}", fg="#28a745")

        except Exception as e:
            print(f"Error: {e}")
            self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")

    # ==================== Quiz Results ====================

    def _show_results_dialog(self):
        """Show quiz results dialog at end of quiz."""
        try:
            # Show results dialog
            dialog = QuizResultsDialog(
                self.page,
                self.correct_count,
                self.wrong_count,
                self.mistakes
            )

            # Handle user action
            if dialog.action == "new_quiz":
                # Start new quiz with setup dialog
                self.start_new_quiz_with_dialog()
            elif dialog.action == "review":
                # Could implement review mode here
                # For now, just show a message
                self.page.res_label.config(
                    text="Review mode: Study the mistakes shown in the dialog",
                    fg="#1e88e5"
                )

        except Exception as e:
            print(f"Error showing results dialog: {e}")

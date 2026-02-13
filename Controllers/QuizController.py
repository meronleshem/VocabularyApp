"""
Quiz Controller - Business logic for Quiz page

Improved version with:
- Session statistics tracking
- Better answer validation
- Smooth quiz flow
- Enhanced error handling
"""
import random
from typing import Dict, Tuple, List, Optional
from View.View import ViewManager
from Database.DatabaseManager import DatabaseManager
from Utils.DiffucltyEnum import Difficulty
from View.QuizPage import DifficultyDialog, GroupSelectionDialog


class QuizController:
    """
    Controller for the Quiz page.

    Manages:
    - Quiz state and flow
    - Answer checking
    - Statistics tracking
    - Difficulty filtering
    - Group filtering
    """

    def __init__(self, model: DatabaseManager, view: ViewManager):
        """
        Initialize the quiz controller.

        Args:
            model: Database manager
            view: View manager
        """
        self.model = model
        self.view = view
        self.page = self.view.pages["quiz_page"]

        # Word dictionaries
        self.words_dict: Dict[str, Tuple[str, str]] = {}  # {eng: (heb, difficulty)}
        self.all_words_dict: Dict[str, Tuple[str, str]] = {}

        # Current quiz state
        self.curr_ans: str = ""
        self.curr_eng_word: str = ""
        self.current_index: int = 0
        self.total_questions: int = 0
        self.filtered_words: List[str] = []
        self.word_index: int = 0

        # Quiz control
        self.new_quiz: bool = True
        self.difficulties: List[str] = []
        self.answer_selected: bool = False

        # Statistics
        self.correct_count: int = 0
        self.wrong_count: int = 0

        # Initialize
        self.init_words_dict()
        self.bind()

    def bind(self):
        """Bind UI events to controller methods."""
        # Navigation
        self.page.back_btn.config(command=self.go_back)
        self.page.next_btn.config(command=self.next_question)

        # Answer buttons
        for i, btn in enumerate(self.page.option_buttons):
            btn.config(command=lambda idx=i, b=btn: self.check_answer(idx, b))

        # Action buttons
        self.page.update_btn.config(command=self.update_difficulty)
        self.page.select_groups_btn.config(command=self.select_groups)

        # New quiz button
        if hasattr(self.page, 'new_quiz_btn'):
            self.page.new_quiz_btn.config(command=self.start_new_quiz)

        # Difficulty checkboxes - trigger quiz restart
        self.page.choice_new.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_easy.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_medium.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_hard.trace('w', lambda *args: self._on_filter_change())

    # ==================== Navigation ====================

    def go_back(self):
        """Navigate back to home page."""
        self.view.show_page(self.view.pages["add_word_page"])

    # ==================== Quiz Initialization ====================

    def init_words_dict(self):
        """Load all words from database into dictionaries."""
        try:
            words_list = self.model.get_full_data()

            for eng_word, heb_word, difficulty, group_name in words_list:
                self.words_dict[eng_word] = (heb_word, difficulty)
                self.all_words_dict[eng_word] = (heb_word, difficulty)

        except Exception as e:
            print(f"Error loading words: {e}")

    def start_new_quiz(self):
        """Start a completely new quiz session."""
        self.new_quiz = True
        self.correct_count = 0
        self.wrong_count = 0
        self.page.update_stats(0, 0)
        self.new_word_quiz()

    def _on_filter_change(self):
        """Handle difficulty filter changes."""
        self.new_quiz = True

    # ==================== Quiz Flow ====================

    def new_word_quiz(self):
        """
        Load and display a new quiz question.
        Handles quiz initialization and word selection.
        """
        # Initialize new quiz if needed
        if self.new_quiz or self.word_index >= self.total_questions:
            self._initialize_quiz()

        # Check if there are words to quiz
        if len(self.filtered_words) == 0:
            self._show_no_words_message()
            return

        # Reset state
        self.page.res_label.config(text="")
        self.page.reset_button_colors()
        self.answer_selected = False

        # Get current word
        self.curr_eng_word = self.filtered_words[self.word_index]
        self.curr_ans = self.words_dict[self.curr_eng_word][0]
        difficulty_word = self.words_dict[self.curr_eng_word][1]

        # Update UI
        self.page.update_difficulty_badge(difficulty_word)

        # Generate answer options
        options = self._generate_answer_options()

        # Update progress
        self.word_index += 1
        self.page.update_progress(self.word_index, self.total_questions)

        # Display question
        self.page.show_options(self.curr_eng_word, self.curr_ans, options)

    def next_question(self):
        """Move to next question."""
        if not self.answer_selected:
            # If no answer selected, treat as wrong
            self.wrong_count += 1
            self.page.update_stats(self.correct_count, self.wrong_count)

        self.new_word_quiz()

    def _initialize_quiz(self):
        """Initialize a new quiz session with filtered words."""
        # Filter difficulties
        self.filter_difficulties()

        # Clear result
        self.page.res_label.config(text="")

        # Filter words by difficulty
        self.filtered_words = [
            word for word in self.words_dict.keys()
            if self.words_dict[word][1] in self.difficulties
        ]

        # Shuffle words
        random.shuffle(self.filtered_words)

        # Reset state
        self.new_quiz = False
        self.word_index = 0
        self.total_questions = len(self.filtered_words)

    def _generate_answer_options(self) -> List[str]:
        """
        Generate 4 answer options including the correct answer.

        Returns:
            List of 4 Hebrew words (options)
        """
        # Get three random wrong answers
        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            other_options = random.sample(list(self.all_words_dict.values()), 3)
            other_options_words = [value[0] for value in other_options]
            other_options_words.append(self.curr_ans)

            # Ensure all options are unique
            if len(set(other_options_words)) == 4:
                break

            attempts += 1

        # Shuffle so correct answer isn't always in same position
        random.shuffle(other_options_words)

        return other_options_words

    def _show_no_words_message(self):
        """Show message when no words match filters."""
        self.page.eng_word_label.config(text="No words available")
        self.page.res_label.config(
            text="Adjust your filters or add more words",
            fg="#6c757d"
        )

        for btn in self.page.option_buttons:
            btn.config(text="", state="disabled")

    # ==================== Answer Checking ====================

    def check_answer(self, button_index: int, button):
        """
        Check if selected answer is correct.

        Args:
            button_index: Index of clicked button
            button: The button widget that was clicked
        """
        # Prevent multiple answers
        if self.answer_selected:
            return

        self.answer_selected = True

        # Get selected answer
        selected_ans = button.cget("text")

        # Check if correct
        is_correct = (selected_ans == self.curr_ans)

        # Update statistics
        if is_correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1

        self.page.update_stats(self.correct_count, self.wrong_count)

        # Visual feedback
        self._show_answer_feedback(button_index, is_correct)

        # Show result message
        self.page.show_result(is_correct, self.curr_ans if not is_correct else None)

    def _show_answer_feedback(self, selected_index: int, is_correct: bool):
        """
        Show visual feedback for answer selection.

        Args:
            selected_index: Index of selected button
            is_correct: Whether answer was correct
        """
        # Highlight selected button
        self.page.highlight_answer(selected_index, is_correct)

        # If wrong, also highlight correct answer
        if not is_correct:
            correct_index = self._find_correct_answer_index()
            if correct_index is not None:
                self.page.highlight_answer(correct_index, True)

        # Disable all buttons after answer
        for btn in self.page.option_buttons:
            btn.config(state="disabled")

    def _find_correct_answer_index(self) -> Optional[int]:
        """
        Find the index of the button with the correct answer.

        Returns:
            Index of correct answer button, or None if not found
        """
        for i, btn in enumerate(self.page.option_buttons):
            if btn.cget("text") == self.curr_ans:
                return i
        return None

    # ==================== Difficulty Management ====================

    def filter_difficulties(self):
        """Filter quiz words based on selected difficulty checkboxes."""
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
        """Open dialog to update current word's difficulty."""
        if not self.curr_eng_word:
            return

        # Show difficulty dialog
        dialog = DifficultyDialog(self.page)
        new_difficulty = dialog.result

        if not new_difficulty:
            return

        # Convert to enum
        difficulty_enum = self._convert_difficulty_to_enum(new_difficulty)

        if difficulty_enum:
            try:
                # Update in database
                self.model.update_difficulty(self.curr_eng_word, difficulty_enum)

                # Update local dict
                heb_word = self.words_dict[self.curr_eng_word][0]
                self.words_dict[self.curr_eng_word] = (heb_word, difficulty_enum)
                self.all_words_dict[self.curr_eng_word] = (heb_word, difficulty_enum)

                # Show success message
                self.page.res_label.config(
                    text=f"Difficulty updated to {new_difficulty}!",
                    fg="#28a745"
                )

            except Exception as e:
                print(f"Error updating difficulty: {e}")
                self.page.res_label.config(
                    text="Failed to update difficulty",
                    fg="#dc3545"
                )

    def _convert_difficulty_to_enum(self, difficulty_str: str) -> Optional[str]:
        """
        Convert difficulty string to enum name.

        Args:
            difficulty_str: Difficulty as string ("Easy", "Medium", "Hard")

        Returns:
            Enum name or None
        """
        difficulty_map = {
            "Easy": Difficulty.EASY.name,
            "Medium": Difficulty.MEDIUM.name,
            "Hard": Difficulty.HARD.name
        }

        return difficulty_map.get(difficulty_str)

    # ==================== Group Filtering ====================

    def select_groups(self):
        """Open dialog to select groups for quiz filtering."""
        try:
            # Get all groups
            all_groups_names = self.model.get_all_groups_names()
            groups = [row[0] for row in all_groups_names]

            if not groups:
                self.page.res_label.config(
                    text="No groups available",
                    fg="#6c757d"
                )
                return

            # Open group selection dialog
            dialog = GroupSelectionDialog(self.page, groups)

            # Get selected groups
            selected_groups = getattr(dialog, 'selected_groups', [])

            if selected_groups:
                # Get words from selected groups
                self._filter_by_groups(selected_groups)

        except Exception as e:
            print(f"Error selecting groups: {e}")
            self.page.res_label.config(
                text="Failed to load groups",
                fg="#dc3545"
            )

    def _filter_by_groups(self, selected_groups: List[str]):
        """
        Filter quiz words by selected groups.

        Args:
            selected_groups: List of group names to include
        """
        try:
            # Query words from selected groups
            words_by_groups = self.model.get_words_by_groups(selected_groups)

            # Update words dict
            self.words_dict = {}
            for eng_word, heb_word, difficulty, group_name in words_by_groups:
                self.words_dict[eng_word] = (heb_word, difficulty)

            # Mark for new quiz
            self.new_quiz = True

            # Show confirmation
            group_names = ", ".join(selected_groups[:3])
            if len(selected_groups) > 3:
                group_names += f" +{len(selected_groups) - 3} more"

            self.page.res_label.config(
                text=f"Quiz filtered to: {group_names}",
                fg="#28a745"
            )

        except Exception as e:
            print(f"Error filtering by groups: {e}")
            self.page.res_label.config(
                text="Failed to filter groups",
                fg="#dc3545"
            )

    # ==================== Statistics ====================

    def get_session_stats(self) -> Dict[str, int]:
        """
        Get current session statistics.

        Returns:
            Dictionary with session stats
        """
        total = self.correct_count + self.wrong_count
        accuracy = (self.correct_count / total * 100) if total > 0 else 0

        return {
            "correct": self.correct_count,
            "wrong": self.wrong_count,
            "total": total,
            "accuracy": round(accuracy, 1)
        }

    def reset_stats(self):
        """Reset session statistics."""
        self.correct_count = 0
        self.wrong_count = 0
        self.page.update_stats(0, 0)

    # ==================== Public API ====================

    def initialize(self):
        """Initialize the quiz controller."""
        self.init_words_dict()
        self.start_new_quiz()

    def cleanup(self):
        """Cleanup when controller is destroyed."""
        # Add any cleanup logic here
        pass

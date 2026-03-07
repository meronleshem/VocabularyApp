#
# import random
# import re
# from typing import Dict, Tuple, List, Optional
# from tkinter import messagebox
#
#
# class FillBlankQuizController:
#     def __init__(self, model, view):
#         self.model = model
#         self.view = view
#         self.page = self.view.pages["fill_blank_quiz_page"]
#
#         # Word storage - (eng, heb, difficulty, examples)
#         self.words_with_examples: List[Tuple] = []
#         self.all_words: List[str] = []  # All English words for wrong options
#
#         # Quiz state
#         self.current_word: str = ""
#         self.current_hebrew: str = ""  # Hebrew translation
#         self.current_sentence: str = ""
#         self.current_difficulty: str = ""
#         self.filtered_words: List[Tuple] = []
#         self.word_index: int = 0
#         self.total_questions: int = 0
#         self.new_quiz: bool = True
#         self.answer_selected: bool = False
#         self.difficulties: List[str] = []
#
#         # Statistics
#         self.correct_count: int = 0
#         self.wrong_count: int = 0
#
#         # Quiz configuration
#         self.max_questions: Optional[int] = None
#
#         # Initialize
#         self.init_words()
#         self.bind()
#
#         # Show welcome or start quiz
#         self._show_welcome_message()
#
#         # Auto-show setup on page visible
#         self.page.bind("<Visibility>", self._on_page_visible)
#         self.quiz_configured = False
#
#     def init_words(self):
#         """Load words with examples from database."""
#         try:
#             # Get all word details
#             query = "SELECT engWord, hebWord, difficulty, examples, group_name FROM vocabulary WHERE examples IS NOT NULL AND examples != ''"
#             self.model.cursor.execute(query)
#             results = self.model.cursor.fetchall()
#
#             # Filter words that have examples
#             for eng, heb, diff, examples, group in results:
#                 if examples and examples.strip():
#                     self.words_with_examples.append((eng, heb, diff, examples, group))
#
#             # Get all words for generating wrong options
#             all_data = self.model.cursor.execute("SELECT engWord FROM vocabulary")
#             self.all_words = [row[0] for row in all_data.fetchall()]
#
#             print(f"Loaded {len(self.words_with_examples)} words with examples")
#
#         except Exception as e:
#             print(f"Error loading words: {e}")
#
#     def bind(self):
#         """Bind UI events."""
#         print("Binding Fill-in-Blank quiz events...")  # DEBUG
#
#         self.page.back_btn.config(command=self.go_back)
#         self.page.next_btn.config(command=self.next_question)
#
#         # Answer buttons - bind each one explicitly
#         for i, btn in enumerate(self.page.option_buttons):
#             btn.config(command=lambda idx=i: self._on_button_click(idx))
#             print(f"Bound button {i}")  # DEBUG
#
#         # Control buttons
#         self.page.select_groups_btn.config(command=self.select_groups)
#         self.page.new_quiz_btn.config(command=self.start_new_quiz_with_dialog)
#
#         # Difficulty filters
#         self.page.choice_new.trace('w', lambda *args: self._on_filter_change())
#         self.page.choice_easy.trace('w', lambda *args: self._on_filter_change())
#         self.page.choice_medium.trace('w', lambda *args: self._on_filter_change())
#         self.page.choice_hard.trace('w', lambda *args: self._on_filter_change())
#
#     def _on_button_click(self, button_index):
#         """Handle button click."""
#         print(f"Button {button_index} clicked!")  # DEBUG
#         btn = self.page.option_buttons[button_index]
#         self.check_answer(button_index, btn)
#
#     def _on_page_visible(self, event):
#         """Show setup dialog when page becomes visible."""
#         if not self.quiz_configured:
#             self.page.after(100, self._show_initial_setup)
#
#     def _show_initial_setup(self):
#         """Show setup dialog."""
#         if not self.quiz_configured:
#             self.show_setup_dialog()
#
#     def _show_welcome_message(self):
#         """Show welcome message."""
#         self.page.sentence_label.config(text="Welcome to Fill-in-the-Blank Quiz!")
#         self.page.res_label.config(text="Complete sentences by selecting the correct word", fg="#666")
#         self.page.next_btn.config(state="disabled")
#         for btn in self.page.option_buttons:
#             btn.config(text="", state="disabled")
#
#     def _on_filter_change(self):
#         """Handle filter changes."""
#         if self.quiz_configured:
#             self.new_quiz = True
#
#     # ==================== Quiz Setup ====================
#
#     def show_setup_dialog(self):
#         """Show quiz setup dialog."""
#         try:
#             from View.QuizSetupDialog import QuizSetupDialog
#
#             # Get available groups
#             groups_data = self.model.get_all_groups_names()
#             groups = [row[0] for row in groups_data] if groups_data else []
#
#             # Show dialog
#             dialog = QuizSetupDialog(self.view, groups)
#
#             if dialog.result:
#                 self.quiz_configured = True
#                 config = dialog.result
#
#                 # Apply settings
#                 self._apply_difficulty_filters(config['difficulties'])
#
#                 if config['groups']:
#                     self._filter_by_groups(config['groups'])
#
#                 self.max_questions = config['question_count']
#
#                 # Start quiz
#                 self.start_quiz()
#                 return True
#             else:
#                 # Cancelled - go back
#                 self.go_back()
#                 return False
#
#         except Exception as e:
#             print(f"Error in setup dialog: {e}")
#             messagebox.showerror("Error", f"Failed to start quiz: {e}")
#             self.go_back()
#             return False
#
#     def _apply_difficulty_filters(self, difficulties: List[str]):
#         """Apply difficulty filters."""
#         self.page.choice_new.set(1 if "NEW_WORD" in difficulties else 0)
#         self.page.choice_easy.set(1 if "EASY" in difficulties else 0)
#         self.page.choice_medium.set(1 if "MEDIUM" in difficulties else 0)
#         self.page.choice_hard.set(1 if "HARD" in difficulties else 0)
#
#     def start_quiz(self):
#         """Start quiz."""
#         self.new_quiz = True
#         self.correct_count = 0
#         self.wrong_count = 0
#         self.mistakes = []
#         self.page.update_stats(0, 0)
#         self.new_question()
#
#     def start_new_quiz_with_dialog(self):
#         """Start new quiz with setup dialog."""
#         self.quiz_configured = False
#         self.show_setup_dialog()
#
#     # ==================== Navigation ====================
#
#     def go_back(self):
#         """Go back to home page."""
#         self.quiz_configured = False
#         self.view.show_page(self.view.pages["add_word_page"])
#
#     # ==================== Quiz Flow ====================
#
#     def new_question(self):
#         """Load and display new question."""
#         # Initialize if needed
#         if self.new_quiz or self.word_index >= self.total_questions:
#             self._initialize_quiz()
#
#         # Check if words available
#         if not self.filtered_words:
#             self._show_no_words()
#             return
#
#         # Reset state
#         self.page.res_label.config(text="")
#         self.page.reset_button_colors()
#         self.answer_selected = False
#         self.page.disable_next_button()
#
#         # Get word and example
#         word_data = self.filtered_words[self.word_index]
#         self.current_word = word_data[0]
#         self.current_hebrew = word_data[1]  # Store Hebrew translation
#         self.current_difficulty = word_data[2]
#         examples = word_data[3]
#
#         # Extract first sentence from examples
#         self.current_sentence = self._extract_sentence(examples, self.current_word)
#
#         if not self.current_sentence:
#             # No valid sentence, skip to next
#             self.word_index += 1
#             if self.word_index < self.total_questions:
#                 self.new_question()
#             else:
#                 self._show_quiz_complete()
#             return
#
#         # Create sentence with blank
#         blank_sentence = self.current_sentence.replace(self.current_word, "_____")
#         #blank_sentence = blank_sentence.replace(self.current_word.capitalize(), "_____")
#         #blank_sentence = blank_sentence.replace(self.current_word.upper(), "_____")
#
#         # Generate options
#         options = self._generate_options()
#
#         # Update UI
#         self.page.update_difficulty_badge(self.current_difficulty)
#         self.page.show_sentence(blank_sentence)
#         self.page.show_options(options)
#
#         # Update progress
#         self.word_index += 1
#         self.page.update_progress(self.word_index, self.total_questions)
#
#     def next_question(self):
#         """Move to next question."""
#         if not self.answer_selected:
#             self.wrong_count += 1
#             self.page.update_stats(self.correct_count, self.wrong_count)
#
#         # Check if quiz complete
#         if self.word_index >= self.total_questions:
#             self._show_quiz_complete()
#         else:
#             self.new_question()
#
#     def _initialize_quiz(self):
#         """Initialize quiz with filtered words."""
#         self.filter_difficulties()
#         self.page.res_label.config(text="")
#
#         # Filter words by difficulty
#         self.filtered_words = [
#             word for word in self.words_with_examples
#             if word[2] in self.difficulties
#         ]
#
#         # Apply question limit
#         if self.max_questions and len(self.filtered_words) > self.max_questions:
#             random.shuffle(self.filtered_words)
#             self.filtered_words = self.filtered_words[:self.max_questions]
#         else:
#             random.shuffle(self.filtered_words)
#
#         self.new_quiz = False
#         self.word_index = 0
#         self.total_questions = len(self.filtered_words)
#
#     def _extract_sentence(self, examples: str, word: str) -> str:
#         """Extract a sentence containing the word from examples."""
#         if not examples:
#             return ""
#
#         # Split into sentences
#         sentences = re.split(r'[\n]+', examples)
#         matches = []
#
#         for sentence in sentences:
#             sentence = sentence.strip()
#             if len(sentence) < 10:  # Too short
#                 continue
#
#             # Check if word appears (case-insensitive)
#             if re.search(r'\b' + re.escape(word) + r'\b', sentence, re.IGNORECASE):
#                 matches.append(sentence)
#
#         # Return random match if any found
#         if matches:
#             return random.choice(matches)
#         else:
#             return ""
#
#     def _generate_options(self) -> List[str]:
#         """Generate 4 options including correct answer."""
#         options = [self.current_word]
#
#         # Get 3 random wrong words
#         attempts = 0
#         while len(options) < 4 and attempts < 20:
#             wrong_word = random.choice(self.all_words)
#             if wrong_word not in options and wrong_word != self.current_word:
#                 options.append(wrong_word)
#             attempts += 1
#
#         # Fill remaining if needed
#         while len(options) < 4:
#             options.append(f"word{len(options)}")
#
#         # Shuffle
#         random.shuffle(options)
#
#         return options
#
#     def _show_no_words(self):
#         """Show no words message."""
#         self.page.sentence_label.config(text="No words with examples available")
#         self.page.res_label.config(text="Adjust filters or add words with examples", fg="#666")
#         for btn in self.page.option_buttons:
#             btn.config(text="", state="disabled")
#         self.page.next_btn.config(state="disabled")
#
#     def _show_quiz_complete(self):
#         """Show quiz complete dialog."""
#         try:
#             from View.QuizResultsDialog import QuizResultsDialog
#
#             dialog = QuizResultsDialog(
#                 self.page,
#                 self.correct_count,
#                 self.wrong_count,
#                 self.mistakes if hasattr(self, 'mistakes') else []
#             )
#
#             if dialog.action == "new_quiz":
#                 self.start_new_quiz_with_dialog()
#
#         except Exception as e:
#             print(f"Error showing results: {e}")
#
#     # ==================== Answer Checking ====================
#
#     def check_answer(self, button_index: int, button):
#         """Check if answer is correct."""
#         if self.answer_selected:
#             return
#
#         print(f"Checking answer: button {button_index}")  # DEBUG
#
#         self.answer_selected = True
#         selected = button.cget("text")
#         is_correct = (selected.lower() == self.current_word.lower())
#
#         print(f"Selected: {selected}, Correct: {self.current_word}, Is Correct: {is_correct}")  # DEBUG
#
#         # Update stats
#         if is_correct:
#             self.correct_count += 1
#         else:
#             self.wrong_count += 1
#             # Track mistake
#             if not hasattr(self, 'mistakes'):
#                 self.mistakes = []
#             self.mistakes.append((self.current_word, selected, self.current_word))
#
#         self.page.update_stats(self.correct_count, self.wrong_count)
#
#         # Visual feedback - highlight the clicked button
#         self.page.highlight_answer(button_index, is_correct)
#
#         # If wrong, also highlight correct answer
#         if not is_correct:
#             for i, btn in enumerate(self.page.option_buttons):
#                 if btn.cget("text").lower() == self.current_word.lower():
#                     self.page.highlight_answer(i, True)
#                     break
#
#         # Disable remaining buttons (ones not highlighted)
#         for i, btn in enumerate(self.page.option_buttons):
#             # Only disable if not already handled by highlight_answer
#             if i != button_index:
#                 # Check if this is the correct answer (if wrong was selected)
#                 if not is_correct and btn.cget("text").lower() == self.current_word.lower():
#                     continue  # Already highlighted
#                 else:
#                     btn.config(state="disabled")
#
#         # Show result
#         self.page.show_result(
#             is_correct,
#             self.current_word if not is_correct else None,
#             self.current_hebrew  # Pass Hebrew translation
#         )
#
#         print("Answer checked and result shown")  # DEBUG
#
#     # ==================== Difficulty ====================
#
#     def filter_difficulties(self):
#         """Apply difficulty filters."""
#         self.difficulties.clear()
#
#         if self.page.choice_new.get() == 1:
#             self.difficulties.append("NEW_WORD")
#         if self.page.choice_easy.get() == 1:
#             self.difficulties.append("EASY")
#         if self.page.choice_medium.get() == 1:
#             self.difficulties.append("MEDIUM")
#         if self.page.choice_hard.get() == 1:
#             self.difficulties.append("HARD")
#
#     # ==================== Group Filtering ====================
#
#     def select_groups(self):
#         """Select groups for filtering."""
#         try:
#             from View.QuizPage import GroupSelectionDialog
#
#             groups_data = self.model.get_all_groups_names()
#             groups = [row[0] for row in groups_data]
#
#             if not groups:
#                 self.page.res_label.config(text="No groups available", fg="#666")
#                 return
#
#             dialog = GroupSelectionDialog(self.page, groups)
#             selected = getattr(dialog, 'selected_groups', [])
#
#             if selected:
#                 self._filter_by_groups(selected)
#                 if not self.quiz_configured:
#                     self.start_quiz()
#
#         except Exception as e:
#             print(f"Error: {e}")
#             self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")
#
#     def _filter_by_groups(self, selected_groups: List[str]):
#         """Filter words by groups."""
#         try:
#             # Filter words_with_examples by groups
#             self.words_with_examples = [
#                 word for word in self.words_with_examples
#                 if word[4] in selected_groups  # group is index 4
#             ]
#
#             self.new_quiz = True
#
#             group_names = ", ".join(selected_groups[:3])
#             if len(selected_groups) > 3:
#                 group_names += f" +{len(selected_groups) - 3} more"
#
#             self.page.res_label.config(text=f"Filtered to: {group_names}", fg="#28a745")
#
#         except Exception as e:
#             print(f"Error: {e}")
#             self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")


import random
import re
from typing import Dict, Tuple, List, Optional
from tkinter import messagebox


# ==================== Improved Word Matcher ====================

class WordMatcher:
    """
    Fuzzy word matching for finding examples with word variations.

    Handles:
    - Regular suffixes (jump → jumping, jumped, jumps)
    - Double consonants (run → running, stop → stopping)
    - Y to IES (baby → babies)
    - E-dropping (make → making)
    """

    @staticmethod
    def get_possible_forms(word: str) -> List[str]:
        """Generate all possible forms of a word."""
        word = word.lower()
        forms = [word]  # Base form

        # 1. Y → IES for plurals (baby → babies)
        if word.endswith('y') and len(word) > 2:
            forms.append(word[:-1] + 'ies')

        # 2. Double consonant before ING/ED (run → running)
        if len(word) >= 3:
            last = word[-1]
            second_last = word[-2]

            if (last in 'bcdfghjklmnpqrstvwxyz' and
                    second_last in 'aeiou'):
                forms.extend([
                    word + last + 'ing',  # running
                    word + last + 'ed',  # stopped
                    word + last + 'er',  # runner
                ])

        # 3. E-dropping (make → making)
        if word.endswith('e') and len(word) > 2:
            stem = word[:-1]
            forms.append(stem + 'ing')

        # 4. Regular forms
        forms.extend([
            word + 's', word + 'es', word + 'ing', word + 'ed',
            word + 'd', word + 'er', word + 'est', word + 'ly', word + 'en'
        ])

        return list(set(forms))

    @staticmethod
    def create_pattern(word: str, fuzzy: bool = True) -> str:
        """Create regex pattern matching all word forms."""
        if not fuzzy:
            return r'\b' + re.escape(word) + r'\b'

        forms = WordMatcher.get_possible_forms(word)
        forms.sort(key=len, reverse=True)  # Longest first
        escaped = [re.escape(f) for f in forms]
        return r'\b(?:' + '|'.join(escaped) + r')\b'

    @staticmethod
    def word_matches(word: str, text: str, fuzzy: bool = True) -> bool:
        """Check if word (or any form) appears in text."""
        pattern = WordMatcher.create_pattern(word, fuzzy=fuzzy)
        return bool(re.search(pattern, text, re.IGNORECASE))


# ==================== Fill Blank Quiz Controller ====================

class FillBlankQuizController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["fill_blank_quiz_page"]

        # Word storage - (eng, heb, difficulty, examples)
        self.words_with_examples: List[Tuple] = []
        self.all_words: List[str] = []  # All English words for wrong options

        # Quiz state
        self.current_word: str = ""
        self.current_hebrew: str = ""  # Hebrew translation
        self.current_sentence: str = ""
        self.current_difficulty: str = ""
        self.filtered_words: List[Tuple] = []
        self.word_index: int = 0
        self.total_questions: int = 0
        self.new_quiz: bool = True
        self.answer_selected: bool = False
        self.difficulties: List[str] = []

        # Statistics
        self.correct_count: int = 0
        self.wrong_count: int = 0

        # Quiz configuration
        self.max_questions: Optional[int] = None

        # Initialize
        self.init_words()
        self.bind()

        # Show welcome or start quiz
        self._show_welcome_message()

        # Auto-show setup on page visible
        self.page.bind("<Visibility>", self._on_page_visible)
        self.quiz_configured = False

    def init_words(self):
        """Load words with examples from database."""
        try:
            # Get all word details
            query = "SELECT engWord, hebWord, difficulty, examples, group_name FROM vocabulary WHERE examples IS NOT NULL AND examples != ''"
            self.model.cursor.execute(query)
            results = self.model.cursor.fetchall()

            # Filter words that have examples
            for eng, heb, diff, examples, group in results:
                if examples and examples.strip():
                    self.words_with_examples.append((eng, heb, diff, examples, group))

            # Get all words for generating wrong options
            all_data = self.model.cursor.execute("SELECT engWord FROM vocabulary")
            self.all_words = [row[0] for row in all_data.fetchall()]

            print(f"Loaded {len(self.words_with_examples)} words with examples")

        except Exception as e:
            print(f"Error loading words: {e}")

    def bind(self):
        """Bind UI events."""
        print("Binding Fill-in-Blank quiz events...")  # DEBUG

        self.page.back_btn.config(command=self.go_back)
        self.page.next_btn.config(command=self.next_question)

        # Answer buttons - bind each one explicitly
        for i, btn in enumerate(self.page.option_buttons):
            btn.config(command=lambda idx=i: self._on_button_click(idx))
            print(f"Bound button {i}")  # DEBUG

        # Control buttons
        self.page.select_groups_btn.config(command=self.select_groups)
        self.page.new_quiz_btn.config(command=self.start_new_quiz_with_dialog)

        # Difficulty filters
        self.page.choice_new.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_easy.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_medium.trace('w', lambda *args: self._on_filter_change())
        self.page.choice_hard.trace('w', lambda *args: self._on_filter_change())

    def _on_button_click(self, button_index):
        """Handle button click."""
        print(f"Button {button_index} clicked!")  # DEBUG
        btn = self.page.option_buttons[button_index]
        self.check_answer(button_index, btn)

    def _on_page_visible(self, event):
        """Show setup dialog when page becomes visible."""
        if not self.quiz_configured:
            self.page.after(100, self._show_initial_setup)

    def _show_initial_setup(self):
        """Show setup dialog."""
        if not self.quiz_configured:
            self.show_setup_dialog()

    def _show_welcome_message(self):
        """Show welcome message."""
        self.page.sentence_label.config(text="Welcome to Fill-in-the-Blank Quiz!")
        self.page.res_label.config(text="Complete sentences by selecting the correct word", fg="#666")
        self.page.next_btn.config(state="disabled")
        for btn in self.page.option_buttons:
            btn.config(text="", state="disabled")

    def _on_filter_change(self):
        """Handle filter changes."""
        if self.quiz_configured:
            self.new_quiz = True

    # ==================== Quiz Setup ====================

    def show_setup_dialog(self):
        """Show quiz setup dialog."""
        try:
            from View.QuizSetupDialog import QuizSetupDialog

            # Get available groups
            groups_data = self.model.get_all_groups_names()
            groups = [row[0] for row in groups_data] if groups_data else []

            # Show dialog
            dialog = QuizSetupDialog(self.view, groups, self.model)

            if dialog.result:
                self.quiz_configured = True
                config = dialog.result

                # Apply settings
                self._apply_difficulty_filters(config['difficulties'])

                if config['groups']:
                    self._filter_by_groups(config['groups'])

                self.max_questions = config['question_count']

                # Start quiz
                self.start_quiz()
                return True
            else:
                # Cancelled - go back
                self.go_back()
                return False

        except Exception as e:
            print(f"Error in setup dialog: {e}")
            messagebox.showerror("Error", f"Failed to start quiz: {e}")
            self.go_back()
            return False

    def _apply_difficulty_filters(self, difficulties: List[str]):
        """Apply difficulty filters."""
        self.page.choice_new.set(1 if "NEW_WORD" in difficulties else 0)
        self.page.choice_easy.set(1 if "EASY" in difficulties else 0)
        self.page.choice_medium.set(1 if "MEDIUM" in difficulties else 0)
        self.page.choice_hard.set(1 if "HARD" in difficulties else 0)

    def start_quiz(self):
        """Start quiz."""
        self.new_quiz = True
        self.correct_count = 0
        self.wrong_count = 0
        self.mistakes = []
        self.page.update_stats(0, 0)
        self.new_question()

    def start_new_quiz_with_dialog(self):
        """Start new quiz with setup dialog."""
        self.quiz_configured = False
        self.show_setup_dialog()

    # ==================== Navigation ====================

    def go_back(self):
        """Go back to home page."""
        self.quiz_configured = False
        self.view.show_page(self.view.pages["add_word_page"])

    # ==================== Quiz Flow ====================

    def new_question(self):
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
        self.page.disable_next_button()

        # Get word and example
        word_data = self.filtered_words[self.word_index]
        self.current_word = word_data[0]
        self.current_hebrew = word_data[1]  # Store Hebrew translation
        self.current_difficulty = word_data[2]
        examples = word_data[3]

        # Extract first sentence from examples (WITH FUZZY MATCHING)
        self.current_sentence = self._extract_sentence(examples, self.current_word)

        if not self.current_sentence:
            # No valid sentence, skip to next
            self.word_index += 1
            if self.word_index < self.total_questions:
                self.new_question()
            else:
                self._show_quiz_complete()
            return

        # Replace word with blank
        blank_sentence = self._create_blank_sentence(self.current_sentence, self.current_word)

        # Generate options
        options = self._generate_options()

        # Display
        self.page.show_sentence(blank_sentence)
        self.page.show_options(options)
        self.page.update_progress(self.word_index + 1, self.total_questions)
        self.page.update_difficulty_badge(self.current_difficulty)

    def next_question(self):
        """Move to next question."""
        self.word_index += 1

        # Update stats
        if self.answer_selected:
            # Stats already updated in check_answer
            pass
        else:
            # No answer selected, count as wrong
            self.wrong_count += 1
            self.page.update_stats(self.correct_count, self.wrong_count)

        # Check if quiz complete
        if self.word_index >= self.total_questions:
            self._show_quiz_complete()
        else:
            self.new_question()

    def _initialize_quiz(self):
        """Initialize quiz with filtered words."""
        self.filter_difficulties()
        self.page.res_label.config(text="")

        # Filter words by difficulty
        self.filtered_words = [
            word for word in self.words_with_examples
            if word[2] in self.difficulties
        ]

        # Apply question limit
        if self.max_questions and len(self.filtered_words) > self.max_questions:
            random.shuffle(self.filtered_words)
            self.filtered_words = self.filtered_words[:self.max_questions]
        else:
            random.shuffle(self.filtered_words)

        self.new_quiz = False
        self.word_index = 0
        self.total_questions = len(self.filtered_words)

    def _extract_sentence(self, examples: str, word: str) -> str:
        """
        Extract a sentence containing the word (or its variations) from examples.

        🌟 WITH FUZZY MATCHING! 🌟

        Matches:
        - jump → jumping, jumped, jumps
        - corridor → corridors
        - baby → babies
        - run → running, runner
        """
        if not examples:
            return ""

        # Split into sentences
        sentences = re.split(r'[\n]+', examples)
        matches = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Too short
                continue

            # 🌟 FUZZY MATCHING - matches word variations! 🌟
            if WordMatcher.word_matches(word, sentence, fuzzy=True):
                matches.append(sentence)

        # Return random match if any found
        if matches:
            return random.choice(matches)
        else:
            return ""

    def _create_blank_sentence(self, sentence: str, word: str) -> str:
        """
        Replace the word (or its variation) with a blank.

        🌟 WITH FUZZY MATCHING! 🌟

        Examples:
        - "He is jumping" → "He is _____" (word is "jump")
        - "The corridors" → "The _____" (word is "corridor")
        - "The babies" → "The _____" (word is "baby")
        """
        # Find the actual word in the sentence using fuzzy matching
        pattern = WordMatcher.create_pattern(word, fuzzy=True)
        match = re.search(pattern, sentence, re.IGNORECASE)

        if match:
            # Replace with blank
            blank_sentence = sentence[:match.start()] + "_____" + sentence[match.end():]
            return blank_sentence
        else:
            # Fallback: shouldn't happen
            return sentence.replace(word, "_____")

    def _generate_options(self) -> List[str]:
        """Generate 4 options including correct answer."""
        options = [self.current_word]

        # Get 3 random wrong words
        attempts = 0
        while len(options) < 4 and attempts < 20:
            wrong_word = random.choice(self.all_words)
            if wrong_word not in options and wrong_word != self.current_word:
                options.append(wrong_word)
            attempts += 1

        # Fill remaining if needed
        while len(options) < 4:
            options.append(f"word{len(options)}")

        # Shuffle
        random.shuffle(options)

        return options

    def _show_no_words(self):
        """Show no words message."""
        self.page.sentence_label.config(text="No words with examples available")
        self.page.res_label.config(text="Adjust filters or add words with examples", fg="#666")
        for btn in self.page.option_buttons:
            btn.config(text="", state="disabled")
        self.page.next_btn.config(state="disabled")

    def _show_quiz_complete(self):
        """Show quiz complete dialog."""
        try:
            from View.QuizResultsDialog import QuizResultsDialog

            dialog = QuizResultsDialog(
                self.page,
                self.correct_count,
                self.wrong_count,
                self.mistakes if hasattr(self, 'mistakes') else []
            )

            if dialog.action == "new_quiz":
                self.start_new_quiz_with_dialog()

        except Exception as e:
            print(f"Error showing results: {e}")

    # ==================== Answer Checking ====================

    def check_answer(self, button_index: int, button):
        """Check if answer is correct."""
        if self.answer_selected:
            return

        print(f"Checking answer: button {button_index}")  # DEBUG

        self.answer_selected = True
        selected = button.cget("text")
        is_correct = (selected.lower() == self.current_word.lower())

        print(f"Selected: {selected}, Correct: {self.current_word}, Is Correct: {is_correct}")  # DEBUG

        # Update stats
        if is_correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1
            # Track mistake
            if not hasattr(self, 'mistakes'):
                self.mistakes = []
            self.mistakes.append((self.current_word, selected, self.current_word))

        self.page.update_stats(self.correct_count, self.wrong_count)

        # Visual feedback - highlight the clicked button
        self.page.highlight_answer(button_index, is_correct)

        # If wrong, also highlight correct answer
        if not is_correct:
            for i, btn in enumerate(self.page.option_buttons):
                if btn.cget("text").lower() == self.current_word.lower():
                    self.page.highlight_answer(i, True)
                    break

        # Disable remaining buttons (ones not highlighted)
        for i, btn in enumerate(self.page.option_buttons):
            # Only disable if not already handled by highlight_answer
            if i != button_index:
                # Check if this is the correct answer (if wrong was selected)
                if not is_correct and btn.cget("text").lower() == self.current_word.lower():
                    continue  # Already highlighted
                else:
                    btn.config(state="disabled")

        # Show result
        self.page.show_result(
            is_correct,
            self.current_word if not is_correct else None,
            self.current_hebrew  # Pass Hebrew translation
        )

        print("Answer checked and result shown")  # DEBUG

    # ==================== Difficulty ====================

    def filter_difficulties(self):
        """Apply difficulty filters."""
        self.difficulties.clear()

        if self.page.choice_new.get() == 1:
            self.difficulties.append("NEW_WORD")
        if self.page.choice_easy.get() == 1:
            self.difficulties.append("EASY")
        if self.page.choice_medium.get() == 1:
            self.difficulties.append("MEDIUM")
        if self.page.choice_hard.get() == 1:
            self.difficulties.append("HARD")

    # ==================== Group Filtering ====================

    def select_groups(self):
        """Select groups for filtering."""
        try:
            from View.QuizPage import GroupSelectionDialog

            groups_data = self.model.get_all_groups_names()
            groups = [row[0] for row in groups_data]

            if not groups:
                self.page.res_label.config(text="No groups available", fg="#666")
                return

            dialog = GroupSelectionDialog(self.page, groups)
            selected = getattr(dialog, 'selected_groups', [])

            if selected:
                self._filter_by_groups(selected)
                if not self.quiz_configured:
                    self.start_quiz()

        except Exception as e:
            print(f"Error: {e}")
            self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")

    def _filter_by_groups(self, selected_groups: List[str]):
        """Filter words by groups."""
        try:
            # Filter words_with_examples by groups
            self.words_with_examples = [
                word for word in self.words_with_examples
                if word[4] in selected_groups  # group is index 4
            ]

            self.new_quiz = True

            group_names = ", ".join(selected_groups[:3])
            if len(selected_groups) > 3:
                group_names += f" +{len(selected_groups) - 3} more"

            self.page.res_label.config(text=f"Filtered to: {group_names}", fg="#28a745")

        except Exception as e:
            print(f"Error: {e}")
            self.page.res_label.config(text="Failed to filter groups", fg="#dc3545")

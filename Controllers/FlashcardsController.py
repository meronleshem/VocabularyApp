
import random
from typing import List, Tuple, Optional
from tkinter import messagebox


class FlashcardsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["flashcards_page"]
        
        # Session data
        self.words: List[Tuple] = []  # (english, hebrew, difficulty, group)
        self.current_index: int = 0
        self.total_words: int = 0
        
        # Statistics
        self.know_count: int = 0
        self.guess_count: int = 0
        self.dont_know_count: int = 0
        
        # Session tracking
        self.session_started = False
        
        # Bind events
        self.bind()
        
        # Auto-start session when page becomes visible
        self.page.bind("<Visibility>", self._on_page_visible)

    
    def bind(self):
        self.page.back_btn.config(command=self.go_back)
        
        # Override rating button commands
        self.page.dont_know_btn.config(command=lambda: self.rate_word("dont_know"))
        self.page.guess_btn.config(command=lambda: self.rate_word("guess"))
        self.page.know_btn.config(command=lambda: self.rate_word("know"))

        self.page.bind("<Left>", lambda e: self.rate_word("dont_know"))
        self.page.bind("<Right>", lambda e: self.rate_word("dont_know"))

    # ==================== Session Management ====================
    
    def start_session(self, words: Optional[List[Tuple]] = None):
        """
        Start a new flashcard session.
        
        Args:
            words: Optional list of words to study.
                   If None, loads all words from database.
        """
        # Load words
        if words is None:
            words = self.model.get_full_data()
        
        if not words:
            self.page.show_welcome_message()
            messagebox.showinfo(
                "No Words",
                "No words available for flashcards.\nPlease add some words first!",
                parent=self.page
            )
            return
        
        # Shuffle for randomness
        self.words = list(words)
        random.shuffle(self.words)
        
        # Reset session state
        self.current_index = 0
        self.total_words = len(self.words)
        self.know_count = 0
        self.guess_count = 0
        self.dont_know_count = 0
        
        # Update UI
        self.page.enable_buttons()
        self.page.update_stats(0, 0, 0)
        
        # Show first card
        self.show_current_card()
    
    def show_current_card(self):
        """Display the current word card."""
        if self.current_index >= self.total_words:
            self.end_session()
            return
        
        # Get current word
        word_data = self.words[self.current_index]
        english = word_data[0]
        hebrew = word_data[1]
        difficulty = word_data[2] if len(word_data) > 2 else "NEW_WORD"
        
        # Display card
        self.page.show_word(english, hebrew, difficulty)
        self.page.update_progress(self.current_index + 1, self.total_words)
    
    def next_card(self):
        """Move to the next card."""
        self.current_index += 1
        
        if self.current_index >= self.total_words:
            self.end_session()
        else:
            self.show_current_card()
    
    def end_session(self):
        """End the flashcard session and show results."""
        self.page.disable_buttons()
        
        # Calculate accuracy
        total_rated = self.know_count + self.guess_count + self.dont_know_count
        
        if total_rated > 0:
            accuracy = (self.know_count / total_rated) * 100
        else:
            accuracy = 0
        
        # Show completion message
        message = (
            f"Session Complete! 🎉\n\n"
            f"Cards reviewed: {total_rated}\n"
            f"Know: {self.know_count}\n"
            f"Guess: {self.guess_count}\n"
            f"Don't Know: {self.dont_know_count}\n\n"
            f"Accuracy: {accuracy:.0f}%"
        )
        
        result = messagebox.askyesno(
            "Session Complete",
            message + "\n\nStart another session?",
            parent=self.page
        )
        
        if result:
            self.start_session()
        else:
            self.go_back()
    
    # ==================== Rating & Difficulty ====================
    
    def rate_word(self, rating: str):
        """
        Rate the current word and update its difficulty.
        
        Args:
            rating: 'know', 'guess', or 'dont_know'
        """
        if self.current_index >= self.total_words:
            return
        
        # Get current word
        word_data = self.words[self.current_index]
        english = word_data[0]
        
        # Map rating to difficulty
        difficulty_map = {
            "know": "EASY",
            "guess": "MEDIUM",
            "dont_know": "HARD"
        }
        
        new_difficulty = difficulty_map.get(rating, "MEDIUM")
        
        # Update difficulty in database
        try:
            self.model.update_difficulty(english, new_difficulty)
        except Exception as e:
            print(f"Error updating difficulty: {e}")
        
        # Update statistics
        if rating == "know":
            self.know_count += 1
        elif rating == "guess":
            self.guess_count += 1
        elif rating == "dont_know":
            self.dont_know_count += 1
        
        self.page.update_stats(self.know_count, self.guess_count, self.dont_know_count)
        
        # Move to next card
        self.next_card()
    
    # ==================== Navigation ====================
    
    def go_back(self):
        """Return to home page."""
        # Ask for confirmation if session is active
        if self.current_index > 0 and self.current_index < self.total_words:
            result = messagebox.askyesno(
                "Exit Session",
                "You have an active flashcard session.\nAre you sure you want to exit?",
                parent=self.page
            )
            if not result:
                return
        
        self.view.show_page(self.view.pages["add_word_page"])
    
    # ==================== Advanced Features ====================
    
    def start_filtered_session(self, difficulties: List[str] = None, 
                               groups: List[str] = None,
                               max_cards: Optional[int] = None):
        """
        Start a session with filtered words.
        
        Args:
            difficulties: List of difficulty levels to include
            groups: List of groups to include
            max_cards: Maximum number of cards (None = all)
        """
        # Get all words
        all_words = list(self.model.get_full_data())
        
        # Filter by difficulty
        if difficulties:
            all_words = [
                word for word in all_words
                if len(word) > 2 and word[2] in difficulties
            ]
        
        # Filter by groups
        if groups:
            all_words = [
                word for word in all_words
                if len(word) > 3 and word[3] in groups
            ]
        
        # Limit number of cards
        if max_cards and len(all_words) > max_cards:
            random.shuffle(all_words)
            all_words = all_words[:max_cards]
        
        # Start session with filtered words
        self.start_session(all_words)
    
    def _on_page_visible(self, event):
        """Start session when page becomes visible."""
        if not self.session_started:
            self.page.after(100, self._auto_start)

        self.page.focus_set()

    def _auto_start(self):
        """Auto-start a flashcard session."""
        if not self.session_started:
            self.session_started = True
            self.start_session()
        
        # Reset flag when leaving page
        self.page.bind("<Unmap>", lambda e: setattr(self, "session_started", False))

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


class FlashcardsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#e8eaf6")
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Card state
        self.is_flipped = False
        
        # Create UI
        self._create_header()
        self._create_card_area()
        self._create_controls()
        
    def _create_header(self):
        """Create header with title and progress."""
        header = tk.Frame(self, bg="#5e35b1", height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.columnconfigure(1, weight=1)
        
        # Back button
        self.back_btn = tb.Button(header, text="← Back",
                                  bootstyle="light-outline", width=10)
        self.back_btn.grid(row=0, column=0, padx=20, pady=15)
        
        # Title
        tk.Label(header, text="🎴 Flashcards",
                 font=("Segoe UI", 16, "bold"),
                 bg="#5e35b1", fg="#ffffff").grid(row=0, column=1, sticky="w", padx=20)
        
        # Progress
        self.progress_label = tk.Label(header, text="Card 0 / 0",
                                       font=("Segoe UI", 11),
                                       bg="#5e35b1", fg="#e8eaf6")
        self.progress_label.grid(row=0, column=2, padx=20)
        
        # Stats
        self.stats_label = tk.Label(header, text="✓ 0  ~ 0  ✗ 0",
                                    font=("Segoe UI", 10),
                                    bg="#5e35b1", fg="#e8eaf6")
        self.stats_label.grid(row=0, column=3, padx=(0, 20))
    
    def _create_card_area(self):
        """Create the card display area."""
        card_container = tk.Frame(self, bg="#e8eaf6")
        card_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        card_container.columnconfigure(0, weight=1)
        card_container.rowconfigure(0, weight=1)
        
        # Card frame (clickable)
        self.card_frame = tk.Frame(card_container, bg="#ffffff",
                                   relief="raised", borderwidth=3,
                                   cursor="hand2")
        self.card_frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=50)
        self.card_frame.columnconfigure(0, weight=1)
        self.card_frame.rowconfigure(0, weight=1)
        
        # Card content container
        card_content = tk.Frame(self.card_frame, bg="#ffffff")
        card_content.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        card_content.columnconfigure(0, weight=1)
        card_content.rowconfigure(1, weight=1)
        
        # Instruction label (top)
        self.instruction_label = tk.Label(
            card_content,
            text="Click card to reveal translation",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#999"
        )
        self.instruction_label.grid(row=0, column=0, pady=(0, 15))
        
        # Word label (center - large)
        self.word_label = tk.Label(
            card_content,
            text="Word",
            font=("Segoe UI", 24, "bold"),
            bg="#ffffff",
            fg="#283593",
            wraplength=500,
            justify="center"
        )
        self.word_label.grid(row=1, column=0, sticky="nsew")
        
        # Difficulty badge (bottom)
        self.difficulty_badge = tk.Label(
            card_content,
            text="NEW",
            font=("Segoe UI", 9, "bold"),
            bg="#757575",
            fg="#ffffff",
            padx=12,
            pady=4
        )
        self.difficulty_badge.grid(row=2, column=0, pady=(20, 0))
        
        # Bind click events to flip card
        self.card_frame.bind("<Button-1>", lambda e: self.flip_card())
        self.word_label.bind("<Button-1>", lambda e: self.flip_card())

    def _create_controls(self):
        """Create control buttons."""
        control = tk.Frame(self, bg="#ffffff", height=120)
        control.grid(row=2, column=0, sticky="ew")
        control.grid_propagate(False)
        
        # Buttons container
        buttons = tk.Frame(control, bg="#ffffff")
        buttons.pack(expand=True)
        
        # Don't Know button (Red/Hard)
        self.dont_know_btn = tb.Button(
            buttons,
            text="✗ Don't Know\n(Hard)",
            bootstyle="danger",
            width=18,
            command=lambda: self._on_rating_click("dont_know")
        )
        self.dont_know_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Guess button (Orange/Medium)
        self.guess_btn = tb.Button(
            buttons,
            text="~ Guess\n(Medium)",
            bootstyle="warning",
            width=18,
            command=lambda: self._on_rating_click("guess")
        )
        self.guess_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Know button (Green/Easy)
        self.know_btn = tb.Button(
            buttons,
            text="✓ Know\n(Easy)",
            bootstyle="success",
            width=18,
            command=lambda: self._on_rating_click("know")
        )
        self.know_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Instructions
        instructions = tk.Label(
            buttons,
            text="Rate your knowledge to update difficulty and see next card",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#666"
        )
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 10))
    
    # ==================== Card Display Methods ====================
    
    def show_word(self, english: str, hebrew: str, difficulty: str):
        # Reset card to front side
        self.is_flipped = False
        self.current_english = english
        self.current_hebrew = hebrew
        self.current_difficulty = difficulty
        
        # Show English word
        self.word_label.config(text=english, fg="#283593")
        self.instruction_label.config(text="Click card to reveal translation")
        
        # Update difficulty badge
        self._update_difficulty_badge(difficulty)
        
        # Change card color to front (white)
        self.card_frame.config(bg="#ffffff")
        self.word_label.config(bg="#ffffff")
        self.instruction_label.config(bg="#ffffff")
    
    def flip_card(self):
        """Flip the card to show translation (or flip back)."""
        if not self.is_flipped:
            # Flip to back (show Hebrew)
            self.word_label.config(text=self.current_hebrew, fg="#1565c0")
            self.instruction_label.config(text="Hebrew Translation")
            self.card_frame.config(bg="#ffffff")
            self.word_label.config(bg="#ffffff")
            self.instruction_label.config(bg="#ffffff")
            self.is_flipped = True
        else:
            # Flip to front (show English)
            self.word_label.config(text=self.current_english, fg="#283593")
            self.instruction_label.config(text="Click card to reveal translation")
            self.card_frame.config(bg="#ffffff")
            self.word_label.config(bg="#ffffff")
            self.instruction_label.config(bg="#ffffff")
            self.is_flipped = False
    
    def _update_difficulty_badge(self, difficulty: str):
        """Update the difficulty badge appearance."""
        colors = {
            "NEW_WORD": ("#757575", "NEW"),
            "EASY": ("#43a047", "EASY"),
            "MEDIUM": ("#fb8c00", "MEDIUM"),
            "HARD": ("#e53935", "HARD")
        }
        
        bg_color, text = colors.get(difficulty, ("#757575", "NEW"))
        self.difficulty_badge.config(text=text, bg=bg_color)
    
    # ==================== Progress & Stats ====================
    
    def update_progress(self, current: int, total: int):
        """Update progress display."""
        self.progress_label.config(text=f"Card {current} / {total}")
    
    def update_stats(self, know: int, guess: int, dont_know: int):
        """Update statistics display."""
        self.stats_label.config(text=f"✓ {know}  ~ {guess}  ✗ {dont_know}")
    
    # ==================== Button Handlers ====================
    
    def _on_rating_click(self, rating: str):
        """
        Handle rating button click.
        
        This is a placeholder - the actual logic is in the controller.
        Override this or bind to controller methods.
        """
        print(f"Rating clicked: {rating}")
    
    # ==================== State Management ====================
    
    def show_welcome_message(self):
        """Show welcome message when no cards available."""
        self.word_label.config(text="No flashcards available")
        self.instruction_label.config(text="Select words to study from settings")
        self.difficulty_badge.grid_remove()
        
        # Disable buttons
        self.dont_know_btn.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self.know_btn.config(state="disabled")
    
    def enable_buttons(self):
        """Enable rating buttons."""
        self.dont_know_btn.config(state="normal")
        self.guess_btn.config(state="normal")
        self.know_btn.config(state="normal")
    
    def disable_buttons(self):
        """Disable rating buttons."""
        self.dont_know_btn.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self.know_btn.config(state="disabled")

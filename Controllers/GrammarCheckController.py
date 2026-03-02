import threading
from tkinter import messagebox


class GrammarCheckController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.page = self.view.pages["grammar_check_page"]

        # Import here to avoid circular imports
        try:
            from Utils.GrammarChecker import GrammarChecker
            self.checker = GrammarChecker()
        except ImportError:
            print("Warning: GrammarChecker not found")
            self.checker = None

        # Bind events
        self.bind()

    def bind(self):
        """Bind UI events."""
        self.page.back_btn.config(command=self.go_back)
        self.page.check_btn.config(command=self.check_grammar)

    def check_grammar(self):
        if not self.checker:
            messagebox.showerror(
                "Error",
                "Grammar checker is not available. Please check Utils/GrammarChecker.py",
                parent=self.page
            )
            return

        # Get input text
        text = self.page.get_input_text()

        if not text:
            messagebox.showwarning(
                "No Text",
                "Please enter a sentence to check.",
                parent=self.page
            )
            return

        # Show loading
        self.page.show_loading()
        self.page.clear_results()

        # Check grammar in background thread (to not freeze UI)
        thread = threading.Thread(target=self._check_grammar_async, args=(text,))
        thread.daemon = True
        thread.start()

    def _check_grammar_async(self, text: str):
        try:
            # Call API
            result = self.checker.check_grammar(text)

            # Update UI in main thread
            self.page.after(0, self._display_results, result)

        except Exception as e:
            result = {
                'is_correct': None,
                'error_count': 0,
                'errors': [],
                'corrected_text': text,
                'score': 0,
                'error': str(e)
            }
            self.page.after(0, self._display_results, result)

    def _display_results(self, result: dict):
        self.page.hide_loading()
        self.page.display_results(result)

    def go_back(self):
        self.view.show_page(self.view.pages["add_word_page"])

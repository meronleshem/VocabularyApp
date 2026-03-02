import tkinter as tk
from tkinter import ttk, scrolledtext
import ttkbootstrap as tb


class GrammarCheckPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#e8eaf6")

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create UI
        self._create_header()
        self._create_main_content()
        self._create_footer()

    def _create_header(self):
        header = tk.Frame(self, bg="#5e35b1", height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.columnconfigure(1, weight=1)

        # Back button
        self.back_btn = tb.Button(header, text="← Back",
                                  bootstyle="light-outline", width=10)
        self.back_btn.grid(row=0, column=0, padx=20, pady=20)

        # Title
        tk.Label(header, text="✍️ Grammar Checker",
                 font=("Segoe UI", 18, "bold"),
                 bg="#5e35b1", fg="#ffffff").grid(row=0, column=1, sticky="w", padx=20)

    def _create_main_content(self):
        """Create main content area."""
        main = tk.Frame(self, bg="#e8eaf6")
        main.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        # Input section
        self._create_input_section(main)

        # Check button
        self._create_check_button(main)

        # Results section
        self._create_results_section(main)

    def _create_input_section(self, parent):
        """Create text input area."""
        input_frame = tk.Frame(parent, bg="#ffffff", relief="flat",
                               highlightbackground="#c5cae9", highlightthickness=2)
        input_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))

        # Label
        tk.Label(input_frame, text="Enter your sentence:",
                 font=("Segoe UI", 12, "bold"),
                 bg="#ffffff", fg="#283593").pack(anchor="w", padx=20, pady=(15, 10))

        # Text input
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            font=("Segoe UI", 14),
            wrap=tk.WORD,
            height=8,
            relief="flat",
            bg="#ffffff"
        )
        self.input_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Placeholder text
        self.input_text.insert("1.0", "Type or paste your sentence here...")
        self.input_text.config(fg="gray")
        self.input_text.bind("<FocusIn>", self._clear_placeholder)
        self.input_text.bind("<FocusOut>", self._restore_placeholder)

    def _create_check_button(self, parent):
        """Create check grammar button."""
        btn_frame = tk.Frame(parent, bg="#e8eaf6")
        btn_frame.grid(row=1, column=0, pady=15)

        self.check_btn = tb.Button(
            btn_frame,
            text="🔍 Check Grammar",
            bootstyle="success",
            width=20,
            command=self._on_check_click
        )
        self.check_btn.pack()

        # Loading label
        self.loading_label = tk.Label(
            btn_frame,
            text="",
            font=("Segoe UI", 10),
            bg="#e8eaf6",
            fg="#666"
        )
        self.loading_label.pack(pady=(10, 0))

    def _create_results_section(self, parent):
        """Create results display area."""
        results_frame = tk.Frame(parent, bg="#ffffff", relief="flat",
                                 highlightbackground="#c5cae9", highlightthickness=2)
        results_frame.grid(row=2, column=0, sticky="nsew", pady=(20, 0))

        # Results label
        self.results_label = tk.Label(
            results_frame,
            text="Results will appear here",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
            fg="#666"
        )
        self.results_label.pack(anchor="w", padx=20, pady=(15, 10))

        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            height=10,
            relief="flat",
            bg="#f8f9fa",
            state="disabled"
        )
        self.results_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Configure text tags for coloring
        self.results_text.tag_config("correct", foreground="#28a745", font=("Segoe UI", 12, "bold"))
        self.results_text.tag_config("incorrect", foreground="#dc3545", font=("Segoe UI", 12, "bold"))
        self.results_text.tag_config("error", foreground="#ff6b6b")
        self.results_text.tag_config("suggestion", foreground="#0066cc", font=("Segoe UI", 11, "italic"))
        self.results_text.tag_config("score", foreground="#5e35b1", font=("Segoe UI", 14, "bold"))

    def _create_footer(self):
        """Create footer with instructions."""
        footer = tk.Frame(self, bg="#e8eaf6")
        footer.grid(row=2, column=0, sticky="ew", padx=40, pady=(10, 20))

        tk.Label(
            footer,
            text="💡 Tip: Write complete sentences for best results. Powered by LanguageTool API (Free).",
            font=("Segoe UI", 9),
            bg="#e8eaf6",
            fg="#666"
        ).pack()

    # ==================== Helper Methods ====================

    def _clear_placeholder(self, event):
        """Clear placeholder text on focus."""
        if self.input_text.get("1.0", "end-1c") == "Type or paste your sentence here...":
            self.input_text.delete("1.0", tk.END)
            self.input_text.config(fg="black")

    def _restore_placeholder(self, event):
        """Restore placeholder if empty."""
        if not self.input_text.get("1.0", "end-1c").strip():
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", "Type or paste your sentence here...")
            self.input_text.config(fg="gray")

    def _on_check_click(self):
        """Placeholder for check button click."""
        pass  # Will be overridden by controller

    # ==================== Public Methods ====================

    def get_input_text(self) -> str:
        """Get the text from input area."""
        text = self.input_text.get("1.0", "end-1c").strip()
        if text == "Type or paste your sentence here...":
            return ""
        return text

    def show_loading(self):
        """Show loading indicator."""
        self.loading_label.config(text="⏳ Checking grammar...")
        self.check_btn.config(state="disabled")

    def hide_loading(self):
        """Hide loading indicator."""
        self.loading_label.config(text="")
        self.check_btn.config(state="normal")

    def display_results(self, result: dict):
        """Display grammar check results."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        if result.get('error'):
            # API error
            self.results_label.config(text="❌ Error", fg="#dc3545")
            self.results_text.insert("1.0", f"Error: {result['error']}\n\n")
            self.results_text.insert(tk.END, "Please check your internet connection and try again.")

        elif result['is_correct']:
            # No errors found
            self.results_label.config(text="✓ Perfect!", fg="#28a745")
            self.results_text.insert("1.0", "✓ Excellent! No grammar or spelling errors found.\n\n", "correct")
            self.results_text.insert(tk.END, f"Grammar Score: {result['score']}/100", "score")

        else:
            # Errors found
            self.results_label.config(text=f"Found {result['error_count']} Issue(s)", fg="#dc3545")

            # Show score
            self.results_text.insert("1.0", f"Grammar Score: {result['score']}/100\n\n", "score")

            # Show errors
            self.results_text.insert(tk.END, f"✗ Found {result['error_count']} error(s):\n\n", "incorrect")

            for i, error in enumerate(result['errors'], 1):
                self.results_text.insert(tk.END, f"{i}. ", "error")
                self.results_text.insert(tk.END, f"{error['message']}\n", "error")

                if error['replacements']:
                    self.results_text.insert(tk.END, f"   💡 Suggestions: ", "suggestion")
                    self.results_text.insert(tk.END, f"{', '.join(error['replacements'])}\n\n", "suggestion")
                else:
                    self.results_text.insert(tk.END, "\n")

            # Show corrected version
            if result['corrected_text']:
                self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
                self.results_text.insert(tk.END, "✓ Corrected Version:\n\n", "correct")
                self.results_text.insert(tk.END, result['corrected_text'])

        self.results_text.config(state="disabled")

    def clear_results(self):
        """Clear results area."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state="disabled")
        self.results_label.config(text="Results will appear here", fg="#666")

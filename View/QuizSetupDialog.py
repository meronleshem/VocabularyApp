import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from typing import List, Dict, Optional
import re


# ==================== Natural Sorting Function ====================

def natural_sort_key(text):
    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    parts = re.split(r'(\d+)', str(text) if text else "")
    return [convert(part) for part in parts]


# ==================== Quiz Setup Dialog ====================

class QuizSetupDialog(tk.Toplevel):
    def __init__(self, parent, available_groups: List[str]):
        super().__init__(parent)

        self.available_groups = available_groups
        self.result: Optional[Dict] = None

        # Configuration
        self.title("Quiz Setup")
        self.geometry("850x550")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Configure background
        self.configure(bg="#e8eaf6")

        # Create UI
        self._create_header()
        self._create_content()
        self._create_buttons()

        # Center dialog
        self._center_dialog()

        # Wait for user
        self.wait_window()

    def _create_header(self):
        """Create header."""
        header = tk.Frame(self, bg="#3f51b5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg="#3f51b5")
        header_content.pack(fill="both", expand=True, padx=20, pady=12)

        tk.Label(header_content, text="🎯 Quiz Setup",
                 font=("Segoe UI", 16, "bold"),
                 bg="#3f51b5", fg="#ffffff").pack(side="left")

        tk.Label(header_content, text="Configure your quiz settings",
                 font=("Segoe UI", 9),
                 bg="#3f51b5", fg="#e8eaf6").pack(side="left", padx=(15, 0))

    def _create_content(self):
        """Create horizontal layout."""
        content = tk.Frame(self, bg="#e8eaf6")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=1)

        self._create_difficulty_column(content)
        self._create_groups_column(content)
        self._create_settings_column(content)

    def _create_difficulty_column(self, parent):
        """Create difficulty column."""
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        header = tk.Frame(card, bg="#43a047")
        header.pack(fill="x")

        tk.Label(header, text="📊 Difficulty",
                 font=("Segoe UI", 11, "bold"),
                 bg="#43a047", fg="#ffffff").pack(pady=12, padx=15)

        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text="Select levels to include:",
                 font=("Segoe UI", 8),
                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 8))

        self.diff_new = tk.IntVar(value=1)
        self.diff_easy = tk.IntVar(value=1)
        self.diff_medium = tk.IntVar(value=1)
        self.diff_hard = tk.IntVar(value=1)

        ttk.Checkbutton(content, text="New Words",
                        variable=self.diff_new).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Easy",
                        variable=self.diff_easy).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Medium",
                        variable=self.diff_medium).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Hard",
                        variable=self.diff_hard).pack(anchor="w", pady=3)

    def _create_groups_column(self, parent):
        """Create groups column with hierarchical tree."""
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=1, sticky="nsew", padx=4)

        header = tk.Frame(card, bg="#1e88e5")
        header.pack(fill="x")

        tk.Label(header, text="📚 Groups",
                 font=("Segoe UI", 11, "bold"),
                 bg="#1e88e5", fg="#ffffff").pack(pady=12, padx=15)

        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text="Choose word groups:",
                 font=("Segoe UI", 8),
                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 8))

        # Tree view with scrollbar
        tree_frame = tk.Frame(content, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True)

        # Create treeview
        self.groups_tree = ttk.Treeview(tree_frame, show="tree", height=10)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.groups_tree.yview)
        self.groups_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.groups_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate tree with hierarchical groups
        self._populate_groups_tree()

        # Bind click events
        self.groups_tree.bind("<Button-1>", self._on_tree_click)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            self.groups_tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.groups_tree.bind("<MouseWheel>", _on_mousewheel)

        # Quick buttons
        if self.available_groups:
            btn_row = tk.Frame(content, bg="#ffffff")
            btn_row.pack(fill="x", pady=(8, 0))

            tb.Button(btn_row, text="All", bootstyle="info-outline",
                      width=8, command=self._select_all_groups).pack(side="left", padx=(0, 4))
            tb.Button(btn_row, text="None", bootstyle="secondary-outline",
                      width=8, command=self._deselect_all_groups).pack(side="left")

    def _populate_groups_tree(self):
        """Populate tree with hierarchical group structure - WITH NATURAL SORTING! 🎯"""
        if not self.available_groups:
            return

        # Organize groups into hierarchy
        hierarchy = self._organize_groups_hierarchy()

        # Storage for tree items
        self.tree_items = {}  # Maps group name to tree item id
        self.item_states = {}  # Maps item id to checkbox state (True/False)

        # 🌟 NATURAL SORT for book names! 🌟
        for book_name, chapters in sorted(hierarchy.items(), key=natural_sort_key):
            if len(chapters) == 1 and chapters[0] == book_name:
                # Single group, no hierarchy
                item_id = self.groups_tree.insert("", "end", text=f"☐ {book_name}",
                                                  tags=("unchecked",))
                self.tree_items[book_name] = item_id
                self.item_states[item_id] = True  # Selected by default
                # Update to checked
                self.groups_tree.item(item_id, text=f"☑ {book_name}", tags=("checked",))
            else:
                # Book with chapters
                book_id = self.groups_tree.insert("", "end", text=f"☐ {book_name} ({len(chapters)})",
                                                  tags=("book", "unchecked"))
                self.tree_items[f"__BOOK__{book_name}"] = book_id
                self.item_states[book_id] = True  # Selected by default

                # 🌟 NATURAL SORT for chapters! 🌟
                for chapter in sorted(chapters, key=natural_sort_key):
                    chapter_id = self.groups_tree.insert(book_id, "end", text=f"☐ {chapter}",
                                                         tags=("chapter", "unchecked"))
                    self.tree_items[chapter] = chapter_id
                    self.item_states[chapter_id] = True  # Selected by default
                    # Update to checked
                    self.groups_tree.item(chapter_id, text=f"☑ {chapter}", tags=("chapter", "checked"))

                # Update book checkbox
                self.groups_tree.item(book_id, text=f"☑ {book_name} ({len(chapters)})",
                                      tags=("book", "checked"))

    def _organize_groups_hierarchy(self) -> Dict[str, List[str]]:
        """
        Organize groups into book -> chapters hierarchy.

        Returns:
            Dict mapping book name to list of chapter names
        """
        hierarchy = {}

        for group in self.available_groups:
            # Try to extract book and chapter
            # Pattern: "Book Name Chapter" or "Book Name 1" etc.
            match = re.match(r'^(.+?)\s+(\d+|[IVX]+)$', group)

            if match:
                book_name = match.group(1)
                full_name = group

                if book_name not in hierarchy:
                    hierarchy[book_name] = []

                hierarchy[book_name].append(full_name)
            else:
                # Single group without chapter
                hierarchy[group] = [group]

        return hierarchy

    def _on_tree_click(self, event):
        """Handle tree item click."""
        region = self.groups_tree.identify_region(event.x, event.y)
        if region != "tree":
            return

        item = self.groups_tree.identify_row(event.y)
        if not item:
            return

        # Toggle checkbox
        current_state = self.item_states.get(item, False)
        new_state = not current_state
        self.item_states[item] = new_state

        # Update checkbox display
        text = self.groups_tree.item(item, "text")
        checkbox = "☑" if new_state else "☐"

        if text.startswith("☑") or text.startswith("☐"):
            text = text[2:]

        self.groups_tree.item(item, text=f"{checkbox} {text}")

        # Update tags
        tags = list(self.groups_tree.item(item, "tags"))
        if "checked" in tags:
            tags.remove("checked")
        if "unchecked" in tags:
            tags.remove("unchecked")
        tags.append("checked" if new_state else "unchecked")
        self.groups_tree.item(item, tags=tuple(tags))

        # If it's a parent, update all children
        children = self.groups_tree.get_children(item)
        if children:
            for child in children:
                self.item_states[child] = new_state
                child_text = self.groups_tree.item(child, "text")
                if child_text.startswith("☑") or child_text.startswith("☐"):
                    child_text = child_text[2:]

                self.groups_tree.item(child, text=f"{checkbox} {child_text}")

                # Update child tags
                child_tags = list(self.groups_tree.item(child, "tags"))
                if "checked" in child_tags:
                    child_tags.remove("checked")
                if "unchecked" in child_tags:
                    child_tags.remove("unchecked")
                child_tags.append("checked" if new_state else "unchecked")
                self.groups_tree.item(child, tags=tuple(child_tags))

        # If it's a chapter, update parent book
        parent = self.groups_tree.parent(item)
        if parent:
            siblings = self.groups_tree.get_children(parent)
            all_checked = all(self.item_states.get(s, False) for s in siblings)
            any_checked = any(self.item_states.get(s, False) for s in siblings)

            parent_checkbox = "☑" if all_checked else "☐"
            parent_text = self.groups_tree.item(parent, "text")
            if parent_text.startswith("☑") or parent_text.startswith("☐"):
                parent_text = parent_text[2:]

            self.groups_tree.item(parent, text=f"{parent_checkbox} {parent_text}")
            self.item_states[parent] = all_checked

    def _select_all_groups(self):
        """Select all groups."""
        for item in self.groups_tree.get_children():
            self._set_item_checked(item, True)

    def _deselect_all_groups(self):
        """Deselect all groups."""
        for item in self.groups_tree.get_children():
            self._set_item_checked(item, False)

    def _set_item_checked(self, item, checked):
        """Recursively set item and children checked state."""
        self.item_states[item] = checked
        text = self.groups_tree.item(item, "text")
        checkbox = "☑" if checked else "☐"

        if text.startswith("☑") or text.startswith("☐"):
            text = text[2:]

        self.groups_tree.item(item, text=f"{checkbox} {text}")

        # Update children
        for child in self.groups_tree.get_children(item):
            self._set_item_checked(child, checked)

    def _get_selected_groups(self) -> List[str]:
        """Get list of selected group names."""
        selected = []

        for group_name, item_id in self.tree_items.items():
            if group_name.startswith("__BOOK__"):
                continue  # Skip book parents

            if self.item_states.get(item_id, False):
                selected.append(group_name)

        return selected

    def _create_settings_column(self, parent):
        """Create settings column."""
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        header = tk.Frame(card, bg="#fb8c00")
        header.pack(fill="x")

        tk.Label(header, text="⚙️ Settings",
                 font=("Segoe UI", 11, "bold"),
                 bg="#fb8c00", fg="#ffffff").pack(pady=12, padx=15)

        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text="Quiz Length:",
                 font=("Segoe UI", 10, "bold"),
                 bg="#ffffff", fg="#283593").pack(anchor="w", pady=(0, 8))

        self.quiz_length = tk.StringVar(value="all")

        ttk.Radiobutton(content, text="All words",
                        variable=self.quiz_length,
                        value="all").pack(anchor="w", pady=4)

        custom_row = tk.Frame(content, bg="#ffffff")
        custom_row.pack(anchor="w", pady=4)

        ttk.Radiobutton(custom_row, text="Limit to:",
                        variable=self.quiz_length,
                        value="custom").pack(side="left")

        self.custom_count = tk.IntVar(value=20)
        ttk.Spinbox(custom_row, from_=5, to=100, width=8,
                    textvariable=self.custom_count).pack(side="left", padx=(5, 3))

        tk.Label(custom_row, text="questions", bg="#ffffff",
                 font=("Segoe UI", 8), fg="#666").pack(side="left")

        tk.Frame(content, bg="#ffffff", height=15).pack()

        tk.Label(content, text="Quick Options:",
                 font=("Segoe UI", 10, "bold"),
                 bg="#ffffff", fg="#283593").pack(anchor="w", pady=(5, 8))

        tk.Frame(content, bg="#e0e0e0", height=1).pack(fill="x", pady=8)

        preset_frame = tk.Frame(content, bg="#ffffff")
        preset_frame.pack(fill="x")

        tb.Button(preset_frame, text="🎯 Easy Quiz",
                  bootstyle="success-outline",
                  command=self._preset_easy).pack(fill="x", pady=2)

        tb.Button(preset_frame, text="🔥 Hard Quiz",
                  bootstyle="danger-outline",
                  command=self._preset_hard).pack(fill="x", pady=2)

        tb.Button(preset_frame, text="📝 Quick 10",
                  bootstyle="info-outline",
                  command=self._preset_quick).pack(fill="x", pady=2)

    def _create_buttons(self):
        """Create action buttons."""
        btn_frame = tk.Frame(self, bg="#e8eaf6")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        info_label = tk.Label(btn_frame,
                              text="💡 Tip: Click books to expand/collapse chapters",
                              font=("Segoe UI", 8),
                              bg="#e8eaf6", fg="#666")
        info_label.pack(side="left")

        tb.Button(btn_frame, text="Cancel", bootstyle="secondary",
                  width=12, command=self._on_cancel).pack(side="right", padx=(8, 0))

        tb.Button(btn_frame, text="Start Quiz →", bootstyle="success",
                  width=14, command=self._on_start).pack(side="right")

    def _preset_easy(self):
        """Easy quiz preset."""
        self.diff_new.set(1)
        self.diff_easy.set(1)
        self.diff_medium.set(0)
        self.diff_hard.set(0)
        self.quiz_length.set("custom")
        self.custom_count.set(15)

    def _preset_hard(self):
        """Hard quiz preset."""
        self.diff_new.set(0)
        self.diff_easy.set(0)
        self.diff_medium.set(1)
        self.diff_hard.set(1)
        self.quiz_length.set("all")

    def _preset_quick(self):
        """Quick quiz preset."""
        self.diff_new.set(1)
        self.diff_easy.set(1)
        self.diff_medium.set(1)
        self.diff_hard.set(1)
        self.quiz_length.set("custom")
        self.custom_count.set(10)

    def _on_start(self):
        """Handle Start Quiz button."""
        difficulties = []
        if self.diff_new.get():
            difficulties.append("NEW_WORD")
        if self.diff_easy.get():
            difficulties.append("EASY")
        if self.diff_medium.get():
            difficulties.append("MEDIUM")
        if self.diff_hard.get():
            difficulties.append("HARD")

        if not difficulties:
            messagebox.showwarning(
                "No Difficulty Selected",
                "Please select at least one difficulty level.",
                parent=self
            )
            return

        selected_groups = self._get_selected_groups()

        if self.quiz_length.get() == "all":
            question_count = None
        else:
            question_count = self.custom_count.get()

        self.result = {
            "difficulties": difficulties,
            "groups": selected_groups if selected_groups else None,
            "question_count": question_count
        }

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = None
        self.destroy()

    def _center_dialog(self):
        """Center dialog on parent."""
        self.update_idletasks()
        parent = self.master

        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2

        self.geometry(f"+{x}+{y}")

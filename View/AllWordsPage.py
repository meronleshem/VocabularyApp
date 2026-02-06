import tkinter as tk
from tkinter import ttk


class AllWordsPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.all_words_cache = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ===== Title =====
        title = ttk.Label(
            self,
            text="All Words",
            font=("Segoe UI", 16, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # ===== Top Bar =====
        top_bar = ttk.Frame(self)
        top_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        top_bar.columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            top_bar,
            textvariable=self.search_var,
            font=("Segoe UI", 11)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        #self.search_entry.insert(0, "Search…")

        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.search_placeholder = "Search…"
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.configure(foreground="gray")

        self.search_entry.bind("<FocusIn>", self._clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_search_placeholder)

        # ===== Table =====
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("English", "Hebrew", "Difficulty", "Group")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")

        self.tree.column("English", width=150)
        self.tree.column("Hebrew", width=350)
        self.tree.column("Difficulty", width=100, anchor="center")
        self.tree.column("Group", width=150)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_double_click)

        # ===== Footer =====
        self.footer_label = ttk.Label(
            self,
            text="Double-click to change difficulty",
            foreground="gray"
        )
        self.footer_label.grid(row=3, column=0, sticky="w", pady=(8, 0))

        # ===== Bottom Bar =====
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.add_word_btn = ttk.Button(bottom_bar, text="Home Page")
        self.add_word_btn.pack()

    # ================= Logic =================

    def show_words(self, word_list):
        self.all_words_cache = word_list
        self._populate_tree(word_list)

    def _populate_tree(self, words):
        self.clear_treeview()
        for eng, heb, diff, group in words:
            self.tree.insert("", "end", values=(eng, heb, diff, group))

    def on_search(self, event=None):
        query = self.search_var.get().strip().lower()

        if not query:
            self._populate_tree(self.all_words_cache)
            return

        filtered = [
            word for word in self.all_words_cache
            if query in str(word[0]).lower()
            or query in str(word[1]).lower()
            or query in str(word[3]).lower()
        ]

        self._populate_tree(filtered)

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_double_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item[0], "values")
        print(values)

    def _clear_search_placeholder(self, event):
        if self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground="black")

    def _restore_search_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, self.search_placeholder)
            self.search_entry.configure(foreground="gray")

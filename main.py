import os
import sqlite3
import datetime
import barcode
from barcode.writer import ImageWriter
import tkinter as tk
from tkinter import ttk, messagebox

class LibraryManagementSystem:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.create_ui()

    def create_tables(self):
        """Creates necessary database tables for the library management system."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                donated_by TEXT,
                date_added TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                standard TEXT NOT NULL,
                division TEXT NOT NULL,
                roll_number INTEGER NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(member_id) REFERENCES members(id)
            )
        ''')
        
        self.connection.commit()

    def create_ui(self):
        """Creates the user interface for the library management system."""
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        
        # Create tabs for each section
        self.tab_control = ttk.Notebook(self.root)
        
        self.book_tab = ttk.Frame(self.tab_control)
        self.member_tab = ttk.Frame(self.tab_control)
        self.transaction_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.book_tab, text="Books")
        self.tab_control.add(self.member_tab, text="Members")
        self.tab_control.add(self.transaction_tab, text="Transactions")
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_book_tab()
        self.setup_member_tab()
        self.setup_transaction_tab()
        
        self.root.mainloop()
    
    def setup_member_tab(self):
        """Sets up the Member tab in the UI."""
        self.member_name_entry = tk.Entry(self.member_tab)
        self.member_name_entry.pack()
        
        self.member_standard_entry = tk.Entry(self.member_tab)
        self.member_standard_entry.pack()
        
        self.member_division_entry = tk.Entry(self.member_tab)
        self.member_division_entry.pack()
        
        self.member_roll_number_entry = tk.Entry(self.member_tab)
        self.member_roll_number_entry.pack()
        
        self.add_member_button = tk.Button(self.member_tab, text="Add Member", command=self.add_member_from_ui)
        self.add_member_button.pack()
    
    def add_member_from_ui(self):
        name = self.member_name_entry.get()
        standard = self.member_standard_entry.get()
        division = self.member_division_entry.get()
        roll_number = self.member_roll_number_entry.get()
        self.add_member(name, standard, division, roll_number)
    
    def add_member(self, name, standard, division, roll_number):
        """Adds a new library member."""
        try:
            self.cursor.execute('''
                INSERT INTO members (name, standard, division, roll_number)
                VALUES (?, ?, ?, ?)
            ''', (name, standard, division, roll_number))
            self.connection.commit()
            messagebox.showinfo("Success", f"Member '{name}' added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", "Error adding member: " + str(e))
    
    def close(self):
        """Closes the database connection."""
        self.connection.close()

if __name__ == "__main__":
    system = LibraryManagementSystem()

# Made with ❤️ by Krypton03625

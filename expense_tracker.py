import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def setup_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT)''')
    conn.commit()
    conn.close()

setup_db()

def add_expense():
    date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = desc_entry.get()
    
    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all fields")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                   (date, category, amount, description))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Expense added successfully!")
    view_expenses()
    clear_fields()

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    conn.close()
    
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    
    for record in records:
        expense_tree.insert("", tk.END, values=record)


def delete_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an expense to delete")
        return
    
    expense_id = expense_tree.item(selected_item)['values'][0]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Expense deleted successfully!")
    view_expenses()

def export_csv():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    conn.close()
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
            writer.writerows(records)
        messagebox.showinfo("Success", "Expenses exported successfully!")

def show_analysis():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    records = cursor.fetchall()
    conn.close()
    
    categories = [record[0] for record in records]
    amounts = [record[1] for record in records]
    
    analysis_frame.pack(fill=tk.BOTH, expand=True)
    plt.figure(figsize=(6, 4))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Breakdown by Category")
    plt.show()

def clear_fields():
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x500")

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()
date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

tk.Label(root, text="Category").pack()
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["Food", "Rent", "Travel", "Shopping", "Other"])
category_dropdown.pack()
category_dropdown.current(0)

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Show Analysis", command=show_analysis).pack(pady=5)
tk.Button(root, text="Export to CSV", command=export_csv).pack(pady=5)


columns = ("ID", "Date", "Category", "Amount", "Description")
expense_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100)
expense_tree.pack(pady=10)

tk.Button(root, text="Delete Expense", command=delete_expense).pack(pady=5)


analysis_frame = tk.Frame(root)
analysis_frame.pack_forget()

view_expenses()
root.mainloop()

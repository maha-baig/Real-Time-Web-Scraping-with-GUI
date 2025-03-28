import tkinter as tk
from tkinter import ttk
import pandas as pd
import subprocess
import webbrowser
import sys

# Load Data
def load_data():
    return pd.read_csv("data/latest_news.csv")

df = load_data()

# GUI Setup
root = tk.Tk()
root.title("📢 News Sentiment Dashboard")
root.geometry("1000x700")
root.configure(bg="#1E1E1E")

# --- Refresh Data ---
def refresh_data():
    subprocess.run([sys.executable, "scraper.py"])
    global df
    df = load_data()
    update_table(df)

# --- Update Table ---
def update_table(filtered_df):
    for row in tree.get_children():
        tree.delete(row)

    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=(row["Source"], row["Headline"], row["Sentiment"], row["URL"]))

# --- Open Link ---
def open_link(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        url = item["values"][3]
        webbrowser.open(url)

# --- Sorting ---
def sort_data():
    sort_order = sort_var.get()
    if sort_order == "Most Negative":
        sorted_df = df.sort_values(by="Sentiment", ascending=True)
    elif sort_order == "Most Positive":
        sorted_df = df.sort_values(by="Sentiment", ascending=False)
    else:
        sorted_df = df
    update_table(sorted_df)

# --- Widgets ---
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

# Title
ttk.Label(frame, text="📊 News Sentiment Dashboard", font=("Arial", 20, "bold"), background="#1E1E1E", foreground="#FF6B6B").grid(row=0, column=0, columnspan=3, pady=10)

# Sorting Option
ttk.Label(frame, text="Sort By:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
sort_var = ttk.Combobox(frame, values=["Most Negative", "Most Positive", "All"], font=("Arial", 12))
sort_var.current(2)
sort_var.grid(row=1, column=1, padx=10, pady=5)
ttk.Button(frame, text="Sort", command=sort_data).grid(row=1, column=2, padx=10, pady=5)

# Refresh Button
ttk.Button(frame, text="🔄 Refresh News", command=refresh_data).grid(row=2, column=0, columnspan=3, pady=10)

# Data Table
tree_frame = tk.Frame(root, bg="#1E1E1E")
tree_frame.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=("Source", "Headline", "Sentiment", "URL"), show="headings", height=15)
tree.heading("Source", text="Source")
tree.heading("Headline", text="Headline")
tree.heading("Sentiment", text="Sentiment Score")
tree.heading("URL", text="URL")

tree.column("Source", width=100)
tree.column("Headline", width=500)
tree.column("Sentiment", width=100)
tree.column("URL", width=200)

tree.pack(fill="both", expand=True)

# Make headlines clickable
tree.bind("<Double-1>", open_link)

# Run GUI
root.mainloop()

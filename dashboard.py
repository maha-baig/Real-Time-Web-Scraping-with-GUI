import tkinter as tk
from tkinter import ttk
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
# Load initial data
def load_data():
    return pd.read_csv("data/latest_news.csv")

df = load_data()

# GUI setup
root = tk.Tk()
root.title("📢 News Headlines Dashboard")
root.geometry("950x700")
root.configure(bg="#1E1E1E")

# --- REFRESH FUNCTION ---
def refresh_data():
    subprocess.run([sys.executable, "scraper.py"])
    global df
    df = load_data()  # Reload data
    filter_data()  # Refresh displayed content

# --- FILTERING FUNCTION ---
def filter_data():
    timeframe = timeframe_var.get()
    keyword = keyword_entry.get().lower()

    filtered_df = df.copy()

    # Time-based filtering
    if timeframe != "All":
        from datetime import datetime, timedelta
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        now = datetime.now()
        if timeframe == "Last 24 hours":
            filtered_df = filtered_df[df["Timestamp"] >= now - timedelta(days=1)]
        elif timeframe == "Last 7 days":
            filtered_df = filtered_df[df["Timestamp"] >= now - timedelta(days=7)]

    # Keyword filtering
    if keyword:
        filtered_df = filtered_df[filtered_df["Headline"].str.contains(keyword, case=False, na=False)]

    update_table(filtered_df)

# --- DISPLAY FUNCTION ---
def update_table(filtered_df):
    """Updates displayed headlines"""
    for row in tree.get_children():
        tree.delete(row)

    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=(row["Headline"], row["Timestamp"]))

# --- GUI WIDGETS ---
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

# Title
ttk.Label(frame, text="📰 News Headlines Dashboard", font=("Arial", 20, "bold"), background="#1E1E1E", foreground="#FF6B6B").grid(row=0, column=0, columnspan=3, pady=10)

# Time Filter
ttk.Label(frame, text="Timeframe:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
timeframe_var = ttk.Combobox(frame, values=["All", "Last 24 hours", "Last 7 days"], font=("Arial", 12))
timeframe_var.current(0)
timeframe_var.grid(row=1, column=1, padx=10, pady=5)

# Keyword Filter
ttk.Label(frame, text="Keyword Filter:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
keyword_entry = ttk.Entry(frame, font=("Arial", 12))
keyword_entry.grid(row=2, column=1, padx=10, pady=5)

# Apply Filter Button
ttk.Button(frame, text="Apply Filters", command=filter_data).grid(row=3, column=0, columnspan=2, pady=10)

# Refresh Button
ttk.Button(frame, text="🔄 Refresh News", command=refresh_data, style="TButton").grid(row=4, column=0, columnspan=2, pady=10)

# Data Table
tree_frame = tk.Frame(root, bg="#1E1E1E")
tree_frame.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=("Headline", "Timestamp"), show="headings", height=10)
tree.heading("Headline", text="Headline")
tree.heading("Timestamp", text="Timestamp")

tree.column("Headline", width=600)
tree.column("Timestamp", width=200, anchor="center")

tree.pack(fill="both", expand=True)

# Run GUI
root.mainloop()

import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedStyle

# Load Data
df = pd.read_csv("data/enhanced_headlines.csv")

# GUI Setup
root = tk.Tk()
root.title("📢 News Headlines Dashboard")
root.geometry("950x650")
root.configure(bg="#1E1E1E")

# Apply Themed Styling
style = ThemedStyle(root)
style.set_theme("equilux")  # A dark modern theme
style.configure("TLabel", font=("Arial", 12), background="#1E1E1E", foreground="white")
style.configure("TButton", font=("Arial", 12, "bold"), background="#FF6B6B", foreground="white")
style.configure("TEntry", font=("Arial", 12), padding=5)
style.configure("TCombobox", font=("Arial", 12))
style.configure("Treeview", font=("Arial", 11), background="#2C2C2C", foreground="white", rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#FF6B6B", foreground="white")

# --- FILTERING FUNCTION ---
def filter_data():
    sentiment = sentiment_var.get()
    keyword = keyword_entry.get().lower()
    min_length = int(length_var.get())

    filtered_df = df.copy()

    if sentiment != "All":
        filtered_df = filtered_df[filtered_df["Sentiment_Label"] == sentiment]

    if keyword:
        filtered_df = filtered_df[filtered_df["Cleaned_Headline"].str.contains(keyword, case=False, na=False)]

    filtered_df = filtered_df[filtered_df["Word_Count"] >= min_length]

    update_table(filtered_df)
    update_chart(filtered_df)

# --- DISPLAY FUNCTION ---
def update_table(filtered_df):
    """Updates the displayed headlines"""
    for row in tree.get_children():
        tree.delete(row)

    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=(row["Headline"], row["Sentiment_Label"], row["Word_Count"]))

# --- CHART FUNCTION ---
def update_chart(filtered_df):
    """Updates sentiment distribution chart"""
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.set_style("darkgrid")
    sns.countplot(x=filtered_df["Sentiment_Label"], palette="coolwarm", ax=ax)
    ax.set_title("Sentiment Distribution", fontsize=14, fontweight="bold")

    # Embed in Tkinter
    for widget in chart_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

# --- GUI WIDGETS ---
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

# Title
title_label = ttk.Label(frame, text="📰 News Headlines Dashboard", font=("Arial", 20, "bold"), background="#1E1E1E", foreground="#FF6B6B")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Sentiment Filter
ttk.Label(frame, text="Filter by Sentiment:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
sentiment_var = ttk.Combobox(frame, values=["All", "Positive", "Negative", "Neutral"], font=("Arial", 12))
sentiment_var.current(0)
sentiment_var.grid(row=1, column=1, padx=10, pady=5)

# Keyword Filter
ttk.Label(frame, text="Keyword Filter:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
keyword_entry = ttk.Entry(frame, font=("Arial", 12))
keyword_entry.grid(row=2, column=1, padx=10, pady=5)

# Word Length Filter
ttk.Label(frame, text="Min Word Length:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
length_var = ttk.Spinbox(frame, from_=0, to=50, font=("Arial", 12))
length_var.grid(row=3, column=1, padx=10, pady=5)

# Apply Filter Button
apply_button = ttk.Button(frame, text="Apply Filters", command=filter_data, style="TButton")
apply_button.grid(row=4, column=0, columnspan=2, pady=10)

# Data Table
tree_frame = tk.Frame(root, bg="#1E1E1E")
tree_frame.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=("Headline", "Sentiment", "Length"), show="headings", height=10)
tree.heading("Headline", text="Headline")
tree.heading("Sentiment", text="Sentiment")
tree.heading("Length", text="Word Count")

tree.column("Headline", width=500)
tree.column("Sentiment", width=100, anchor="center")
tree.column("Length", width=100, anchor="center")

tree.pack(fill="both", expand=True)

# Chart Section
chart_frame = tk.Frame(root, bg="#1E1E1E")
chart_frame.pack()

# Run GUI
root.mainloop()

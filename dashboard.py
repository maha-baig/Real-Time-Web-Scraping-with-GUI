import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the enhanced dataset
df = pd.read_csv("data/enhanced_headlines.csv")

# GUI setup
root = tk.Tk()
root.title("News Headlines Dashboard")
root.geometry("900x600")

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

    # Update the display
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
    sns.countplot(x=filtered_df["Sentiment_Label"], palette="coolwarm", ax=ax)
    ax.set_title("Sentiment Distribution")

    # Embed in Tkinter
    for widget in chart_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

# --- GUI WIDGETS ---
ttk.Label(root, text="Filter by Sentiment:").pack()
sentiment_var = ttk.Combobox(root, values=["All", "Positive", "Negative", "Neutral"])
sentiment_var.current(0)
sentiment_var.pack()

ttk.Label(root, text="Keyword Filter:").pack()
keyword_entry = ttk.Entry(root)
keyword_entry.pack()

ttk.Label(root, text="Min Word Length:").pack()
length_var = ttk.Spinbox(root, from_=0, to=50)
length_var.pack()

ttk.Button(root, text="Apply Filters", command=filter_data).pack()

# Data Table
tree = ttk.Treeview(root, columns=("Headline", "Sentiment", "Length"), show="headings", height=10)
tree.heading("Headline", text="Headline")
tree.heading("Sentiment", text="Sentiment")
tree.heading("Length", text="Word Count")
tree.pack(fill="both", expand=True)

# Chart Section
chart_frame = tk.Frame(root)
chart_frame.pack()

# Run GUI
root.mainloop()
# This code creates a simple GUI dashboard using Tkinter to visualize and filter news headlines data.
# Users can filter by sentiment, keyword, and minimum word length.
import json
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import sys

# Data storage
trades_data = {}

def save_data():
    with open("trades_data.json", "w") as f:
        json.dump(trades_data, f)

def load_data():
    global trades_data
    try:
        with open("trades_data.json", "r") as f:
            trades_data = json.load(f)
    except FileNotFoundError:
        trades_data = {}

def add_pair_gui():
    pair_name = simpledialog.askstring("Add Pair", "Enter pair name:")
    if not pair_name:
        return
    if pair_name not in trades_data:
        trades_data[pair_name] = []
        save_data()
        messagebox.showinfo("Success", f"Pair '{pair_name}' added!")
        update_pair_list()
    else:
        messagebox.showwarning("Warning", "Pair already exists!")

def add_trade_gui():
    selected_pair = pair_var.get()
    if not selected_pair:
        messagebox.showwarning("Error", "Select a pair!")
        return
    
    result = result_var.get()
    bias_followed = bias_var.get() == "Yes"
    map_color = map_var.get()
    confluences = [c.strip() for c in conf_entry.get().split(",") if c.strip()]

    trade = {
        "result": result,
        "confluences": confluences,
        "bias_followed": bias_followed,
        "map_color": map_color
    }
    trades_data[selected_pair].append(trade)
    save_data()
    messagebox.showinfo("Success", f"Trade added to {selected_pair}")

def calculate_statistics(trades):
    stats = {
        "wins": 0,
        "losses": 0,
        "confluence_wins": {},
        "confluence_losses": {},
        "map_wins": {},
        "map_losses": {},
        "bias_correct": 0,
        "bias_incorrect": 0
    }
    
    for trade in trades:
        if trade["result"] == "win":
            stats["wins"] += 1
            for conf in trade["confluences"]:
                stats["confluence_wins"][conf] = stats["confluence_wins"].get(conf, 0) + 1
            stats["map_wins"][trade["map_color"]] = stats["map_wins"].get(trade["map_color"], 0) + 1
        else:
            stats["losses"] += 1
            for conf in trade["confluences"]:
                stats["confluence_losses"][conf] = stats["confluence_losses"].get(conf, 0) + 1
            stats["map_losses"][trade["map_color"]] = stats["map_losses"].get(trade["map_color"], 0) + 1
        
        if trade["bias_followed"]:
            stats["bias_correct"] += 1
        else:
            stats["bias_incorrect"] += 1
    
    return stats

def plot_statistics():
    selected_pair = stats_pair_var.get()
    if selected_pair == "All":
        trades = [trade for trades in trades_data.values() for trade in trades]
    else:
        trades = trades_data.get(selected_pair, [])
    
    if not trades:
        messagebox.showwarning("No data", "No trades available!")
        return
    
    total_stats = calculate_statistics(trades)

    plt.figure(figsize=(15, 10))

    # Win/Loss total
    plt.subplot(2, 2, 1)
    plt.bar(["Wins", "Losses"], [total_stats["wins"], total_stats["losses"]], color=['green', 'red'])
    plt.title("Total Wins vs Losses")

    # Confluences Win/Loss
    plt.subplot(2, 2, 2)
    all_confs = list(set(total_stats["confluence_wins"].keys()).union(total_stats["confluence_losses"].keys()))
    wins = [total_stats["confluence_wins"].get(c, 0) for c in all_confs]
    losses = [total_stats["confluence_losses"].get(c, 0) for c in all_confs]
    bar_width = 0.35
    x = range(len(all_confs))
    plt.bar(x, wins, width=bar_width, color='green', label='Wins')
    plt.bar([i + bar_width for i in x], losses, width=bar_width, color='red', label='Losses')
    plt.xticks([i + bar_width/2 for i in x], all_confs, rotation=45)
    plt.title("Confluence Wins/Losses")
    plt.legend()

    # Map Win/Loss
    plt.subplot(2, 2, 3)
    all_maps = list(set(total_stats["map_wins"].keys()).union(total_stats["map_losses"].keys()))
    map_win_counts = [total_stats["map_wins"].get(m, 0) for m in all_maps]
    map_loss_counts = [total_stats["map_losses"].get(m, 0) for m in all_maps]
    x = range(len(all_maps))
    plt.bar(x, map_win_counts, width=bar_width, color='green', label='Wins')
    plt.bar([i + bar_width for i in x], map_loss_counts, width=bar_width, color='red', label='Losses')
    plt.xticks([i + bar_width/2 for i in x], all_maps)
    plt.title("Map Colors Wins/Losses")
    plt.legend()

    # Bias info
    plt.subplot(2, 2, 4)
    plt.bar(["Bias Correct", "Bias Incorrect"], [total_stats["bias_correct"], total_stats["bias_incorrect"]], color=['blue', 'orange'])
    plt.title("Bias Followed vs Not Followed")

    plt.tight_layout()
    plt.show()

def plot_statistics_per_pair():
    if not trades_data:
        messagebox.showwarning("No data", "No trades available!")
        return
    
    for pair, trades in trades_data.items():
        stats = calculate_statistics(trades)

        plt.figure(figsize=(12, 8))
        plt.suptitle(f"Statistics for {pair}")

        # Win/Loss per pair
        plt.subplot(2, 2, 1)
        plt.bar(["Wins", "Losses"], [stats["wins"], stats["losses"]], color=['green', 'red'])
        plt.title("Wins vs Losses")

        # Confluences
        plt.subplot(2, 2, 2)
        all_confs = list(set(stats["confluence_wins"].keys()).union(stats["confluence_losses"].keys()))
        wins_c = [stats["confluence_wins"].get(c, 0) for c in all_confs]
        losses_c = [stats["confluence_losses"].get(c, 0) for c in all_confs]
        bar_width = 0.35
        x = range(len(all_confs))
        plt.bar(x, wins_c, width=bar_width, color='green', label='Wins')
        plt.bar([i + bar_width for i in x], losses_c, width=bar_width, color='red', label='Losses')
        plt.xticks([i + bar_width/2 for i in x], all_confs, rotation=45)
        plt.title("Confluences")
        plt.legend()

        # Map colors
        plt.subplot(2, 2, 3)
        all_maps = list(set(stats["map_wins"].keys()).union(stats["map_losses"].keys()))
        map_win_counts = [stats["map_wins"].get(m, 0) for m in all_maps]
        map_loss_counts = [stats["map_losses"].get(m, 0) for m in all_maps]
        x = range(len(all_maps))
        plt.bar(x, map_win_counts, width=bar_width, color='green', label='Wins')
        plt.bar([i + bar_width for i in x], map_loss_counts, width=bar_width, color='red', label='Losses')
        plt.xticks([i + bar_width/2 for i in x], all_maps)
        plt.title("Map Colors")
        plt.legend()

        # Bias info as text
        plt.subplot(2, 2, 4)
        plt.bar(["Bias Correct", "Bias Incorrect"], [stats["bias_correct"], stats["bias_incorrect"]], color=['blue', 'orange'])
        plt.title("Bias Followed vs Not Followed")

        plt.tight_layout(rect=[0, 0, 1, 0.95])  # space for title
        plt.show()

def reset_data():
    global trades_data
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all data?"):
        trades_data = {}
        save_data()
        update_pair_list()
        messagebox.showinfo("Success", "All data has been deleted!")

def view_trades_gui():
    selected_pair = pair_var.get()
    if not selected_pair:
        messagebox.showwarning("Error", "Select a pair!")
        return

    trades = trades_data.get(selected_pair, [])
    if not trades:
        messagebox.showwarning("No data", "No trades available for this pair!")
        return

    view_window = tk.Toplevel(root)
    view_window.title(f"Trades for {selected_pair}")

    for i, trade in enumerate(trades):
        trade_str = f"Trade {i+1}: Result: {trade['result']}, Confluences: {', '.join(trade['confluences'])}, Bias followed: {'Yes' if trade['bias_followed'] else 'No'}, Map color: {trade['map_color']}"
        tk.Label(view_window, text=trade_str).pack()

        def delete_trade(index=i):
            del trades_data[selected_pair][index]
            save_data()
            view_window.destroy()
            view_trades_gui()
        
        tk.Button(view_window, text="Delete", command=delete_trade).pack()

def refresh_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# GUI setup
load_data()
root = tk.Tk()
root.title("Trade Logger")

# Pair selection
pair_frame = tk.Frame(root)
pair_frame.pack(pady=10)

tk.Label(pair_frame, text="Select Pair:").pack(side=tk.LEFT)
pair_var = tk.StringVar()
pair_dropdown = ttk.Combobox(pair_frame, textvariable=pair_var, values=list(trades_data.keys()))
pair_dropdown.pack(side=tk.LEFT, padx=5)

def update_pair_list():
    pair_dropdown['values'] = list(trades_data.keys())

# Add pair button
tk.Button(root, text="Add Pair", command=add_pair_gui).pack()

# Add trade form
trade_frame = tk.Frame(root)
trade_frame.pack(pady=10)

tk.Label(trade_frame, text="Result (win/loss):").grid(row=0, column=0, sticky='w')
result_var = tk.StringVar(value="win")
ttk.Combobox(trade_frame, textvariable=result_var, values=["win", "loss"]).grid(row=0, column=1)

tk.Label(trade_frame, text="Confluences (comma separated):").grid(row=1, column=0, sticky='w')
conf_entry = tk.Entry(trade_frame, width=30)
conf_entry.grid(row=1, column=1)

tk.Label(trade_frame, text="Bias followed?").grid(row=2, column=0, sticky='w')
bias_var = tk.StringVar(value="Yes")
ttk.Combobox(trade_frame, textvariable=bias_var, values=["Yes", "No"]).grid(row=2, column=1)

tk.Label(trade_frame, text="Map color:").grid(row=3, column=0, sticky='w')
map_var = tk.StringVar(value="none")
ttk.Combobox(trade_frame, textvariable=map_var, values=["red", "orange", "gray", "none"]).grid(row=3, column=1)

tk.Button(root, text="Add Trade", command=add_trade_gui).pack(pady=5)

# Add a dropdown menu to select a specific pair for statistics
tk.Label(root, text="Select Pair for Statistics:").pack()
stats_pair_var = tk.StringVar()
stats_pair_dropdown = ttk.Combobox(root, textvariable=stats_pair_var, values=["All"] + list(trades_data.keys()))
stats_pair_dropdown.pack(pady=5)

# Statistics button
tk.Button(root, text="Show Statistics", command=plot_statistics).pack(pady=10)

# View trades button
tk.Button(root, text="View Trades", command=view_trades_gui).pack(pady=10)

# Refresh button
tk.Button(root, text="Refresh", command=refresh_program).pack(pady=10)

# Reset button
tk.Button(root, text="Reset Data", command=reset_data, bg="red", fg="white").pack(pady=10)

update_pair_list()
root.mainloop()
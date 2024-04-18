# 1. select folder to process file
# 2. process file
# 3. completion message
# 4. open folder

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sys
import io
from task_token import token_mainfile
from task_response_leads import task_response_leads

def run_process(folder_path, selected_process):
    if selected_process == "Token":
        output_stream = io.StringIO()
        sys.stdout = output_stream
        token_mainfile.main(folder_path)
        output = output_stream.getvalue()
        sys.stdout = sys.__stdout__
        output_text.insert(tk.END, output)
    elif selected_process == "Response Leads":
        output_stream = io.StringIO()
        sys.stdout = output_stream
        task_response_leads.main(folder_path)
        output = output_stream.getvalue()
        sys.stdout = sys.__stdout__
        output_text.insert(tk.END, output)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_text.insert(tk.END, f"Selected folder: {folder_path}\n")
        selected_process = process_var.get()
        run_process(folder_path, selected_process)

root = tk.Tk()
root.title("Task Simplifier")
root.geometry("600x400")
root.config(bg="#121212")

# Create a style to customize the dropdown menu
style = ttk.Style()
style.configure('Custom.TCombobox', width=10)

# Create a frame for widgets
frame = tk.Frame(root, bg="#121212")
frame.pack(padx=10, pady=10, fill=tk.X)

# Create the dropdown menu
process_var = tk.StringVar()
processes = ["Token", "Response Leads"]
process_dropdown = ttk.Combobox(frame, textvariable=process_var, values=processes, style='Custom.TCombobox')
process_dropdown.pack(side=tk.LEFT, padx=(0, 5))

# Create the select folder button
select_button = tk.Button(frame, text="Browse", command=select_folder)
select_button.pack(side=tk.RIGHT)

# Output text
output_text = tk.Text(root, height=20, width=70, bg="#212121", fg="#FFFFFF")
output_text.pack(padx=10, pady=10)

root.mainloop()
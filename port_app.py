# 1. select folder to process file
# 2. process file
# 3. completion message
# 4. open folder

# import python module
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sys
import io

# import .py file
from task_token import token_mainfile
from task_response_leads import task_response_leads
from task_onetimeconversion import task_tm_ot_conv_to_pledge
from task_burnt import task_tm_burnt
from task_onhold import task_on_hold_hrsr
from task_reactivation import task_reactivation_main
from task_upgrade import task_upgrade
from task_winbackonhold import task_winback_onhold
from task_winback_nofirstpayment import task_winbacknfp

def run_process(folder_path, selected_process):
    process_function = {
        "Token" : token_mainfile.main, 
        "Response Leads" : task_response_leads.main, 
        "One Time Conversion To Pledge" : task_tm_ot_conv_to_pledge.main,
        "Burnt" : task_tm_burnt.main, 
        "On Hold" : task_on_hold_hrsr.main,
        "Reactivation": task_reactivation_main.main,
        "Upgrade" : task_upgrade.main, 
        "Winback On Hold" : task_winback_onhold.main, 
        "Winback No First Payment" : task_winbacknfp.main

    }

    if selected_process in process_function:
        output_stream = io.StringIO()
        sys.stdout = output_stream
        process_function[selected_process](folder_path)
        output = output_stream.getvalue()
        sys.stdout = sys.__stdout__
        output_text.insert(tk.END, output)
    else:
        print("Selected process not found.")



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
processes = ["Token", "Response Leads","One Time Conversion To Pledge", "Burnt", "On Hold", "Reactivation"
             "Winback On Hold", "Upgrade", "Winback No First Payment"]

# Get max length for dropdown by using max for dropdown text
max_text_length = max(len(process) for process in processes)

process_dropdown = ttk.Combobox(frame, textvariable=process_var, values=processes, style='Custom.TCombobox', width=max_text_length)
process_dropdown.pack(side=tk.LEFT, padx=(0, 5))

# Create the select folder button
select_button = tk.Button(frame, text="Browse", command=select_folder)
select_button.pack(side=tk.RIGHT)

# Output text
output_text = tk.Text(root, height=20, width=70, bg="#212121", fg="#FFFFFF")
output_text.pack(padx=10, pady=10)

root.mainloop()
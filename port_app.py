# 1. select folder to process file
# 2. process file
# 3. completion message
# 4. open folder

# import module
from task_token import token_mainfile
from task_response_leads import task_response_leads
import tkinter as tk
import sys
import io
from tkinter import filedialog
from tkinter import ttk


# functions

def run_process(folder_path, selected_process):

    if selected_process == "Token":
        # Redirect stdout to a StringIO object
        output_stream = io.StringIO()
        sys.stdout = output_stream
        
        # Call the main function
        token_mainfile.main(folder_path)
        
        # Get the output from the StringIO object
        output = output_stream.getvalue()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Insert the output into the Text widget
        output_text.insert(tk.END, output)

    elif selected_process == "Response Leads":

        # Redirect stdout to a StringIO object
        output_stream = io.StringIO()
        sys.stdout = output_stream
        
        # Call the main function
        task_response_leads.main(folder_path)
        
        # Get the output from the StringIO object
        output = output_stream.getvalue()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Insert the output into the Text widget
        output_text.insert(tk.END, output)


def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_text.insert(tk.END, f"Selected folder: {folder_path}\n")
        selected_process = process_var.get()
        run_process(folder_path, selected_process)

# tkinter code
root = tk.Tk()
root.title("Simple Tkinter Example")
root.geometry("600x400")

# color scheme
background_color = "#121212"
text_bg_color = "#212121"
text_fg_color = "#FFFFFF"

root.config(bg=background_color)

# create a dropdown menu
process_var = tk.StringVar()
processes = ["Token", "Response Leads"]
process_dropdown = ttk.Combobox(root, textvariable=process_var, values=processes)
process_dropdown.pack(pady=10)
process_dropdown.current(0)

# create select folder button
select_button2 = tk.Button(root, text="Browse", command=select_folder)
select_button2.pack()

# output text
output_text = tk.Text(root, height=10, width=70, bg=text_bg_color, fg=text_fg_color)
output_text.pack(side=tk.BOTTOM, padx=10, pady=10)

root.mainloop()
import tkinter as tk

def say_hello():
    label.config(text="Hello, " + entry.get())

root = tk.Tk()
root.title("Simple Tkinter App")

label = tk.Label(root, text="Enter your name:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Say Hello", command=say_hello)
button.pack()

root.mainloop()
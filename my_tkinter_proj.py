import os
from tkinter import *
from tkinter import ttk

# Global variable to keep track of root node ID
root_node_id = None

# Function to populate left Treeview (directories)
def populate_treeview(path):
    global tree_dirs
    tree_dirs.delete(*tree_dirs.get_children())  # Clear directory tree
    root_node = tree_dirs.insert('', 'end', text=path, open=True)
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for d in dirs:
        tree_dirs.insert(root_node, 'end', text=d)
    return root_node

# Function to populate right TreeView (files)
def populate_fileview(path):
    tree_files.delete(*tree_files.get_children())  # Clear file list
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for f in files:
            tree_files.insert('', 'end', text=f)
    except Exception as e:
        print(f"Error reading files: {e}")

# 'Go' button logic
def go(path):
    global root_node_id
    if os.path.isdir(path):
        root_node_id = populate_treeview(path)
        populate_fileview(path)

# On selecting a directory from the left tree
def on_tree_item_click(event):
    global root_node_id
    selected_item = tree_dirs.selection()
    if selected_item:
        item_text = tree_dirs.item(selected_item)['text']
        cwd = tree_dirs.item(root_node_id)['text']
        full_path = os.path.join(cwd, item_text)
        entry.delete(0, END)
        entry.insert(0, full_path)
        populate_fileview(full_path)

def on_tree_double_click(event):
    item_id = tree_dirs.identify_row(event.y)
    if item_id:
        item_text = tree_dirs.item(item_id, 'text')
        cwd = tree_dirs.item(root_node_id, 'text')
        full_path = os.path.join(cwd, item_text)
        entry.delete(0, END)
        entry.insert(0, full_path)
        go(full_path)

def on_backspace(event):
    current_path = entry.get()
    parent_path = os.path.dirname(current_path)
    if os.path.isdir(parent_path):
        entry.delete(0, END)
        entry.insert(0, parent_path)
        go(parent_path)
    # Prevent default backspace behavior in Entry
    return 'break'

# Create window
root = Tk()
root.title('Directory & File Viewer')
root.geometry('800x500')

# Frame for entry and button
frame = Frame(root)
frame.pack(fill=X, padx=10, pady=10)

label = Label(frame, text="Dir: ")
label.pack(side=LEFT)

cwd = os.getcwd()
entry = Entry(frame)
entry.insert(0, cwd)
entry.pack(side=LEFT, fill=X, expand=True)

button = Button(frame, text="Go", command=lambda: go(entry.get()))
button.pack(side=LEFT, padx=5)

# Middle Frame with two TreeViews
middle_frame = Frame(root)
middle_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Left Treeview for directories
tree_dirs = ttk.Treeview(middle_frame)
tree_dirs.pack(side=LEFT, fill=BOTH, expand=TRUE)
tree_dirs.heading('#0', text='Directories', anchor='w')

# Right Treeview for files
tree_files = ttk.Treeview(middle_frame)
tree_files.pack(side=LEFT, fill=BOTH, expand=True)
tree_files.heading('#0', text='Files', anchor='w')

# Initial population
root_node_id = populate_treeview(cwd)
populate_fileview(cwd)

# Bind events
tree_dirs.bind('<<TreeviewSelect>>', on_tree_item_click)
tree_dirs.bind('<Double-1>', on_tree_double_click)
tree_dirs.bind('<BackSpace>', on_backspace)
entry.bind('<Return>', lambda event: go(entry.get()))
entry.bind('<BackSpace>', on_backspace)

# Run GUI
root.mainloop()
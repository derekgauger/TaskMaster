import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox
import re

# GLOBAL COLOR CODES
DARK_BLUE = "#051f66"
DARK_GRAY = "#050101"
GREEN = "#20bd08"

# Data class for items in the list
class ListItem:
    def __init__(self, item, is_completed=False):
        self.item = item
        self.is_completed = is_completed

# ----------------------------------------------------------------
# Adds an item to the listbox and the saved_items
# ----------------------------------------------------------------
def add_item(event=None):
    item = entry.get()
    if item.strip() != "":
        listbox.insert(tk.END, item)
        saved_items.append(ListItem(item))
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Empty Input", "Please enter an item.")

# ----------------------------------------------------------------
# Deletes the selected items from the listbox
# ----------------------------------------------------------------
def delete_item(event=None):
    selected_indices = listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            saved_items.pop(index)
            listbox.delete(index)
            # If backspace is the method of deletion, set the focus to the previous index (delete upward)
            if event.keysym == "BackSpace":
                listbox.selection_set(index - 1)
            # If delete is the method of deletion, set the focus to the next index (delete downward)
            if event.keysym == "Delete":
                listbox.selection_set(index)
    else:
        messagebox.showwarning("No Selection", "Please select an item to delete.")

# ----------------------------------------------------------------
# Toggle if the selected items are completed
# ----------------------------------------------------------------
def toggle_completed(event=None):
    selected_indices = listbox.curselection()
    if selected_indices:
        for index in selected_indices:
            current_list_item = saved_items[index]
            # Toggle completed
            current_list_item.is_completed = not current_list_item.is_completed
            # Set the color of the item
            if dark_mode:
                listbox.itemconfig(index, bg="gray25" if not current_list_item.is_completed else GREEN)
            else:
                listbox.itemconfig(index, bg="white" if not current_list_item.is_completed else GREEN)
    else:
        messagebox.showwarning("No Selection", "Please select an item to toggle check/uncheck.")

# ----------------------------------------------------------------
# Edit the selected item. If multiple items are selected, edit the first selected item.
# ----------------------------------------------------------------
def on_double_click(event):
    selected_indices = listbox.curselection()
    if selected_indices:
        index = selected_indices[0]
        item = listbox.get(index)
        # Configure the editing window
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Item")
        edit_window.geometry("800x100")
        # Configure the textbox for editing
        edit_entry = tk.Entry(edit_window, font=("Arial", 12))
        edit_entry.insert(0, item)
        edit_entry.pack(pady=10, padx=20, fill=tk.X, expand=True)
        edit_entry.focus_set()
        # ----------------------------------------------------------------
        # Save the edit to the saved items and listbox
        # ----------------------------------------------------------------
        def save_edit(event=None):  # Modified to accept event argument
            new_text = edit_entry.get()
            if new_text.strip() != "":
                listbox.delete(index)
                listbox.insert(index, new_text)
                saved_items[index].item = new_text
            edit_window.destroy()
        # Configure the save button
        save_button = tk.Button(edit_window, text="Save", font=("Arial", 12), command=save_edit)
        save_button.pack(pady=5)
        # Bind Return key to save_edit function
        edit_entry.bind("<Return>", save_edit)

# ----------------------------------------------------------------
# Clear the saved items and listbox
# ----------------------------------------------------------------
def clear_list():
    global saved_items
    listbox.delete(0, tk.END)
    saved_items = []

# ----------------------------------------------------------------
# Apply darkmode to the GUI
# ----------------------------------------------------------------
def apply_dark_mode():
    global dark_mode
    dark_mode = True
    root.config(bg="gray15")
    listbox.config(bg="gray25", fg="white")
    entry.config(bg="gray25", fg="white")
    add_button.config(bg=DARK_BLUE, fg="white")
    delete_button.config(bg=DARK_BLUE, fg="white")
    toggle_button.config(bg=DARK_BLUE, fg="white")
    scrollbar.config(bg=DARK_GRAY)
    input_frame.config(bg=DARK_GRAY)
    listbox_frame.config(bg=DARK_GRAY)
    # Set the color of the list items
    for i, item in enumerate(saved_items):
        if item.is_completed:
            listbox.itemconfig(i, bg=GREEN)
        else:
            listbox.itemconfig(i, bg="gray25")

# ----------------------------------------------------------------
# Apply light mode to the GUI
# ----------------------------------------------------------------
def apply_light_mode():
    global dark_mode
    dark_mode = False
    root.config(bg="white")
    listbox.config(bg="white", fg="black")
    entry.config(bg="white", fg="black", insertbackground="black")
    add_button.config(bg="white", fg="black")
    delete_button.config(bg="white", fg="black")
    toggle_button.config(bg="white", fg="black")
    scrollbar.config(bg="white")
    input_frame.config(bg="white")
    listbox_frame.config(bg='lightgray')
    # Set the color of the list items
    for i, item in enumerate(saved_items):
        if item.is_completed:
            listbox.itemconfig(i, bg=GREEN)
        else:
            listbox.itemconfig(i, bg="white")

# ----------------------------------------------------------------
# Import lines in a .txt file to the GUI
# NOTE: Completed/incomplete statuses are ignored
# ----------------------------------------------------------------
def import_items():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                items = file.read().splitlines()
                for item in items:
                    saved_items.append(ListItem(item))
                    listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import from file:\n{e}")

# ----------------------------------------------------------------
# Export the items to a .txt file
# NOTE: Completed/incomplete statuses are ignored
# ----------------------------------------------------------------
def export_items():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                items = listbox.get(0, tk.END)
                for item in items:
                    file.write(item + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to file:\n{e}")

# ----------------------------------------------------------------
# Save the memory to the .txt file
# NOTE: Completed/incomplete statuses are included
# ----------------------------------------------------------------
def save_memory():
    mem_directory = os.path.dirname(get_exe_location())
    memory_location = mem_directory + "/memory.txt"
    with open(memory_location, "w") as memory_file:
        for item in saved_items:
            print(item.item)
            memory_file.write("{},{}\n".format(item.item, item.is_completed))

# ----------------------------------------------------------------
# Method for closing the application. Save memory, close window
# ----------------------------------------------------------------
def on_close():
    save_memory()
    root.quit()

# ----------------------------------------------------------------
# Get the memory from the memory.txt file.
# Save the statuses and items to the save_items list and add them to the listbox
# ----------------------------------------------------------------
def get_memory():
    mem_directory = os.path.dirname(get_exe_location())
    memory_location = mem_directory + "/memory.txt"
    if os.path.exists(memory_location):
        with open(memory_location, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                # Strip the line of newline characters
                line = line.replace("\n", "")
                # Make the capture groups for the data. (item, is_completed)
                match = re.search(r'(.*),(False|True)', line)
                if match:
                    # Parse the capture groups
                    item = match.groups()[0]
                    is_completed = match.groups()[1]
                    listbox.insert(tk.END, item)
                    # Set the listbox item to completed or not based on the parsed status
                    if "True" in is_completed:
                        is_completed = True
                        listbox.itemconfig(i, bg=GREEN)
                    else:
                        is_completed = False
                    # Update saved_items
                    saved_items.append(ListItem(item, is_completed))
                else:
                    raise Exception("Currupted line in memory file at Line {} - {}".format(i, line))


def get_exe_location():
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller runtime, return the path to the .exe file
        return sys.executable
    else:
        # Regular Python runtime, return the current script's directory
        return os.path.abspath(os.path.dirname(__file__))


# ----------------------------------------------------------------
# Clear all the entries (with many checks)
# ----------------------------------------------------------------
def clear_all():
    global saved_items
    mem_directory = os.path.dirname(get_exe_location())
    memory_location = mem_directory + "/memory.txt"
    if os.path.exists(memory_location):
        result = messagebox.askyesno("Confirmation", "Are you really sure you want to clear memory and list info?")
        if result:
            result2 = messagebox.askyesno("Confirmation", "This will delete all progress you have...")
            if result2:
                os.remove(memory_location)
                clear_list()

# Initialize the main application window
root = tk.Tk()
root.title("Task Master")
root.geometry("1000x500")  # Set the window size to 500x400 pixels

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Clear List", command=clear_list)
file_menu.add_command(label="Clear All", command=clear_all)
file_menu.add_separator()
file_menu.add_command(label="Import", command=import_items)
file_menu.add_command(label="Export", command=export_items)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_close)
# Create View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Dark Mode", command=apply_dark_mode)
view_menu.add_command(label="Light Mode", command=apply_light_mode)

# Create the listbox with scrollbar
listbox_frame = tk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED, activestyle="none", font=("Arial", 14))
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the saved items list and initialize it with the memory.txt data 1 second after the GUI is loaded
saved_items = []
root.after(1000, get_memory)

# Create the input text box and buttons
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.BOTH)
entry = tk.Entry(input_frame, font=("Arial", 14))
add_button = tk.Button(input_frame, text="Add", font=("Arial", 14), command=add_item)
delete_button = tk.Button(input_frame, text="Delete", font=("Arial", 14), command=delete_item)
toggle_button = tk.Button(input_frame, text="Toggle", font=("Arial", 14), command=toggle_completed)

entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
add_button.pack(side=tk.LEFT, padx=10, pady=10)
delete_button.pack(side=tk.LEFT, padx=10, pady=10)
toggle_button.pack(side=tk.LEFT, padx=10, pady=10)

# Bind events to functions
entry.bind("<Return>", add_item)           # Bind Enter key to add_item function
listbox.bind("<Delete>", delete_item)      # Bind Delete key to delete_item function
listbox.bind("<BackSpace>", delete_item)   # Bind Backspace key to delete_item function
listbox.bind("<Return>", toggle_completed)    # Bind Enter key to toggle_check function when listbox has focus
listbox.bind("<Double-Button-1>", on_double_click) # Double-click to edit item

root.protocol("WM_DELETE_WINDOW", on_close) # Window is closed using the red X in the top right corner

# Dark mode variable
dark_mode = True
apply_dark_mode() # Set dark mode by default

root.mainloop()

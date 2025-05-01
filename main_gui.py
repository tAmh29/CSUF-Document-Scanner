import tkinter as tk
from tkinter import filedialog, ttk
import os
from reference_graph import ReferenceGraph

graph = ReferenceGraph() # Initialize the reference graph

""" def create_nodes_for_selected_files():
    # Create node for main file
    main_file = selected_main_file_var.get()
    if main_file:
        graph.add_node(main_file)

    # Create nodes for all secondary files
    selected_indices = secondary_files_listbox.curselection()
    for idx in selected_indices:
        sec_file = secondary_files_listbox.get(idx)
        if sec_file:
            graph.add_node(sec_file) """


def create_nodes_for_selected_files():
    # Create node for main file
    main_file = selected_main_file_var.get()
    if main_file:
        graph.add_node(main_file)

    # Create nodes for all files listed in the tertiary directory listbox
    tertiary_items = tertiary_files_listbox.get(0, tk.END)
    for filename in tertiary_items:
        if filename:
            graph.add_node(filename)



def select_main_file():
    global main_directory
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        main_directory = os.path.dirname(file_path)
        selected_main_file_var.set(os.path.basename(file_path)) # Set the selected file name
        update_file_list(main_files_listbox, main_directory)

def select_secondary_file():
    global secondary_directory
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        secondary_directory = os.path.dirname(file_path)
        selected_secondary_file_var.set(os.path.basename(file_path))
        update_file_list(secondary_files_listbox, secondary_directory)

def sort_files(directory, sort_option):
    files = [f for f in os.listdir(directory) 
    if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.txt')]
    
    if sort_option == "Name":
        return sorted(files)
    elif sort_option == "Date Modified":
        return sorted(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    elif sort_option == "Size":
        return sorted(files, key=lambda f: os.path.getsize(os.path.join(directory, f)))
    return files

def update_file_list(listbox, directory):
    listbox.delete(0, tk.END)
    if directory:
        sort_option = main_sort_dropdown.get() if listbox == main_files_listbox else secondary_sort_dropdown.get()
        files = sort_files(directory, sort_option)
        for filename in files:
            listbox.insert(tk.END, filename)

def on_main_file_double_click(event):
    selected = main_files_listbox.curselection()
    if selected and main_directory:
        filename = main_files_listbox.get(selected[0])
        selected_main_file_var.set(filename)
        file_path = os.path.join(main_directory, filename)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            main_text.delete('1.0', tk.END)
            analysis_text.delete('1.0', tk.END)  # Clear analysis output
            main_text.insert(tk.END, content)
        except Exception as e:
            main_text.delete('1.0', tk.END)
            main_text.insert(tk.END, f"Error reading file:\n{e}")

""" def on_secondary_file_double_click(event):
    selected = secondary_files_listbox.curselection()
    if selected and secondary_directory:
        filename = secondary_files_listbox.get(selected[0])
        selected_secondary_file_var.set(filename)
        file_path = os.path.join(secondary_directory, filename)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, content)
        except Exception as e:
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, f"Error reading file:\n{e}") """

""" def on_secondary_file_double_click(event):
    selected = secondary_files_listbox.curselection()
    if selected and secondary_directory:
        filename = secondary_files_listbox.get(selected[0])
        selected_secondary_file_var.set(filename)
        file_path = os.path.join(secondary_directory, filename)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, content)
        except Exception as e:
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, f"Error reading file:\n{e}")
        
        # --- Append to tertiary field ---
        current_value = selected_tertiary_file_var.get()
        if filename not in current_value.split(', '):  # Avoid duplicate entries
            if current_value:
                new_value = f"{current_value}, {filename}"
            else:
                new_value = filename
            selected_tertiary_file_var.set(new_value) """

def on_secondary_file_double_click(event):
    selected = secondary_files_listbox.curselection()
    if selected and secondary_directory:
        filename = secondary_files_listbox.get(selected[0])
        selected_secondary_file_var.set(filename)
        file_path = os.path.join(secondary_directory, filename)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, content)
        except Exception as e:
            secondary_text.delete('1.0', tk.END)
            secondary_text.insert(tk.END, f"Error reading file:\n{e}")
        
        # --- Add to tertiary listbox if not already present ---
        existing_items = tertiary_files_listbox.get(0, tk.END)
        if filename not in existing_items:
            tertiary_files_listbox.insert(tk.END, filename)


def search_main_substring():
    search_term = search_main_entry.get()
    content = main_text.get('1.0', tk.END)
    start_index = '1.0'
    while True:
        start_index = main_text.search(search_term, start_index, nocase=True, stopindex=tk.END)
        if not start_index:
            break
        end_index = f"{start_index}+{len(search_term)}c"
        main_text.tag_add("highlight", start_index, end_index)
        main_text.tag_config("highlight", background="yellow")
        start_index = end_index

def search_secondary_substring():
    search_term = search_secondary_entry.get()
    content = secondary_text.get('1.0', tk.END)
    start_index = '1.0'
    while True:
        start_index = secondary_text.search(search_term, start_index, nocase=True, stopindex=tk.END)
        if not start_index:
            break
        end_index = f"{start_index}+{len(search_term)}c"
        secondary_text.tag_add("highlight", start_index, end_index)
        secondary_text.tag_config("highlight", background="yellow")
        start_index = end_index

def show_reference_data():
    create_nodes_for_selected_files()

    ref_window = tk.Toplevel(root)
    ref_window.title("Reference Data")
    ref_text = tk.Text(ref_window, height=20, width=60)
    ref_text.pack(padx=10, pady=10)
    ref_text.insert(tk.END, "Reference data goes here...\n")
    for node in graph.nodes.values():
        ref_text.insert(tk.END, f"Document: {node.document_name}\n")

root = tk.Tk()
root.title("CSUF Document Scanner")
root.geometry("800x700")
root.columnconfigure(0, weight=1)

main_directory = None
secondary_directory = None

# Top Frame for file selection and show reference data button
top_frame = tk.Frame(root)
top_frame.pack(pady=10, fill="x")

select_main_btn = tk.Button(top_frame, text="Select Main File", command=select_main_file)
select_main_btn.grid(row=0, column=0, padx=5)

select_secondary_btn = tk.Button(top_frame, text="Select Secondary File", command=select_secondary_file)
select_secondary_btn.grid(row=0, column=1, padx=5)

# "Show Reference Data" Button now placed after the Select Main File and Select Secondary File buttons
reference_button = tk.Button(top_frame, text="Show Reference Data", command=show_reference_data)
reference_button.grid(row=0, column=2, padx=5)

# Variables to hold the selected file names
selected_main_file_var = tk.StringVar()
selected_secondary_file_var = tk.StringVar()

# Create a frame for both Main and Secondary File Directory section
directories_frame = tk.Frame(root)
directories_frame.pack(pady=10, fill="x")

# Main File Directory Frame (Left Side)
main_directory_frame = tk.Frame(directories_frame)
main_directory_frame.grid(row=0, column=0, padx=10, sticky="nsew")

main_directory_label = tk.Label(main_directory_frame, text="Main File Directory:")
main_directory_label.grid(row=0, column=0, sticky="w")

main_sort_options = ["Name", "Date Modified", "Size"]
main_sort_dropdown = ttk.Combobox(main_directory_frame, values=main_sort_options, state="readonly", width=15)
main_sort_dropdown.set("Name")
main_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

main_selected_entry = tk.Entry(main_directory_frame, textvariable=selected_main_file_var, state="readonly", width=40)
main_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

main_files_listbox = tk.Listbox(main_directory_frame, height=5)
main_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
main_files_listbox.bind("<Double-Button-1>", on_main_file_double_click)

main_directory_frame.grid_rowconfigure(1, weight=1)
main_directory_frame.grid_columnconfigure(0, weight=1)

# Secondary File Directory Frame (Right Side)
secondary_directory_frame = tk.Frame(directories_frame)
secondary_directory_frame.grid(row=0, column=1, padx=10, sticky="nsew")

secondary_directory_label = tk.Label(secondary_directory_frame, text="Secondary File Directory:")
secondary_directory_label.grid(row=0, column=0, sticky="w")

secondary_sort_options = ["Name", "Date Modified", "Size"]
secondary_sort_dropdown = ttk.Combobox(secondary_directory_frame, values=secondary_sort_options, state="readonly", width=15)
secondary_sort_dropdown.set("Name")
secondary_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

secondary_selected_entry = tk.Entry(secondary_directory_frame, textvariable=selected_secondary_file_var, state="readonly", width=40)
secondary_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

secondary_files_listbox = tk.Listbox(secondary_directory_frame, height=5)
secondary_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
secondary_files_listbox.bind("<Double-Button-1>", on_secondary_file_double_click)

secondary_directory_frame.grid_rowconfigure(1, weight=1)
secondary_directory_frame.grid_columnconfigure(0, weight=1)

# Tertiary File Directory Frame (Rightmost Side)
tertiary_directory_frame = tk.Frame(directories_frame)
tertiary_directory_frame.grid(row=0, column=2, padx=10, sticky="nsew")

tertiary_directory_label = tk.Label(tertiary_directory_frame, text="Tertiary File Directory:")
tertiary_directory_label.grid(row=0, column=0, sticky="w")

tertiary_sort_options = ["Name", "Date Modified", "Size"]
tertiary_sort_dropdown = ttk.Combobox(tertiary_directory_frame, values=tertiary_sort_options, state="readonly", width=15)
tertiary_sort_dropdown.set("Name")
tertiary_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

selected_tertiary_file_var = tk.StringVar()
tertiary_selected_entry = tk.Entry(tertiary_directory_frame, textvariable=selected_tertiary_file_var, state="readonly", width=40)
tertiary_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

tertiary_files_listbox = tk.Listbox(tertiary_directory_frame, height=5)
tertiary_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
#tertiary_files_listbox.bind("<Double-Button-1>", on_tertiary_file_double_click)

tertiary_directory_frame.grid_rowconfigure(1, weight=1)
tertiary_directory_frame.grid_columnconfigure(0, weight=1)


# Middle Frame for Main File Text and Search
middle_frame = tk.Frame(root)
middle_frame.pack(fill="x", padx=10, pady=10)

main_file_label = tk.Label(middle_frame, text="Main File:")
main_file_label.grid(row=0, column=0, sticky="w")

search_main_entry = tk.Entry(middle_frame, width=30)
search_main_entry.grid(row=0, column=1, sticky="e", padx=10)

search_main_btn = tk.Button(middle_frame, text="Search", command=search_main_substring)
search_main_btn.grid(row=0, column=2, padx=10)

# Main File Text Box
main_text = tk.Text(root, height=10)
main_text.pack(fill="both", padx=10, expand=True)

# **Secondary File Section (Duplicated)**

secondary_file_frame = tk.Frame(root)
secondary_file_frame.pack(fill="x", padx=10)

# Secondary File Label, Search Entry, and Button all on the same level
secondary_file_label = tk.Label(secondary_file_frame, text="Secondary File:")
secondary_file_label.pack(side="left", padx=5)

search_secondary_entry = tk.Entry(secondary_file_frame, width=30)
search_secondary_entry.pack(side="left", padx=5)

search_secondary_btn = tk.Button(secondary_file_frame, text="Search", command=search_secondary_substring)
search_secondary_btn.pack(side="left", padx=5)

""" secondary_file_label = tk.Label(root, text="Secondary File:")
secondary_file_label.pack(anchor="w", padx=10)

# Search bar for Secondary File (same level as the label)
search_secondary_frame = tk.Frame(root)
search_secondary_frame.pack(fill="x", padx=10)

search_secondary_entry = tk.Entry(search_secondary_frame, width=30)
search_secondary_entry.pack(side="left", padx=5)

search_secondary_btn = tk.Button(search_secondary_frame, text="Search", command=search_secondary_substring)
search_secondary_btn.pack(side="left", padx=5) """

# Secondary File Text Box
secondary_text = tk.Text(root, height=10)
secondary_text.pack(fill="both", padx=10, expand=True)

# Analysis Output Label and Text Box
analysis_label = tk.Label(root, text="Analysis Output:")
analysis_label.pack(anchor="w", padx=10, pady=(10, 0))

analysis_text = tk.Text(root, height=8)
analysis_text.pack(fill="both", padx=10, expand=True)

root.mainloop()
import tkinter as tk
from tkinter import filedialog, ttk
import os
from tkinter import messagebox
from reference_graph import ReferenceGraph
from plagarizor import detect_plagiarism, calculate_similarity
from traversal_graph import create_traversal_graph
from Algorithm import bfs, dfs
import sort_helper as sort
import time
import huffman_handler
from reference_graph import build_reference_graph_from_log
from log_handler import PlagiarismLog
from r_graph_visualizer import graphLog
import networkx as nx
import matplotlib.pyplot as plt
from Algorithm.longest_common_subsequence import longest_common_subsequence

graph = ReferenceGraph() # Initialize the reference graph

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

#Creates directories for the neccessary files if they dont already exist
def create_file_directories():

    print(__file__)

    current_directory = os.path.dirname(__file__)
    print(current_directory)

    main_file_directory = os.path.join(current_directory, "mainFiles")
    ref_file_directory = os.path.join(current_directory, "referenceFiles")

    print(main_file_directory)
    print(ref_file_directory)

    # if the mainFileDirectory is not present then create it. 
    if not os.path.exists(main_file_directory):
        os.makedirs(main_file_directory)
        print(f"Directory Created: {main_file_directory}")

    # if the referenceFileDirectory is not present then create it. 
    if not os.path.exists(ref_file_directory):
        os.makedirs(ref_file_directory)
        print(f"Directory Created: {ref_file_directory}")
    
    return (main_file_directory,ref_file_directory)



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

def sort_files_in_listbox(listbox_number,directory):

    if listbox_number == 0:
        sort_key = main_sort_dropdown.get()
        files = list(main_files_listbox.get(0, tk.END))
    if listbox_number == 1:
        sort_key = secondary_sort_dropdown.get()
        files = list(secondary_files_listbox.get(0, tk.END))
    if listbox_number == 2:
        sort_key = tertiary_sort_dropdown.get()
        files = list(tertiary_files_listbox.get(0, tk.END))

    if sort_key == "Name":
        #Calls merge sort for the names of the text files
        files_name_sorted = sort.sort_files(files,"name", directory)
        rewrite_listbox(listbox_number, files_name_sorted)

    elif sort_key == "Author":
        #Calls merge sort for the Authors of the text files
        files_author_sorted = sort.sort_files(files,"author",directory)
        rewrite_listbox(listbox_number, files_author_sorted)

    elif sort_key == "Date":
        #Calls merge sort for the Date of the text files
        files_date_sorted = sort.sort_files(files,"date",directory)
        rewrite_listbox(listbox_number, files_date_sorted)

def rewrite_listbox(listbox_number, sorted_files):

    if listbox_number == 0:
        main_files_listbox.delete(0, tk.END)
        for file in sorted_files:
            main_files_listbox.insert(tk.END, file)

    if listbox_number == 1:
        secondary_files_listbox.delete(0, tk.END)
        for file in sorted_files:
            secondary_files_listbox.insert(tk.END, file)

    if listbox_number == 2:
        tertiary_files_listbox.delete(0, tk.END)
        for file in sorted_files:
            tertiary_files_listbox.insert(tk.END, file)


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
        if isinstance(filename, tuple):
            filename = filename[0]
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

def on_secondary_file_double_click(event):
    selected = secondary_files_listbox.curselection()
    if selected and secondary_directory:
        filename = secondary_files_listbox.get(selected[0])
        if isinstance(filename, tuple):
            filename = filename[0]
        #filename = filename[0]
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

def get_only_filename():


    return

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



## string file containing relative path of log.txt file.
## generally in logOutput\log_m_d_h_min.sec.txt

## NOT IN USE
def draw_from_log(logloc):
    ## See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html for draw options
    DRAW_OPTIONS = {
        'with_labels':True,
        'node_color':'#37eb13',
        'alpha':0.7,
        'style':'dashed'
    }
    

    ## Get log from file
    workingLog = PlagiarismLog()
    workingLog = workingLog.parse_log(logloc)
    print(workingLog.nickname_map)
    print(workingLog.buffer_length)
    print(workingLog.sections)



def show_reference_data():
    create_nodes_for_selected_files()
    log_path = os.path.join(os.path.dirname(__file__), "plagiarism_log.txt")

    ref_window = tk.Toplevel(root)
    ref_window.title("Reference Data")
    ref_text = tk.Text(ref_window, height=20, width=60)
    ref_text.pack(padx=10, pady=10)
    ref_text.insert(tk.END, "Reference data goes here...\n")
    for node in graph.nodes.values():
        ref_text.insert(tk.END, f"Document: {node.document_name}\n")
    

    ##

    # ## See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html for draw options
    # DRAW_OPTIONS = {
    #     'with_labels':True,
    #     'node_color':'#37eb13',
    #     'alpha':0.7,
    #     'style':'dashed'
    # }

    # ref_graph = build_reference_graph_from_log(log_path)
    # ref_graph.display_graph()
    # #graph.add_edge(graph.)
    # graph.add_edge('main_file1.txt','ref_file2.txt',0.5)
    # graph.visualize_graph(**DRAW_OPTIONS)
    # ##

def on_search_method_change(event):
    selected_method = selected_search_method.get()
    if selected_method == "Rabin-Karp":
        print("Rabin-Karp method selected")
    elif selected_method == "KMP":
        print("KMP method selected")
    elif selected_method == "Naive":
        print("Naive method selected")
    else:
        print("Unknown method selected")

def draw_graph(graph_dict):
    G = nx.DiGraph()
    for src, targets in graph_dict.items():
        for tgt in targets:
            G.add_edge(src, tgt)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True, edge_color='gray')
    plt.title("Plagiarism Reference Graph")
    plt.show()

def show_bfs_graph():
    if hasattr(root, "latest_graph_data") and hasattr(root, "latest_bfs_result"):
        graph_data = root.latest_graph_data
        bfs_nodes = root.latest_bfs_result
        subgraph = {}

        for node in bfs_nodes:
            subgraph[node] = [neighbor for neighbor in graph_data.get(node, []) if neighbor in bfs_nodes]

        draw_graph(subgraph)

def show_dfs_graph():
    if hasattr(root, "latest_graph_data") and hasattr(root, "latest_dfs_result"):
        graph_data = root.latest_graph_data
        dfs_nodes = root.latest_dfs_result
        subgraph = {}

        for node in dfs_nodes:
            subgraph[node] = [neighbor for neighbor in graph_data.get(node, []) if neighbor in dfs_nodes]

        draw_graph(subgraph)

def run_lcs_only():
    main_file = selected_main_file_var.get()
    sec_file = selected_secondary_file_var.get()

    if not main_file or not sec_file:
        messagebox.showinfo("LCS Analysis", "Please select both a main file and a secondary file.")
        return

    with open(os.path.join(main_directory, main_file), 'r', encoding='utf-8') as f:
        main_content = f.read()

    with open(os.path.join(secondary_directory, sec_file), 'r', encoding='utf-8') as f:
        reference_content = f.read()

    lcs_str = longest_common_subsequence(reference_content, main_content)
    lcs_len = len(lcs_str)

    analysis_text.insert(tk.END, f"[LCS Only] Length between {main_file} and {sec_file}: {lcs_len}\n")

    output_dir = os.path.join(os.path.dirname(__file__), "lcsOutput")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"lcs_{main_file}_vs_{sec_file}.txt".replace(" ", "_"))

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(lcs_str)

    messagebox.showinfo("LCS Complete", f"LCS written to:\n{out_path}")


def run_plagiarism_analysis():
    main_file = selected_main_file_var.get()
    secondary_files = [secondary_files_listbox.get(i) for i in secondary_files_listbox.curselection()] ## get selected files

    if main_file and secondary_files:
        log = PlagiarismLog()
        log.add_nickname("A", main_file)
        log.set_buffer_length(10)
        with open(os.path.join(main_directory, main_file), 'r') as f:
            main_content = f.read()
        log_path = os.path.join(os.path.dirname(__file__), "plagiarism_log.txt")
        open(log_path, "w").close()

        analysis_text.delete('1.0', tk.END)
        analysis_text.insert(tk.END, "Plagiarism Analysis Results:\n")

        for sec_file in secondary_files:
            log.add_nickname("B", sec_file)
            with open(os.path.join(secondary_directory, sec_file), 'r') as f:
                reference_content = f.read()
            start = time.time()
            matches = detect_plagiarism(reference_content, main_content, method=selected_search_method.get())
            end = time.time()
            analysis_text.insert(tk.END, f"Time taken for {sec_file}: {end - start:.2f} seconds\n")
            if not matches:
                analysis_text.insert(tk.END, f"No plagiarism detected from {sec_file}.\n")
            else:
                analysis_text.insert(tk.END, f"Plagiarism detected from {sec_file}:\n")
                main_text.tag_delete("plag")
                secondary_text.tag_delete("plag_ref")

                # kept outside to keep track of multiple instances
                log = PlagiarismLog()
                log.add_nickname("A", main_file)
                log.add_nickname("B", sec_file)
                log.set_buffer_length(10)
                count= 1
                #

                for match in matches:
                    print(str(match),end="//")
                    start_main = main_content.find(match)
                    if start_main != -1 and main_content[start_main:start_main + len(match)] == match:
                        end_main = start_main + len(match)
                        main_text.tag_add("plag", f"1.0+{start_main}c", f"1.0+{end_main}c")
                        main_text.tag_config("plag", background="red")

                    start_ref = reference_content.find(match)
                    if start_ref != -1 and reference_content[start_ref:start_ref + len(match)] == match:
                        end_ref = start_ref + len(match)
                        secondary_text.tag_add("plag_ref", f"1.0+{start_ref}c", f"1.0+{end_ref}c")
                        secondary_text.tag_config("plag_ref", background="lightblue")
                    print(log.add_reference("A", start_main, "B", start_ref, "B."+ str(count), start_ref, end_ref),end="//") ## print for error checking
                    count += 1
                    
                    # print("Located Contents")
                    # for ref in log.sections["A"]:
                    #     print("!!!!",reference_content[ref["ref_start"]:ref["ref_end"]].replace("\n",""),"!!!!")
                    
                analysis_text.insert(tk.END, "\n")
                ## culling has to be performed before written....
                log.sections["A"] = PlagiarismLog.dedup_dicts(log.sections["A"],"ref_label")
                ##once culled we can graph if desired.
                graphLog(log)
                log.write_log()
                print(log.sections["A"][0])
                ##
            similarity = calculate_similarity(reference_content, main_content)
            analysis_text.insert(tk.END, f"Similarity with {sec_file}: {similarity:.2f}%\n\n")
                
            try:
                log_path = log.write_log()
                graph_data = create_traversal_graph(log_path)
                if "A" in graph_data:
                    bfs_result = bfs.bfs(graph_data, "A")
                    dfs_result = dfs.dfs(graph_data, "A")
                    root.latest_graph_data = graph_data
                    root.latest_bfs_result = bfs_result
                    root.latest_dfs_result = dfs_result
                    analysis_text.insert(tk.END, "\n--- Graph Traversal Results ---\n")
                    analysis_text.insert(tk.END, f"BFS: {' --> '.join(bfs_result)}\n")
                    analysis_text.insert(tk.END, f"DFS: {' --> '.join(dfs_result)}\n")
                    # draw_graph(graph_data)
                else:
                    analysis_text.insert(tk.END, f"\nNo graph traversal data found for: {main_file}\n")
            except FileNotFoundError:
                    analysis_text.insert(tk.END, "\nTraversal graph not available (log file missing).\n")

        analysis_text.insert(tk.END, "Analysis complete.\n")


    

##### Setting Up Directories

main_file_directory, reference_file_directory = create_file_directories()
huffman_output_directory, huffman_codes_output = huffman_handler.create_huffman_directories()



##### Creating GUI
root = tk.Tk()
root.title("CSUF Document Scanner")
root.geometry("800x700")
root.columnconfigure(0, weight=1)

selected_search_method = tk.StringVar()
selected_search_method.set("rabin-karp")

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

search_dropdown = ttk.Combobox(
    top_frame,
    textvariable=selected_search_method,
    values=["Rabin-Karp", "KMP", "Naive"],
    state="readonly",
    width=15
)
search_dropdown.bind("<<ComboboxSelected>>", on_search_method_change)
search_dropdown.grid(row=0, column=3, padx=5)

plagiarism_button = tk.Button(top_frame, text="Run Plagiarism Check", command=run_plagiarism_analysis)
plagiarism_button.grid(row=0, column=4, padx=5)

bfs_button = tk.Button(top_frame, text="Show BFS Graph", command=show_bfs_graph)
bfs_button.grid(row=0, column=5, padx=5)

dfs_button = tk.Button(top_frame, text="Show DFS Graph", command=show_dfs_graph)
dfs_button.grid(row=0, column=6, padx=5)

lcs_only_button = tk.Button(top_frame, text="Run LCS Only", command=run_lcs_only)
lcs_only_button.grid(row=0, column=7, padx=5)

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

main_sort_options = ["Name", "Author", "Date"]
main_sort_dropdown = ttk.Combobox(main_directory_frame, values=main_sort_options, state="readonly", width=15)
main_sort_dropdown.set("Name")
main_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

main_selected_entry = tk.Entry(main_directory_frame, textvariable=selected_main_file_var, state="readonly", width=40)
main_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

main_files_listbox = tk.Listbox(main_directory_frame, height=5)
main_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
main_files_listbox.bind("<Double-Button-1>", on_main_file_double_click)
main_sort_dropdown.bind("<<ComboboxSelected>>", lambda event: sort_files_in_listbox(0,main_directory))

main_directory_frame.grid_rowconfigure(1, weight=1)
main_directory_frame.grid_columnconfigure(0, weight=1)

# Secondary File Directory Frame (Right Side)
secondary_directory_frame = tk.Frame(directories_frame)
secondary_directory_frame.grid(row=0, column=1, padx=10, sticky="nsew")

secondary_directory_label = tk.Label(secondary_directory_frame, text="Secondary File Directory:")
secondary_directory_label.grid(row=0, column=0, sticky="w")

secondary_sort_options = ["Name", "Author", "Date"]
secondary_sort_dropdown = ttk.Combobox(secondary_directory_frame, values=secondary_sort_options, state="readonly", width=15)
secondary_sort_dropdown.set("Name")
secondary_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

secondary_selected_entry = tk.Entry(secondary_directory_frame, textvariable=selected_secondary_file_var, state="readonly", width=40)
secondary_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

secondary_files_listbox = tk.Listbox(secondary_directory_frame, height=5)
secondary_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
secondary_files_listbox.bind("<Double-Button-1>", on_secondary_file_double_click)
secondary_sort_dropdown.bind("<<ComboboxSelected>>", lambda event: sort_files_in_listbox(1,secondary_directory))

secondary_directory_frame.grid_rowconfigure(1, weight=1)
secondary_directory_frame.grid_columnconfigure(0, weight=1)

# Tertiary File Directory Frame (Rightmost Side)
tertiary_directory_frame = tk.Frame(directories_frame)
tertiary_directory_frame.grid(row=0, column=2, padx=10, sticky="nsew")

tertiary_directory_label = tk.Label(tertiary_directory_frame, text="Tertiary File Directory:")
tertiary_directory_label.grid(row=0, column=0, sticky="w")

tertiary_sort_options = ["Name", "Author", "Date"]
tertiary_sort_dropdown = ttk.Combobox(tertiary_directory_frame, values=tertiary_sort_options, state="readonly", width=15)
tertiary_sort_dropdown.set("Name")
tertiary_sort_dropdown.grid(row=0, column=1, padx=5, sticky="e")

selected_tertiary_file_var = tk.StringVar()
tertiary_selected_entry = tk.Entry(tertiary_directory_frame, textvariable=selected_tertiary_file_var, state="readonly", width=40)
tertiary_selected_entry.grid(row=0, column=2, padx=5, sticky="e")

tertiary_files_listbox = tk.Listbox(tertiary_directory_frame, height=5)
tertiary_files_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
#tertiary_sort_dropdown.bind("<<ComboboxSelected>>", lambda event: sort_files_in_listbox(2))

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

# Secondary File Text Box
secondary_text = tk.Text(root, height=10)
secondary_text.pack(fill="both", padx=10, expand=True)

# Analysis Output Label and Text Box
analysis_label = tk.Label(root, text="Analysis Output:")
analysis_label.pack(anchor="w", padx=10, pady=(10, 0))

analysis_text = tk.Text(root, height=8)
analysis_text.pack(fill="both", padx=10, expand=True)

root.mainloop()
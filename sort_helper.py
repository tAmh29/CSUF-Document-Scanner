import merge_sort as merge
import os

def sort_files(file_data, sort_data_type, file_directory):

    sorted_file_list = []

    if(sort_data_type == 'name'):
        sorted_file_list = sort_name(file_data)
        return sorted_file_list
    else:
        unsorted_file_data = read_files_data(file_directory)

    if(sort_data_type == 'author'):
        sorted_file_list = sort_author(unsorted_file_data[0])
        return sorted_file_list
    elif(sort_data_type == 'date'):
        sorted_file_list = sort_filesize(unsorted_file_data[1])
        return sorted_file_list
    else:
        print("Sort Data Type is unavailable or wrong")
        return 'Error'


def sort_name(file_list):

    merge.merge_sort_name(file_list)

    return file_list

def sort_author(file_list):
    file_list = list(file_list.items())
    merge.merge_sort(file_list)
    print(file_list)

    return file_list


def sort_filesize(file_list):
    file_list = list(file_list.items())
    merge.merge_sort(file_list)

    return file_list


##Functions for reading file data
def find_author(file):

    author_name = "Unknown"
    file_lines = file.readlines()

    author_line = file_lines[0]
    if(author_line[0] == '$' and author_line[1] == '!'):
        author_name = author_line[3:]
        author_name = author_name.strip()
        print(author_name)
        return author_name
    else:
        print("No Author Found")
        return author_name

def find_date(file):

    file_date = "Unknown"
    file_lines = file.readlines()

    date_line = file_lines[1]
    if(date_line[0] == '$' and date_line[1] == '%'):
        file_date = date_line[3:]
        file_date = file_date.strip()
        print(f"Publication Date: {file_date}")
        return file_date
    else:
        print("No Publication Date Found")
        return file_date

""" 
def find_filesize(file):

    file_data_size = os.path.getsize(file)
    
    return file_data_size """



def read_file_data(file_name, file_directory):

    file_path = os.path.join(file_directory, file_name)
    file_author = "BadRead"
    file_date = "BadRead"

    try:
        with open(file_path, 'r') as read_file:
            file_author = find_author(read_file)
            read_file.seek(0)  # Rewind the file
            file_date = find_date(read_file)
    except Exception as exception:
        print(f"Error reading file data {exception}")

    return (file_author,file_date)

def create_filename_data_tuple(file_name,file_directory):
    file_author,file_size = read_file_data(file_name,file_directory)
    filename_author_tuple = (file_name, file_author)
    filename_size_tuple = (file_name, file_size)

    return filename_author_tuple, filename_size_tuple

def read_files_data(file_directory):

    all_file_authors = {}
    all_file_sizes = {}
    all_file_data = []

    file_list = os.listdir(file_directory)

    for index, file in enumerate(file_list):
        data_tuples = create_filename_data_tuple(file, file_directory)
        all_file_authors[file] = data_tuples[0][1]
        all_file_sizes[file] = data_tuples[1][1]

    all_file_data.append(all_file_authors)
    all_file_data.append(all_file_sizes)

    print(all_file_data)

    return all_file_data
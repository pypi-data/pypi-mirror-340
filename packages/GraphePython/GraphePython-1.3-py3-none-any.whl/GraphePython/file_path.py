# This part of GraphePython is dedicated to file path handling

# Importing os library to get path
import os

# Main function

def get_file_path(relative_file_path : str, file_name : str) -> str :
    """
    This function is used to get a file absolute path on the user's computer

    Prameters :
    relative_file_path(str) : the path of the file from the script directory
    file_name(str) : the name of the file to get the path to

    Returns :
    final_file_path(str) : the path to the file
    """

    script_path = os.path.dirname(os.path.realpath('__file__'))
    final_file_path = os.path.join(script_path, relative_file_path, file_name)

    return final_file_path
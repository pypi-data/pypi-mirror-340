import os

from jemma.utils.terminalPrettifier import errorText

def spitAllFiles(paths):
    """Recursively list all files in given directories."""
    all_files = []  # Initialize an empty list to store file paths
    for path in paths:
        if os.path.isfile(path) and path[0] != '.':
            all_files.append(os.path.abspath(path))
        elif os.path.isdir(path) and path[0] != '.':
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        if entry.is_file():
                            all_files.append(os.path.abspath(entry.path))
                        elif entry.is_dir():
                            all_files.extend(spitAllFiles([entry.path]))  # Extend the list with results from recursive calls
            except PermissionError:
                print(errorText(f"Permission denied: {path}"))
        else:
            continue
    return all_files  # Return the accumulated list of file paths
 
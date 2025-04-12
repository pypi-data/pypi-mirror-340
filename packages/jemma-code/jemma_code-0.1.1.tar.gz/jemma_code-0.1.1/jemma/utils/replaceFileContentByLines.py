def replace_lines_in_file(file_path, start_line, end_line, new_content):
    """
    Replace content in a file between start_line and end_line (inclusive) with new_content.
    
    Args:
        file_path (str): Path to the file
        start_line (int): Starting line number (1-based index)
        end_line (int): Ending line number (1-based index)
        new_content (str): Content to replace the specified lines with
    """
    # Read all lines from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Validate line indices
    if start_line < 1 or end_line > len(lines) or start_line > end_line:
        raise ValueError("Invalid line range")
    
    # Convert to 0-based indexing
    start_idx = start_line - 1
    end_idx = end_line - 1
    
    # Replace the specified lines with new content
    # Split the new content into lines and ensure each line ends with newline
    new_lines = [line + '\n' if not line.endswith('\n') else line for line in new_content.split('\n')]
    
    # Construct the new file content
    result = lines[:start_idx] + new_lines + lines[end_idx + 1:]
    
    # Write back to the file
    with open(file_path, 'w') as file:
        file.writelines(result)
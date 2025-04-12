import os
from jemma.utils.terminalPrettifier import successText

def get_files_content(directory="."):
    """Get content of relevant files in the project with line numbers."""
    ignored_dirs = {".git", "node_modules", "venv", "env", "build", "dist", "__pycache__",
                   "android", "macos", "ios", "linux", "web", "test", "windows"}
    ignored_extensions = {".pyc", ".pyo", ".pyd", ".so", ".dll", ".class", ".exe", 
                         ".obj", ".o", ".h5", ".csv"}
    
    all_content = ""
    
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if not any(file.endswith(ext) for ext in ignored_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, IOError):
                    # Skip binary files or unreadable files
                    continue
                
                # Format file content with line numbers
                formatted_content = []
                for line_num, line in enumerate(content.splitlines(), 1):
                    formatted_content.append(f"{file_path}:{line_num}: {line}")
                
                # Add formatted content to the result
                all_content += (
                    f"\n\nFile: {file_path}\n"
                    "```\n"
                    f"{'\n'.join(formatted_content)}\n"
                    "```\n"
                )
    
 
    return all_content

 
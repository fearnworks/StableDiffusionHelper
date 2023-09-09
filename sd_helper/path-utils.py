def convert_to_unix_path(win_path: str) -> str:
    # Replace backslashes with forward slashes for Unix compatibility
    unix_path = win_path.replace("\\", "/")
    
    # Enclose the Unix path in double quotes
    unix_path = f'"{unix_path}"'
    
    return unix_path
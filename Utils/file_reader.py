"""
Collection of functions related to reading from local files.
"""

def read_token(token_file_path):
    """
    Reads the token from the specified file's first line.
    """
    return _read_first_line(token_file_path)


def read_admin_id(admin_file_path):
    """
    Reads the bot's admin's ID.
    """
    return int(_read_first_line(admin_file_path))


def _read_first_line(file_path):
    """
    Returns the first line of a file.
    """
    with open(file_path, 'r') as file_:
        first_line = file_.readline().strip()
    return first_line

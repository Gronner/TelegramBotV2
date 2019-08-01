"""
Collection of functions related to reading from local files.
"""

def read_token(token_file_path):
    """
    Reads the token from the specified file's first line.
    """
    with open(token_file_path, 'r') as token_file:
        token = token_file.readline().replace('\n', '')
    return token

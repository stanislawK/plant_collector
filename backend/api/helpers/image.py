import os
from werkzeug.datastructures import FileStorage


def get_extension(file):
    """Return file extension"""
    if isinstance(file, FileStorage):
        filename = file.filename
        ext = os.path.splitext(filename)[1]
        return ext.lower()
    return file

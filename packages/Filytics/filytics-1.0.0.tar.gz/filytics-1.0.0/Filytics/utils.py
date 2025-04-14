import os
from typing import Optional, Dict


def is_hidden(path: str) -> bool:
    """
    Determine if a file or directory is hidden (starts with a dot).
    """
    return os.path.basename(path).startswith('.')


def get_file_extension(filename: str) -> str:
    """
    Extract the file extension.
    If no extension is found, return the entire filename.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The file extension if available; otherwise, the filename.
    """
    root, ext = os.path.splitext(filename)
    # Eğer dosyada uzantı varsa, onu döndür; yoksa dosyanın adını döndür.
    return ext if ext else filename


def file_line_count(file_path: str) -> int:
    """
    Return the number of lines in a file.
    Fail fast by raising an error if the file doesn't exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeDecodeError) as e:
        raise RuntimeError(f"Failed to read lines from {file_path}: {e}")


def get_file_size(file_path: str) -> float:
    """
    Return the file size in megabytes (MB).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError as e:
        raise RuntimeError(f"Failed to get size of {file_path}: {e}")


def get_file_timestamps(file_path: str) -> Dict[str, float]:
    """
    Return creation, modification, and access timestamps of a file.
    Raises if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path not found: {file_path}")

    try:
        stat = os.stat(file_path)
        return {
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime
        }
    except OSError as e:
        raise RuntimeError(f"Failed to retrieve timestamps from {file_path}: {e}")

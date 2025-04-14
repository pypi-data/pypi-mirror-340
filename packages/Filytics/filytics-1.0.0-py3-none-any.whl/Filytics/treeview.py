import os
from colorama import Fore, Style, init

# Initialize colorama for ANSI color support.
init(autoreset=True)


def print_tree(directory: str, prefix: str = "") -> None:
    """
    Print a colored tree view of the given directory.

    Directories are displayed in blue, files in the default color.
    The function uses Unicode characters to represent tree structure.

    Args:
        directory (str): The root directory path.
        prefix (str): The prefix for the current level (used recursively).

    Raises:
        ValueError: If the provided directory does not exist.
    """
    if not os.path.exists(directory):
        raise ValueError(f"Directory '{directory}' does not exist.")

    items = sorted(os.listdir(directory))
    count = len(items)

    for index, item in enumerate(items):
        full_path = os.path.join(directory, item)
        connector = "└── " if index == count - 1 else "├── "
        new_prefix = prefix + "    " if index == count - 1 else prefix + "│   "

        if os.path.isdir(full_path):
            # Display directory names in blue.
            print(f"{prefix}{connector}{Fore.BLUE}{item}{Style.RESET_ALL}")
            # Recursive call for subdirectories.
            print_tree(full_path, new_prefix)
        else:
            # Files without additional color.
            print(f"{prefix}{connector}{item}")


# Optional: if run as main, display tree of current directory.
if __name__ == "__main__":
    directory_to_show = "."
    print_tree(directory_to_show)

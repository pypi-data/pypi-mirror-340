import os
from collections import defaultdict
from . import utils


class FileAnalyzer:
    def __init__(
        self,
        paths: list,
        exclude: list = None,
        exclude_hidden_files: bool = False,
        exclude_hidden_dirs: bool = False,
    ):
        """
        Initialize the FileAnalyzer instance.

        Parameters:
          - paths: List of file or folder paths to analyze.
          - exclude: List of paths to ignore.
          - exclude_hidden_files: If True, hidden files are skipped.
          - exclude_hidden_dirs: If True, hidden directories are skipped.
        """
        self.paths = [os.path.abspath(p) for p in paths]
        self.exclude = set(os.path.abspath(p) for p in (exclude or []))
        self.exclude_hidden_files = exclude_hidden_files
        self.exclude_hidden_dirs = exclude_hidden_dirs

        # Internal state variables to store collected files and folder count.
        self._all_files = []
        self._folder_count = 0

    def _reset_state(self) -> None:
        """
        Reset the internal state before a new analysis.
        """
        self._all_files = []
        self._folder_count = 0

    def collect_files(self) -> list:
        """
        Collect files from the provided paths by applying exclusions.

        Returns:
          A list of absolute file paths.
        """
        # Reset state to ensure fresh collection
        self._reset_state()

        for path in self.paths:
            if not os.path.exists(path):
                # Fail fast approach: skip paths that don't exist.
                continue
            if os.path.isfile(path):
                if path in self.exclude:
                    continue
                if self.exclude_hidden_files and utils.is_hidden(path):
                    continue
                self._all_files.append(path)
            elif os.path.isdir(path):
                self._folder_count += 1  # Count the main folder.
                self._walk_directory(path)
        return self._all_files

    def _walk_directory(self, directory: str) -> None:
        """
        Recursively traverse the given directory applying exclude rules.

        Parameters:
          - directory: The directory path to walk.
        """
        for root, dirs, files in os.walk(directory):
            # Apply hidden directory exclusion
            if self.exclude_hidden_dirs:
                dirs[:] = [d for d in dirs if not utils.is_hidden(d)]
            for file in files:
                full_path = os.path.join(root, file)
                if full_path in self.exclude:
                    continue
                if self.exclude_hidden_files and utils.is_hidden(file):
                    continue
                self._all_files.append(full_path)
            # Increase folder count by the number of subdirectories in current root.
            self._folder_count += len(dirs)

    def analyze(self) -> dict:
        """
        Analyze collected files and return a dictionary with the following keys:
          - folder_count: Total number of folders found.
          - file_count: Total number of files analyzed.
          - total_lines: Sum of all lines across the files.
          - total_size: Sum of file sizes in megabytes (MB).
          - extensions: Dictionary with extension stats (count, lines, size, percentages).

        Returns:
          A dictionary with overall analysis results.
        """
        # Prepare the result container.
        analysis_result = {
            "folder_count": self._folder_count,
            "file_count": 0,
            "total_lines": 0,
            "total_size": 0.0,
            "extensions": {},
        }

        ext_stats = defaultdict(lambda: {"count": 0, "lines": 0, "size": 0.0})

        # Collect files before analysis
        self.collect_files()

        for file in self._all_files:
            analysis_result["file_count"] += 1
            lines = utils.file_line_count(file)
            size = utils.get_file_size(file)

            analysis_result["total_lines"] += lines
            analysis_result["total_size"] += size

            ext = utils.get_file_extension(os.path.basename(file))
            ext_stats[ext]["count"] += 1
            ext_stats[ext]["lines"] += lines
            ext_stats[ext]["size"] += size

        # Calculate percentage statistics for each file extension.
        for ext, stats in ext_stats.items():
            if analysis_result["file_count"] > 0:
                stats["file_percentage"] = (stats["count"] * 100) / analysis_result["file_count"]
            else:
                stats["file_percentage"] = 0
            if analysis_result["total_lines"] > 0:
                stats["line_percentage"] = (stats["lines"] * 100) / analysis_result["total_lines"]
            else:
                stats["line_percentage"] = 0
            if analysis_result["total_size"] > 0:
                stats["size_percentage"] = (stats["size"] * 100) / analysis_result["total_size"]
            else:
                stats["size_percentage"] = 0

        analysis_result["extensions"] = dict(ext_stats)
        return analysis_result

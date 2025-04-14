import json
import csv
from io import StringIO

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# Import and initialize colorama for ANSI color support.
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)


class Reporter:
    def __init__(self, analysis_result: dict):
        """
        Initialize Reporter with the analysis_result dictionary.
        """
        self.result = analysis_result
        # Cache extension statistics for easier access
        self.extensions = self.result.get("extensions", {})

    def _format_stats(self, stats: dict) -> tuple:
        """
        Format statistics for one extension.
        Returns a tuple: (files_str, lines_str, size_str)
        """
        files_str = f"{stats['count']} ({stats['file_percentage']:.2f}%)"
        lines_str = f"{stats['lines']} ({stats['line_percentage']:.2f}%)"
        size_str = f"{stats['size']:.8f} ({stats['size_percentage']:.2f}%)"
        return files_str, lines_str, size_str

    def report_text(self) -> str:
        """Generate plain text report with modern colors using colorama."""
        lines = [
            f"{Fore.GREEN}Folders:{Style.RESET_ALL} {self.result.get('folder_count', 0)}",
            f"{Fore.CYAN}Files:{Style.RESET_ALL} {self.result.get('file_count', 0)}",
            f"{Fore.MAGENTA}Total Lines:{Style.RESET_ALL} {self.result.get('total_lines', 0)}",
            f"{Fore.YELLOW}Total Size:{Style.RESET_ALL} {self.result.get('total_size', 0.0):.8f} MB",
            "",
            f"{Fore.BLUE}Extension Statistics:{Style.RESET_ALL}"
        ]
        for ext, stats in self.extensions.items():
            files_str, lines_str, size_str = self._format_stats(stats)
            # Renkli ekstansiyon ismi ve değerler.
            line = (
                f"{Fore.LIGHTBLUE_EX}{ext}{Style.RESET_ALL}: "
                f"{Fore.GREEN}{files_str}{Style.RESET_ALL} files, "
                f"{Fore.CYAN}{lines_str}{Style.RESET_ALL} lines, "
                f"{Fore.YELLOW}{size_str}{Style.RESET_ALL} MB"
            )
            lines.append(line)
        return "\n".join(lines)

    def report_table(self) -> str:
        """Generate report as a formatted table with color codes in cells."""
        if tabulate is None:
            return self.report_text()
        headers = [
            f"{Fore.LIGHTBLUE_EX}Extension{Style.RESET_ALL}",
            f"{Fore.GREEN}Files (Count & %){Style.RESET_ALL}",
            f"{Fore.CYAN}Lines (Count & %){Style.RESET_ALL}",
            f"{Fore.YELLOW}Size (MB & %){Style.RESET_ALL}"
        ]
        table = []
        for ext, stats in self.extensions.items():
            files_str, lines_str, size_str = self._format_stats(stats)
            table.append([
                f"{Fore.LIGHTBLUE_EX}{ext}{Style.RESET_ALL}",
                f"{Fore.GREEN}{files_str}{Style.RESET_ALL}",
                f"{Fore.CYAN}{lines_str}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{size_str}{Style.RESET_ALL}"
            ])
        return tabulate(table, headers=headers, tablefmt="grid")

    def report_json(self) -> str:
        """Return JSON formatted report."""
        # JSON output is plain text since colors are not applicable.
        return json.dumps(self.result, indent=2)

    def report_csv(self) -> str:
        """Return CSV formatted report."""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Extension", "Files", "File Percentage",
            "Lines", "Line Percentage",
            "Size (MB)", "Size Percentage"
        ])
        for ext, stats in self.extensions.items():
            writer.writerow([
                ext,
                stats.get("count", 0),
                f"{stats.get('file_percentage', 0):.2f}",
                stats.get("lines", 0),
                f"{stats.get('line_percentage', 0):.2f}",
                f"{stats.get('size', 0.0):.8f}",
                f"{stats.get('size_percentage', 0):.2f}"
            ])
        return output.getvalue()

    def report_html(self) -> str:
        """Return HTML formatted report with inline CSS styling for modern looks."""
        html = [
            "<html>",
            "<head>",
            "<title>Filytics Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; }",
            "h1, h2 { color: #2c3e50; }",
            "table { border-collapse: collapse; width: 100%; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #3498db; color: white; }",
            "tr:nth-child(even) { background-color: #f2f2f2; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>Filytics Report</h1>",
            f"<p><strong>Folders:</strong> {self.result.get('folder_count', 0)}</p>",
            f"<p><strong>Files:</strong> {self.result.get('file_count', 0)}</p>",
            f"<p><strong>Total Lines:</strong> {self.result.get('total_lines', 0)}</p>",
            f"<p><strong>Total Size:</strong> {self.result.get('total_size', 0.0):.8f} MB</p>",
            "<h2>Extension Statistics</h2>",
            "<table>",
            "<tr><th>Extension</th><th>Files (Count & %)</th><th>Lines (Count & %)</th><th>Size (MB & %)</th></tr>"
        ]
        for ext, stats in self.extensions.items():
            files_str, lines_str, size_str = self._format_stats(stats)
            html.append(
                f"<tr><td>{ext}</td><td>{files_str}</td><td>{lines_str}</td><td>{size_str}</td></tr>"
            )
        html.extend(["</table>", "</body>", "</html>"])
        return "\n".join(html)

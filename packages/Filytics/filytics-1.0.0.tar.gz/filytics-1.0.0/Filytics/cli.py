#!/usr/bin/env python3
import argparse
import sys
from .analyzer import FileAnalyzer
from .reporter import Reporter


def parse_arguments() -> argparse.Namespace:
    """
    Parse and return command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Filytics - File and Folder Statistics Analyzer CLI"
    )
    parser.add_argument(
        '--path',
        nargs='+',
        default=["."],
        help="File or folder paths to analyze (default is the current directory)"
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=[],
        help="Paths to exclude from analysis"
    )
    parser.add_argument(
        '--exclude-hidden-files',
        action='store_true',
        help="Exclude hidden files"
    )
    parser.add_argument(
        '--exclude-hidden-dirs',
        action='store_true',
        help="Exclude hidden directories"
    )
    parser.add_argument(
        '--output-format',
        choices=['text', 'table', 'json', 'csv', 'html'],
        default='text',
        help="Desired output format"
    )
    parser.add_argument(
        '--sort-by',
        choices=['count', 'lines', 'size'],
        default='count',
        help="Sort extensions by 'count', 'lines', or 'size'"
    )
    parser.add_argument(
        '--desc',
        action='store_true',
        help="Sort in descending order"
    )
    # Yeni: Tree view seçeneği eklendi.
    parser.add_argument(
        '--tree',
        action='store_true',
        help="Display a tree view of the provided paths"
    )
    return parser.parse_args()


def sort_extensions(extensions: dict, sort_key: str, reverse: bool) -> dict:
    """
    Sort extension statistics based on the specified key.
    Returns a new dictionary with sorted items.
    """
    # Using the law of Demeter by accessing only the necessary dict value.
    sorted_ext = dict(
        sorted(
            extensions.items(),
            key=lambda item: item[1].get(sort_key, 0),
            reverse=reverse
        )
    )
    return sorted_ext


def main() -> None:
    """
    Entry point: parse arguments, run analysis, sort extension statistics,
    output using the desired format, and optionally display a tree view.
    """
    args = parse_arguments()

    analyzer = FileAnalyzer(
        paths=args.path,
        exclude=args.exclude,
        exclude_hidden_files=args.exclude_hidden_files,
        exclude_hidden_dirs=args.exclude_hidden_dirs,
    )
    analysis_result = analyzer.analyze()

    # Sort extension statistics as needed.
    analysis_result["extensions"] = sort_extensions(
        analysis_result["extensions"],
        sort_key=args.sort_by,
        reverse=args.desc
    )

    reporter = Reporter(analysis_result)

    output_format = args.output_format.lower()
    if output_format == "text":
        print(reporter.report_text())
    elif output_format == "table":
        print(reporter.report_table())
    elif output_format == "json":
        print(reporter.report_json())
    elif output_format == "csv":
        print(reporter.report_csv())
    elif output_format == "html":
        print(reporter.report_html())
    else:
        # Fail fast for unsupported output formats.
        print("Unsupported output format", file=sys.stderr)
        sys.exit(1)

    # Eğer --tree seçeneği verilmişse, her path için tree görünümünü göster.
    if args.tree:
        # İsteğe bağlı: Analiz raporundan sonra ayrı bir başlık altında tree görünümünü gösterebilirsiniz.
        print("\nDirectory Tree View:")
        # Eğer birden fazla path verilmişse, her biri için ayrı ayrı çalıştırılır.
        from .treeview import print_tree
        for path in args.path:
            print(f"\nTree view for: {path}")
            try:
                print_tree(path)
            except Exception as e:
                print(f"Error displaying tree for {path}: {e}")


if __name__ == "__main__":
    main()

import re
import os
import argparse

def adjust_table_widths(file_path, output_file=None):
    """
    Adjusts table column widths in an AsciiDoc file.
    
    Args:
        file_path (str): Path to the input AsciiDoc file
        output_file (str, optional): Path to the output file. If None, uses input filename with .adoc extension.
    
    Returns:
        str: Path to the output file
    """
    with open(file_path, 'r') as file:
        content = file.read()

    tables = re.findall(r'\|===\n(.*?)\n\|===', content, re.DOTALL)

    for table in tables:
        rows = table.strip().split('\n')
        num_columns = len(rows[0].split('|')) - 1
        column_widths = [0] * num_columns

        for row in rows:
            cells = row.split('|')[1:]
            for i, cell in enumerate(cells):
                if i < num_columns:
                    column_widths[i] = max(column_widths[i], len(cell.strip()))

        total_width = sum(column_widths)
        percentages = [f"{int((width / total_width) * 100)}%" for width in column_widths]
        
        new_cols_attribute = f'[cols="{",".join(percentages)}"]'
        content = content.replace('|===', f'{new_cols_attribute}\n|===', 1)

    if output_file is None:
        output_file = os.path.splitext(file_path)[0] + '.adoc'
    
    with open(output_file, 'w') as file:
        file.write(content)

    print(f"Adjusted table widths saved to: {output_file}")
    return output_file

def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Adjust table column widths in AsciiDoc files based on content"
    )
    parser.add_argument(
        "file_path", 
        help="Path to the AsciiDoc file to process"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to the output file (default: same as input with .adoc extension)"
    )
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=f"%(prog)s {__import__('asciidoc_table_width_adjuster').__version__}"
    )
    
    args = parser.parse_args()
    adjust_table_widths(args.file_path, args.output)

if __name__ == "__main__":
    main()

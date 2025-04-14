# AsciiDoc Table Width Adjuster

A Python utility that automatically adjusts table column widths in AsciiDoc files based on content.

## Description

This tool analyzes tables in AsciiDoc files and automatically calculates appropriate column widths based on the content in each column. It adds a `cols` attribute to each table with percentage-based column widths, making the tables more readable and properly formatted.

## Features

- Automatically detects tables in AsciiDoc files
- Calculates optimal column widths based on content
- Adds percentage-based `cols` attribute to tables
- Preserves the original file content

## Installation
### Install via pip

```bash
pip install column-width
```

## Usage

### Command Line

```bash
# Adjust tables in a specific file
column-width path/to/your/file.adoc

# Get help
column-width --help
```

### As a Python Module

```python
from asciidoc_table_width_adjuster import adjust_table_widths

# Adjust tables in a file
adjust_table_widths('path/to/your/file.adoc')
```

## Example

Input file with a table:
```
|===
|Name |Age |Occupation

|John Smith
|35
|Software Engineer

|Jane Doe
|28
|Data Scientist
|===
```

Output file with adjusted table:
```
[cols="40%,20%,40%"]
|===
|Name |Age |Occupation

|John Smith
|35
|Software Engineer

|Jane Doe
|28
|Data Scientist
|===
```

## License

MIT

## Author

Puneet Bajaj
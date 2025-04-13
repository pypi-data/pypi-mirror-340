# Modular

The code you will see here will be a set of two sorts: 
- utilities to abstract core functionality (e.g., document/object storage) in such a way that said functionality can be referred to in a standardized, serializable way, while handling the implementation-specific stuff (e.g., MongoDB, postgres)--including versioning--as purely config that exists far-removed from the code
- some handy tools crafted in a standardized, serializable way, like the `tables` module below, that will also serve as examples of the approach

Why modular?
- It helps devs write clean, readable, configurable code.
- Actions are easily loggable--something taken for granted in highly asynchronous codebases.
- Because code is inherently configurable, environment management is much simpler.
- You can help avoid lock-in, either because you want to choose the best performing tool for the job and easily switch as needed or because e.g., pricing, license, priorities, or principles of a tool changes.

Use this a dependency injection (DI) framework? Yes and no. But yes.

## History

I brought two of these into my dissertation project, which then became the flagship product of the non-profit I co-founded: the Open Science Framework. These were [`modular-odm`](https://github.com/cos-archives/modular-odm) and [`modular-file renderer`](https://github.com/CenterForOpenScience/modular-file-renderer). The latter is still used today; the former, while used heavily at COS, never reached its full potential. That may now change. The goal was to use abstraction to maximize choice and minimize lock-in.

## Installation

```bash
pip install modular
```

## Features

### Tables Module

The `tables` module provides a flexible system for normalizing and formatting tabular data. It consists of three main components:

1. **Data Normalization** (`normalize_table`): Converts various input formats into a standardized table structure
2. **Format Converters**: Built-in formatters for common output formats
3. **High-level Table Function**: Combines normalization and formatting in one step

#### Supported Formats:
- Delimited (CSV, TSV, etc.)
- Markdown
- reStructuredText
- Custom formats through formatter functions

## Usage

### Basic Usage

The simplest way to create formatted tables is using the `table` function:

```python
from modular.tables import table, markdown, delimited, rst

data = [
    {"name": "Alice", "age": 30, "salary": 50000.123},
    {"name": "Bob", "age": 25, "salary": 60000.456}
]

# Convert to Markdown
md_table = table(data, formatter=markdown)

# Convert to CSV
csv_table = table(data, formatter=delimited)

# Convert to TSV
tsv_table = table(data, formatter=lambda t: delimited(t, delimiter='\t'))

# Convert to reStructuredText
rst_table = table(data, formatter=rst)
```

### Advanced Features

#### Column Ordering

Control the order of columns in the output:

```python
md_table = table(
    data,
    formatter=markdown,
    order=['name', 'city', 'age']
)
```

#### Value Formatting

Apply format strings to specific columns or set a default format for all numeric values:

```python
# Format specific columns
md_table = table(
    data,
    formatter=markdown,
    cell_formats=['{:s}', '{:d}', '${:.2f}']  # string, integer, currency format
)

# Set default number format for all numeric values
md_table = table(
    data,
    formatter=markdown,
    default_number_format='{:.3f}'  # 3 decimal places for all numbers
)

# Combine both
md_table = table(
    data,
    formatter=markdown,
    cell_formats=['{:s}', None, '${:.2f}'],  # Use default_number_format where None
    default_number_format='{:.3f}'
)
```

#### Custom Headers

Specify custom column headers:

```python
data = [
    ['Alice', 30, 50000.123],
    ['Bob', 25, 60000.456]
]

md_table = table(
    data,
    formatter=markdown,
    header=['Name', 'Age', 'Salary']
)
```

#### Custom Formatters

Create your own formatters for custom output formats:

```python
def html_formatter(table):
    if not table['data']:
        return ""
    
    html = "<table>\n"
    # Header row
    html += "  <tr>\n"
    for header in table['header']:
        html += f"    <th>{header}</th>\n"
    html += "  </tr>\n"
    # Data rows
    for row in table['data']:
        html += "  <tr>\n"
        for cell in row:
            html += f"    <td>{cell}</td>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html

html_table = table(data, formatter=html_formatter)
```

### Low-level API

If you need more control, you can use the lower-level functions directly:

```python
from modular.tables import normalize_table, markdown

# First normalize the data
normalized = normalize_table(
    data,
    header=['Name', 'Age', 'Salary'],
    order=['Name', 'Salary', 'Age'],
    cell_formats=['{:s}', '{:d}', '{:.2f}']
)

# Then convert to desired format
md_table = markdown(normalized)
```

## Development

To install the package in development mode:

```bash
git clone https://github.com/yourusername/modular.git
cd modular
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest tests/tables/

# Run specific test file
pytest tests/tables/test_table.py

# Run specific test class
pytest tests/tables/test_table.py::TestBuiltinFormatters
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Modular

A Python package for various data processing utilities with a focus on modularity and choice.

## Installation

```bash
pip install modular
```

## Features

### Tables Module

The `tables` module provides functions to convert data into various table formats.

#### Supported Formats:
- Delimited (CSV, TSV, etc.)
- Markdown
- reStructuredText

## Usage

### Converting Data to Different Formats

```python
from modular.tables import to_delimited, to_markdown, to_rst

# Example data as a list of dictionaries
data_dict = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

# Convert to CSV
csv_output = to_delimited(data_dict)
print(csv_output)

# Convert to TSV
tsv_output = to_delimited(data_dict, delimiter='\t')
print(tsv_output)

# Convert to Markdown
md_output = to_markdown(data_dict)
print(md_output)

# Convert to reStructuredText
rst_output = to_rst(data_dict)
print(rst_output)
```

You can also use lists of lists:

```python
data_list = [
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]

# Convert to any format as shown above
```

## Development

To install the package in development mode:

```bash
git clone https://github.com/yourusername/modular.git
cd modular
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

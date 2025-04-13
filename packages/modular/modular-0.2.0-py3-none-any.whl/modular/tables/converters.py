"""
Table conversion functions for various formats.
"""

from typing import Dict, List, Any
import csv
from io import StringIO

def delimited(table: Dict[str, List], delimiter: str = ',') -> str:
    """
    Convert normalized table data to a delimited string format.
    
    Args:
        table: Dictionary with 'header' and 'data' keys from normalize_table
        delimiter: Character to use as delimiter (default: ',')
        
    Returns:
        String containing the delimited data
    """
    if not table['data']:
        return ""
        
    output = StringIO(newline='')  # Set newline='' to control line endings
    writer = csv.writer(output, delimiter=delimiter, lineterminator='\n')  # Explicitly set line endings
    writer.writerow(table['header'])
    writer.writerows(table['data'])
    return output.getvalue()

def markdown(table: Dict[str, List]) -> str:
    """
    Convert normalized table data to Markdown table format.
    
    Args:
        table: Dictionary with 'header' and 'data' keys from normalize_table
        
    Returns:
        String containing the Markdown table
    """
    if not table['data']:
        return ""
        
    # Create header row
    markdown = "| " + " | ".join(str(h) for h in table['header']) + " |\n"
    # Create separator row
    markdown += "| " + " | ".join(["---"] * len(table['header'])) + " |\n"
    # Add data rows
    for row in table['data']:
        markdown += "| " + " | ".join(str(cell) for cell in row) + " |\n"
    
    return markdown

def rst(table: Dict[str, List]) -> str:
    """
    Convert normalized table data to reStructuredText table format.
    
    Args:
        table: Dictionary with 'header' and 'data' keys from normalize_table
        
    Returns:
        String containing the reStructuredText table
    """
    if not table['data']:
        return ""
        
    # Calculate column widths
    headers = [str(h) for h in table['header']]
    data = [[str(cell) for cell in row] for row in table['data']]
    
    col_widths = [max(len(str(cell)) for cell in col) 
                 for col in zip(headers, *data)]
    
    # Create header row
    rst = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+\n"
    rst += "|" + "|".join(f" {header:<{width}} " for header, width in zip(headers, col_widths)) + "|\n"
    rst += "+" + "+".join("=" * (width + 2) for width in col_widths) + "+\n"
    
    # Add data rows
    for row in data:
        rst += "|" + "|".join(f" {cell:<{width}} " for cell, width in zip(row, col_widths)) + "|\n"
    rst += "+" + "+".join("-" * (width + 2) for width in col_widths) + "+\n"
    
    return rst 
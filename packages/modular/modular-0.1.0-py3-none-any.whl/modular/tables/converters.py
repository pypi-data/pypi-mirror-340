"""
Table conversion functions for various formats.
"""

from typing import Union, List, Dict, Any
import csv
from io import StringIO

def _normalize_data(data: Union[List[List[Any]], List[Dict[str, Any]]]) -> tuple[List[List[str]], List[str]]:
    """
    Normalize input data to a consistent format.
    
    Args:
        data: List of lists or list of dictionaries
        
    Returns:
        Tuple of (rows, headers)
    """
    if not data:
        return [], []
        
    if isinstance(data[0], dict):
        headers = list(data[0].keys())
        rows = [[str(row.get(header, '')) for header in headers] for row in data]
    else:
        rows = [[str(cell) for cell in row] for row in data]
        headers = [f"Column {i+1}" for i in range(len(rows[0]))] if rows else []
    
    return rows, headers

def to_delimited(data: Union[List[List[Any]], List[Dict[str, Any]]], 
                delimiter: str = ',') -> str:
    """
    Convert data to a delimited string format.
    
    Args:
        data: List of lists or list of dictionaries
        delimiter: Character to use as delimiter (default: ',')
        
    Returns:
        String containing the delimited data
    """
    rows, headers = _normalize_data(data)
    output = StringIO()
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()

def to_markdown(data: Union[List[List[Any]], List[Dict[str, Any]]]) -> str:
    """
    Convert data to Markdown table format.
    
    Args:
        data: List of lists or list of dictionaries
        
    Returns:
        String containing the Markdown table
    """
    rows, headers = _normalize_data(data)
    if not rows:
        return ""
        
    # Create header row
    markdown = "| " + " | ".join(headers) + " |\n"
    # Create separator row
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    # Add data rows
    for row in rows:
        markdown += "| " + " | ".join(row) + " |\n"
    
    return markdown

def to_rst(data: Union[List[List[Any]], List[Dict[str, Any]]]) -> str:
    """
    Convert data to reStructuredText table format.
    
    Args:
        data: List of lists or list of dictionaries
        
    Returns:
        String containing the reStructuredText table
    """
    rows, headers = _normalize_data(data)
    if not rows:
        return ""
        
    # Calculate column widths
    col_widths = [max(len(str(cell)) for cell in col) 
                 for col in zip(headers, *rows)]
    
    # Create header row
    rst = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+\n"
    rst += "|" + "|".join(f" {header:<{width}} " for header, width in zip(headers, col_widths)) + "|\n"
    rst += "+" + "+".join("=" * (width + 2) for width in col_widths) + "+\n"
    
    # Add data rows
    for row in rows:
        rst += "|" + "|".join(f" {cell:<{width}} " for cell, width in zip(row, col_widths)) + "|\n"
    rst += "+" + "+".join("-" * (width + 2) for width in col_widths) + "+\n"
    
    return rst 
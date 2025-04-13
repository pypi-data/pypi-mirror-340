from typing import List, Dict, Union, Optional, Any, Callable
import numbers
from .normalize import normalize_table

def table(
    data: Union[List[Dict[str, Any]], List[List[Any]]],
    formatter: Callable[[Dict[str, List]], str],
    header: Optional[List[str]] = None,
    order: Optional[List[str]] = None,
    cell_formats: Optional[List[str]] = None,
    default_number_format: str = "{:.2f}"
) -> str:
    """
    Create a formatted table from input data.
    
    Args:
        data: List of dictionaries or list of lists containing the table data
        formatter: Function that takes a normalized table dict and returns formatted string
        header: Optional list of column names. If None and data is list of dicts,
               will use dict keys as header
        order: Optional list of column names/keys to specify column order
        cell_formats: Optional list of format strings to apply to each column
        default_number_format: Format string to apply to numeric values when no
                             cell_formats specified
    
    Returns:
        String containing the formatted table
    """
    normalized = normalize_table(
        data=data,
        header=header,
        order=order,
        cell_formats=cell_formats,
        default_number_format=default_number_format
    )
    
    return formatter(normalized) 
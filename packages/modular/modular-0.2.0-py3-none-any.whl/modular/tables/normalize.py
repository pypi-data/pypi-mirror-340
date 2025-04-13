from typing import List, Dict, Union, Optional, Any
import numbers

def normalize_table(
    data: Union[List[Dict[str, Any]], List[List[Any]]],
    header: Optional[List[str]] = None,
    order: Optional[List[str]] = None,
    cell_formats: Optional[List[str]] = None,
    default_number_format: str = "{:.2f}"
) -> Dict[str, List]:
    """
    Normalize different data formats into a consistent table structure with formatting options.
    
    Args:
        data: List of dictionaries or list of lists containing the table data
        header: Optional list of column names. If None and data is list of dicts,
               will use dict keys as header
        order: Optional list of column names/keys to specify column order
        cell_formats: Optional list of format strings to apply to each column
        default_number_format: Format string to apply to numeric values when no
                             cell_formats specified
    
    Returns:
        Dictionary with keys:
            'data': List of lists containing the normalized table data
            'header': List of column names
    """
    if not data:
        return {'data': [], 'header': []}
        
    # Handle list of dictionaries
    if isinstance(data[0], dict):
        if header is None:
            # Use keys from first dictionary to establish initial order
            header = list(data[0].keys())
            # Add any additional keys from other dictionaries
            for d in data[1:]:
                for key in d.keys():
                    if key not in header:
                        header.append(key)
        
        # Convert dicts to lists based on header order
        table_data = [
            [row.get(col, '') for col in header]
            for row in data
        ]
            
    # Handle list of lists
    else:
        if header is None:
            # Generate numeric headers
            header = [str(i) for i in range(len(data[0]))]
        table_data = list(data)  # Make a copy to avoid modifying input

    # Apply ordering if specified
    if order:
        # Create mapping of current positions
        current_positions = {h: i for i, h in enumerate(header)}
        
        # Create new header order
        new_header = []
        # First add specified columns in order
        for h in order:
            if h in header:
                new_header.append(h)
        # Then add any remaining columns
        new_header.extend(h for h in header if h not in new_header)
        
        # Create mapping for reordering data
        reorder_indices = [current_positions[h] for h in new_header]
        
        # Reorder the data
        table_data = [
            [row[i] for i in reorder_indices]
            for row in table_data
        ]
        
        header = new_header
            
    # Apply formatting
    if cell_formats or default_number_format != "{:.2f}":  # Apply if cell_formats provided or custom default_number_format
        # Use cell_formats if provided, otherwise use default_number_format for all columns
        formats = cell_formats if cell_formats else [default_number_format] * len(header)
        # Ensure formats matches number of columns
        formats = (formats + [default_number_format] * len(header))[:len(header)]
        
        formatted_data = []
        for row in table_data:
            formatted_row = []
            for value, fmt in zip(row, formats):
                if isinstance(value, numbers.Number):
                    try:
                        formatted_row.append(fmt.format(value))
                    except ValueError:
                        formatted_row.append(default_number_format.format(value))
                else:
                    formatted_row.append(str(value))
            formatted_data.append(formatted_row)
        table_data = formatted_data
            
    return {
        'data': table_data,
        'header': header
    } 
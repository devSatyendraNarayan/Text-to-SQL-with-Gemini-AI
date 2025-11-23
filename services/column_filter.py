"""
Filter sensitive columns from query results
"""

# Patterns for sensitive column names (case-insensitive)
SENSITIVE_PATTERNS = [
    'id',
    'password',
    'pwd',
    'created_by',
    'updated_by',
    'laststatus_by',
    'created_datetime',
    'updated_datetime',
    'laststatus_datetime',
    'controllerid',
    'approverid',
    'designation_id'
]

def filter_sensitive_columns(rows, columns):
    """
    Filter out sensitive columns from query results.
    
    Args:
        rows: List of row tuples from database
        columns: List of column names
        
    Returns:
        Tuple of (filtered_rows, filtered_columns)
    """
    if not rows or not columns:
        return rows, columns
    
    # Find indices of non-sensitive columns
    safe_indices = []
    safe_columns = []
    
    for idx, col in enumerate(columns):
        col_lower = col.lower()
        is_sensitive = any(pattern in col_lower for pattern in SENSITIVE_PATTERNS)
        
        if not is_sensitive:
            safe_indices.append(idx)
            safe_columns.append(col)
    
    # Filter rows to only include safe columns
    filtered_rows = []
    for row in rows:
        filtered_row = tuple(row[idx] for idx in safe_indices)
        filtered_rows.append(filtered_row)
    
    return filtered_rows, safe_columns

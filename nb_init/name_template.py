"""Interface name templating"""

from typing import List, Dict, Any
import re
from itertools import product

def expand_name_template(name_template: str) -> List[str]:
    """Expand a name template into a list of interface names.
    
    Args:
        name_template: Template string like 'Ethernet[27-32]/1', 'Ethernet27/[1-4]', 
                      or 'Ethernet[27-32]/[1-4]'
        
    Returns:
        List of interface names
    """
    result = []
    
    # Find all number ranges in the template
    ranges = re.findall(r'\[([0-9]+)-([0-9]+)\]', name_template)
    
    if not ranges:
        # No ranges found, return the template as-is
        return [name_template]
    
    # Extract the static parts of the template
    # Split by range patterns but keep them for reconstruction
    static_parts = re.split(r'\[[0-9]+-[0-9]+\]', name_template)
    
    # Create all combinations of the ranges
    range_values = [range(int(start), int(end) + 1) for start, end in ranges]
    
    for combination in product(*range_values):
        name_parts = []
        static_idx = 0
        
        for range_start, range_end in ranges:
            # Add the static part before this range
            if static_idx < len(static_parts):
                name_parts.append(static_parts[static_idx])
                static_idx += 1
            
            # Add the range value
            name_parts.append(str(combination[ranges.index((range_start, range_end))]))
        
        # Add remaining static parts
        if static_idx < len(static_parts):
            name_parts.append(static_parts[static_idx])
        
        result.append(''.join(name_parts))
    
    return result

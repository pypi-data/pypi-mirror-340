# Data Formatter Utility
# Formats data for display and reports

import json
import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger("osint_scout.data_formatter")

def format_dict_for_display(data, prefix=''):
    """Format a dictionary for console display
    
    Args:
        data (dict): Dictionary to format
        prefix (str): Prefix for nested keys
        
    Returns:
        list: Formatted list of key-value pairs
    """
    formatted = []
    
    try:
        for key, value in data.items():
            if isinstance(value, dict):
                # Handle nested dictionaries
                nested = format_dict_for_display(value, f"{prefix}{key}.")
                formatted.extend(nested)
            elif isinstance(value, list):
                # Handle lists
                if not value:
                    formatted.append((f"{prefix}{key}", "[]"))
                elif isinstance(value[0], dict):
                    # List of dictionaries
                    for i, item in enumerate(value):
                        nested = format_dict_for_display(item, f"{prefix}{key}[{i}].")
                        formatted.extend(nested)
                else:
                    # List of simple values
                    formatted.append((f"{prefix}{key}", format_list(value)))
            else:
                # Handle simple values
                formatted.append((f"{prefix}{key}", format_value(value)))
                
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting dictionary: {str(e)}")
        return [("error", str(e))]

def format_list(data):
    """Format a list for display
    
    Args:
        data (list): List to format
        
    Returns:
        str: Formatted list
    """
    try:
        if not data:
            return "[]"
            
        if len(data) <= 5:
            return ', '.join(str(item) for item in data)
        else:
            # For long lists, show first 5 items and count
            return f"{', '.join(str(item) for item in data[:5])}... ({len(data)} items)"
            
    except Exception as e:
        logger.error(f"Error formatting list: {str(e)}")
        return str(e)

def format_value(value):
    """Format a value for display
    
    Args:
        value: Value to format
        
    Returns:
        str: Formatted value
    """
    try:
        if value is None:
            return "None"
        elif isinstance(value, bool):
            return "Yes" if value else "No"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return str(value)
            
    except Exception as e:
        logger.error(f"Error formatting value: {str(e)}")
        return str(e)

def format_json_for_report(data):
    """Format JSON data for a report
    
    Args:
        data (dict): Data to format
        
    Returns:
        str: Formatted JSON
    """
    try:
        # Pretty print with indentation
        return json.dumps(data, indent=4, sort_keys=False, default=json_serializer)
        
    except Exception as e:
        logger.error(f"Error formatting JSON: {str(e)}")
        return json.dumps({"error": str(e)})

def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serializable representation
    """
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError(f"Type {type(obj)} not serializable")

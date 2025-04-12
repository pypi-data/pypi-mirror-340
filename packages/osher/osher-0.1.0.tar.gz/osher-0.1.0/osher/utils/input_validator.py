# Input Validator Utility
# Validates user input for various data types

import re
import socket
import logging
import ipaddress

# Initialize logger
logger = logging.getLogger("osint_scout.input_validator")

def is_valid_ip(ip_address):
    """Validates if a string is a valid IP address
    
    Args:
        ip_address (str): The IP address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Use ipaddress module to validate both IPv4 and IPv6
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        logger.warning(f"Invalid IP address format: {ip_address}")
        return False

def is_valid_domain(domain):
    """Validates if a string is a valid domain name
    
    Args:
        domain (str): The domain to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic domain validation regex
        # Checks for valid domain format (e.g., example.com)
        domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        
        if re.match(domain_pattern, domain):
            return True
        
        logger.warning(f"Invalid domain format: {domain}")
        return False
    except Exception as e:
        logger.error(f"Error validating domain: {str(e)}")
        return False

def is_valid_email(email):
    """Validates if a string is a valid email address
    
    Args:
        email (str): The email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Email validation regex
        # Checks for valid email format (e.g., user@example.com)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, email):
            return True
        
        logger.warning(f"Invalid email format: {email}")
        return False
    except Exception as e:
        logger.error(f"Error validating email: {str(e)}")
        return False

def is_valid_username(username):
    """Validates if a string is a valid username
    
    Args:
        username (str): The username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic username validation
        # Allows alphanumeric characters, underscores, hyphens, and periods
        # Minimum length of 1, maximum length of 50
        if len(username) < 1 or len(username) > 50:
            logger.warning(f"Username length invalid: {len(username)}")
            return False
        
        # Check for valid characters
        username_pattern = r'^[a-zA-Z0-9._-]+$'
        
        if re.match(username_pattern, username):
            return True
        
        logger.warning(f"Invalid username format: {username}")
        return False
    except Exception as e:
        logger.error(f"Error validating username: {str(e)}")
        return False

def is_valid_phone(phone_number):
    """Validates if a string is a valid phone number
    
    Args:
        phone_number (str): The phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic phone number validation
        # Requires a + followed by digits, may include spaces, parentheses, or hyphens
        phone_pattern = r'^\+\d[\d\s\(\)-]{7,20}$'
        
        if re.match(phone_pattern, phone_number):
            return True
        
        logger.warning(f"Invalid phone number format: {phone_number}")
        return False
    except Exception as e:
        logger.error(f"Error validating phone number: {str(e)}")
        return False

def is_valid_url(url):
    """Validates if a string is a valid URL
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # URL validation regex
        # Checks for valid URL format (e.g., http://example.com)
        url_pattern = r'^(http|https)://[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})(:[0-9]{1,5})?(/.*)?$'
        
        if re.match(url_pattern, url):
            return True
        
        logger.warning(f"Invalid URL format: {url}")
        return False
    except Exception as e:
        logger.error(f"Error validating URL: {str(e)}")
        return False

def is_valid_file_path(file_path):
    """Validates if a string is a valid file path
    
    Args:
        file_path (str): The file path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic file path validation
        # This is a simple check, more complex validation might be required for certain systems
        if file_path and len(file_path) > 0:
            # Check for invalid characters based on common OS restrictions
            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            if any(char in file_path for char in invalid_chars):
                logger.warning(f"Invalid characters in file path: {file_path}")
                return False
            return True
        
        logger.warning(f"Empty file path")
        return False
    except Exception as e:
        logger.error(f"Error validating file path: {str(e)}")
        return False

def is_valid_api_key(api_key):
    """Validates if a string is a potentially valid API key
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if potentially valid, False otherwise
    """
    try:
        # Simple API key validation
        # Just checks that it's not empty and has a reasonable length
        if api_key and len(api_key) >= 8:
            return True
        
        logger.warning(f"API key is too short or empty")
        return False
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        return False

def sanitize_input(input_str, allowed_chars=None):
    """Sanitizes a string by removing potentially dangerous characters
    
    Args:
        input_str (str): The string to sanitize
        allowed_chars (str, optional): Regex pattern of allowed characters
        
    Returns:
        str: Sanitized string
    """
    try:
        if allowed_chars:
            # Keep only allowed characters
            return re.sub(f'[^{allowed_chars}]', '', input_str)
        else:
            # Default: allow alphanumeric, spaces, and common punctuation
            return re.sub(r'[^\w\s.,;:!?@#$%^&*()-]', '', input_str)
    except Exception as e:
        logger.error(f"Error sanitizing input: {str(e)}")
        return ""

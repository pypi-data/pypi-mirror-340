# Configuration Module
# Contains configuration settings for the OSINT Scout

import os
import logging

# Initialize logger
logger = logging.getLogger("osint_scout.config")

# Get API keys from environment variables with fallbacks to empty strings
API_KEYS = {
    'VIRUSTOTAL_API_KEY': os.getenv('VIRUSTOTAL_API_KEY', ''),
    'IPINFO_TOKEN': os.getenv('IPINFO_TOKEN', ''),
    'HAVEIBEENPWNED_API_KEY': os.getenv('HAVEIBEENPWNED_API_KEY', ''),
    'EMAILREP_API_KEY': os.getenv('EMAILREP_API_KEY', ''),
    'HUNTER_API_KEY': os.getenv('HUNTER_API_KEY', ''),
    'NUMVERIFY_API_KEY': os.getenv('NUMVERIFY_API_KEY', ''),
    'WAPPALYZER_API_KEY': os.getenv('WAPPALYZER_API_KEY', '')
}

# API Configuration
API_CONFIG = {
    # Rate limits for various APIs (requests per minute)
    'RATE_LIMITS': {
        'ipapi.co': 45,  # Free tier limit
        'virustotal.com': 4,  # Public API limit
        'haveibeenpwned.com': 10,
        'emailrep.io': 60,
        'hunter.io': 60,
        'numverify': 60
    },
    
    # Timeouts for various APIs (seconds)
    'TIMEOUTS': {
        'default': 10,
        'virustotal.com': 20,  # VT can be slow
        'haveibeenpwned.com': 15
    }
}

# CLI Configuration
CLI_CONFIG = {
    # Default output format for reports
    'DEFAULT_REPORT_FORMAT': 'html',
    
    # Default visualization settings
    'GENERATE_VISUALIZATION': True,
    
    # Default full scan setting for domains
    'DEFAULT_FULL_SCAN': False
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    # Default figure dimensions
    'FIGURE_WIDTH': 12,
    'FIGURE_HEIGHT': 8,
    
    # Default DPI for saved figures
    'DPI': 300,
    
    # Default color scheme
    'COLOR_SCHEME': 'tab10'
}

# Username check platforms to use
# This is a subset of the full list in username_info.py
DEFAULT_PLATFORMS = [
    "Instagram",
    "Twitter/X",
    "Facebook",
    "GitHub",
    "LinkedIn",
    "Reddit"
]

# Email disposable domains list (partial)
DISPOSABLE_DOMAINS = [
    'temp-mail.org',
    'guerrillamail.com',
    'mailinator.com',
    'tempmail.com',
    'throwawaymail.com',
    '10minutemail.com',
    'yopmail.com',
    'getairmail.com',
    'dispostable.com',
    'maildrop.cc',
    'mailnesia.com',
    'mintemail.com'
]

# Free email providers list (partial)
FREE_EMAIL_PROVIDERS = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'outlook.com',
    'aol.com',
    'icloud.com',
    'protonmail.com',
    'mail.com',
    'zoho.com',
    'yandex.com',
    'gmx.com'
]

# DNS record types to check
DNS_RECORD_TYPES = [
    'A',
    'AAAA',
    'CNAME',
    'MX',
    'TXT',
    'NS',
    'SOA',
    'CAA'
]

# Debug mode setting
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

# Configure logging level based on debug mode
LOGGING_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO

def get_api_timeout(domain):
    """Get timeout for a specific API domain
    
    Args:
        domain (str): API domain
        
    Returns:
        int: Timeout in seconds
    """
    # Extract base domain from URL if needed
    if '://' in domain:
        domain = domain.split('://', 1)[1]
    domain = domain.split('/', 1)[0]
    
    # Check if we have a specific timeout for this domain
    for key, value in API_CONFIG['TIMEOUTS'].items():
        if key in domain:
            return value
    
    # Return default timeout
    return API_CONFIG['TIMEOUTS']['default']

def get_api_rate_limit(domain):
    """Get rate limit for a specific API domain
    
    Args:
        domain (str): API domain
        
    Returns:
        int: Maximum requests per minute
    """
    # Extract base domain from URL if needed
    if '://' in domain:
        domain = domain.split('://', 1)[1]
    domain = domain.split('/', 1)[0]
    
    # Check if we have a specific rate limit for this domain
    for key, value in API_CONFIG['RATE_LIMITS'].items():
        if key in domain:
            return value
    
    # Return a conservative default
    return 30  # 30 requests per minute

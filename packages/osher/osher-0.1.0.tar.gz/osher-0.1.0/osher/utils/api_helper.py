# API Helper Utility
# Handles API requests with retries, rate limiting, and error handling

import os
import requests
import time
import logging
import json
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Initialize logger
logger = logging.getLogger("osint_scout.api_helper")

# Define default retry strategy
DEFAULT_RETRY_STRATEGY = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    backoff_factor=1
)

def create_session():
    """Create a requests session with retry strategy
    
    Returns:
        requests.Session: Session with retry configuration
    """
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=DEFAULT_RETRY_STRATEGY)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def make_request(url, method="GET", headers=None, params=None, data=None, json_data=None, 
                timeout=10, verify=True, allow_redirects=True, session=None):
    """Make an API request with error handling and retries
    
    Args:
        url (str): The URL to request
        method (str, optional): HTTP method to use. Defaults to "GET".
        headers (dict, optional): HTTP headers to include. Defaults to None.
        params (dict, optional): Query parameters. Defaults to None.
        data (dict, optional): Form data to send. Defaults to None.
        json_data (dict, optional): JSON data to send. Defaults to None.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.
        verify (bool, optional): Verify SSL certificates. Defaults to True.
        allow_redirects (bool, optional): Follow redirects. Defaults to True.
        session (requests.Session, optional): Session to use. Defaults to None.
    
    Returns:
        requests.Response or None: Response object or None if request failed
    """
    # Use provided session or create a new one
    session = session or create_session()
    
    # Set default headers if none provided
    if headers is None:
        headers = {
            "User-Agent": "OSINT-Scout/1.0.0",
            "Accept": "application/json"
        }
    
    try:
        logger.debug(f"Making {method} request to {url}")
        
        # Make the request
        response = session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json_data,
            timeout=timeout,
            verify=verify,
            allow_redirects=allow_redirects
        )
        
        # Log the response status
        logger.debug(f"Response status code: {response.status_code}")
        
        # Check if the request was successful
        if response.status_code >= 400:
            logger.warning(f"Request failed with status code {response.status_code}: {url}")
            logger.debug(f"Response content: {response.text[:500]}...")
        
        # Return the response regardless of status code
        # This allows the caller to handle specific status codes
        return response
        
    except requests.exceptions.Timeout:
        logger.error(f"Request timed out: {url}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error: {url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {url} - {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during request: {url} - {str(e)}")
    
    # Return None if request failed
    return None

def make_rate_limited_request(url, rate_limit_per_min=60, **kwargs):
    """Make a rate-limited API request
    
    Args:
        url (str): The URL to request
        rate_limit_per_min (int, optional): Maximum requests per minute. Defaults to 60.
        **kwargs: Additional arguments to pass to make_request
    
    Returns:
        requests.Response or None: Response object or None if request failed
    """
    # Calculate sleep time in seconds to respect rate limit
    sleep_time = 60.0 / rate_limit_per_min
    
    # Add jitter to avoid synchronized requests
    sleep_time += random.uniform(0, 0.5)
    
    # Sleep to respect rate limit
    time.sleep(sleep_time)
    
    # Make the request
    return make_request(url, **kwargs)

def get_json_response(response):
    """Extract JSON data from a response with error handling
    
    Args:
        response (requests.Response): Response object
    
    Returns:
        dict or None: JSON data or None if extraction failed
    """
    if response is None:
        return None
    
    try:
        return response.json()
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from response")
        logger.debug(f"Response content: {response.text[:500]}...")
        return None
    except Exception as e:
        logger.error(f"Unexpected error extracting JSON: {str(e)}")
        return None

def handle_api_error(response):
    """Generate a standardized error message from an API response
    
    Args:
        response (requests.Response): Response object
    
    Returns:
        dict: Error information
    """
    error = {
        'status_code': response.status_code if response else 'No response',
        'error': 'Unknown error'
    }
    
    if response is None:
        error['error'] = 'No response received from API'
        return error
    
    try:
        # Try to extract error from JSON response
        data = response.json()
        if isinstance(data, dict):
            error_msg = data.get('error') or data.get('message') or data.get('errorMessage')
            if error_msg:
                error['error'] = error_msg
                return error
    except:
        # If not JSON or missing error field, use status code
        pass
    
    # Use standard HTTP status messages if nothing else available
    http_errors = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout'
    }
    
    error['error'] = http_errors.get(response.status_code, f'HTTP Error {response.status_code}')
    return error

def is_api_available(url, timeout=5):
    """Check if an API is available
    
    Args:
        url (str): The URL to check
        timeout (int, optional): Request timeout in seconds. Defaults to 5.
    
    Returns:
        bool: True if API is available, False otherwise
    """
    try:
        response = make_request(url, timeout=timeout)
        return response is not None and response.status_code < 500
    except:
        return False

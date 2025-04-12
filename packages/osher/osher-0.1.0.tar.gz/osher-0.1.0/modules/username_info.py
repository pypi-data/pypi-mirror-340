# Username Information Module
# Checks username presence across various platforms

import os
import requests
import time
import json
import concurrent.futures
import logging
from utils import api_helper
import config

logger = logging.getLogger("osint_scout.username_info")

# Define social media sites and their user URL patterns
PLATFORMS = [
    {"name": "Instagram", "url_pattern": "https://www.instagram.com/{}", "error_message": "Sorry, this page isn't available."},
    {"name": "Twitter/X", "url_pattern": "https://twitter.com/{}", "error_message": "This account doesn't exist"},
    {"name": "Facebook", "url_pattern": "https://www.facebook.com/{}", "error_message": "isn't available"},
    {"name": "TikTok", "url_pattern": "https://www.tiktok.com/@{}", "error_message": "Couldn't find this account"},
    {"name": "GitHub", "url_pattern": "https://github.com/{}", "error_message": "Not Found"},
    {"name": "LinkedIn", "url_pattern": "https://www.linkedin.com/in/{}", "error_message": "this page doesn't exist"},
    {"name": "Reddit", "url_pattern": "https://www.reddit.com/user/{}", "error_message": "Sorry, nobody on Reddit goes by that name"},
    {"name": "YouTube", "url_pattern": "https://www.youtube.com/@{}", "error_message": "This page isn't available"},
    {"name": "Pinterest", "url_pattern": "https://www.pinterest.com/{}/", "error_message": "Sorry! We couldn't find that page"},
    {"name": "Twitch", "url_pattern": "https://www.twitch.tv/{}", "error_message": "Sorry. Unless you've got a time machine"},
    {"name": "Medium", "url_pattern": "https://medium.com/@{}", "error_message": "404"},
    {"name": "Quora", "url_pattern": "https://www.quora.com/profile/{}", "error_message": "Page Not Found"},
    {"name": "Mastodon (mastodon.social)", "url_pattern": "https://mastodon.social/@{}", "error_message": "The page you are looking for isn't here"},
    {"name": "SoundCloud", "url_pattern": "https://soundcloud.com/{}", "error_message": "We can't find that user"},
    {"name": "Spotify", "url_pattern": "https://open.spotify.com/user/{}", "error_message": "Couldn't find that page"},
    {"name": "Steam", "url_pattern": "https://steamcommunity.com/id/{}", "error_message": "The specified profile could not be found"},
    {"name": "Vimeo", "url_pattern": "https://vimeo.com/{}", "error_message": "Page not found"},
    {"name": "Behance", "url_pattern": "https://www.behance.net/{}", "error_message": "Be right back"},
    {"name": "Patreon", "url_pattern": "https://www.patreon.com/{}", "error_message": "Page not found"},
    {"name": "Flickr", "url_pattern": "https://www.flickr.com/people/{}", "error_message": "Couldn't find that page"}
]

def get_username_info(username):
    """Find information about a username across various platforms
    
    Args:
        username (str): The username to investigate
        
    Returns:
        dict: Information about the username
    """
    result = {
        'username': username,
        'platforms': [],
        'visualization_data': {
            'username': username,
            'found_platforms': [],
            'not_found_platforms': []
        }
    }
    
    try:
        # Use a thread pool to check multiple platforms concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_platform, username, platform): platform for platform in PLATFORMS}
            
            for future in concurrent.futures.as_completed(futures):
                platform = futures[future]
                try:
                    platform_result = future.result()
                    result['platforms'].append(platform_result)
                    
                    # Add to visualization data
                    if platform_result['found']:
                        result['visualization_data']['found_platforms'].append(platform_result['name'])
                    else:
                        result['visualization_data']['not_found_platforms'].append(platform_result['name'])
                        
                except Exception as e:
                    logger.error(f"Error checking {platform['name']}: {str(e)}")
                    result['platforms'].append({
                        'name': platform['name'],
                        'found': False,
                        'url': platform['url_pattern'].format(username),
                        'error': str(e)
                    })
                    result['visualization_data']['not_found_platforms'].append(platform['name'])
        
        # Sort results
        result['platforms'].sort(key=lambda x: (not x['found'], x['name']))
        
        # Check if we have any other data sources available
        if config.API_KEYS.get('HAVEIBEENPWNED_API_KEY'):
            # If username might be an email, check haveibeenpwned
            if '@' in username:
                breaches = check_haveibeenpwned(username)
                if breaches:
                    result['breaches'] = breaches
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving username information: {str(e)}")
        return {'error': f"Error retrieving username information: {str(e)}"}

def check_platform(username, platform):
    """Check if a username exists on a specific platform
    
    Args:
        username (str): The username to check
        platform (dict): Platform information
    
    Returns:
        dict: Result of the check
    """
    try:
        url = platform['url_pattern'].format(username)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = api_helper.make_request(url, headers=headers, timeout=10)
        
        if response:
            # Check if the error message exists in the response
            found = platform['error_message'] not in response.text
            
            # Additional check for HTTP status codes
            if response.status_code == 404:
                found = False
                
            return {
                'name': platform['name'],
                'found': found,
                'url': url,
                'status_code': response.status_code
            }
        else:
            return {
                'name': platform['name'],
                'found': False,
                'url': url,
                'error': 'No response from server'
            }
            
    except Exception as e:
        logger.error(f"Error checking {platform['name']}: {str(e)}")
        return {
            'name': platform['name'],
            'found': False,
            'url': platform['url_pattern'].format(username),
            'error': str(e)
        }

def check_haveibeenpwned(email):
    """Check if an email has been involved in data breaches
    
    Args:
        email (str): The email to check
    
    Returns:
        list: List of breaches
    """
    try:
        api_key = config.API_KEYS.get('HAVEIBEENPWNED_API_KEY')
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            'hibp-api-key': api_key,
            'User-Agent': 'OSINT-Scout'
        }
        
        response = api_helper.make_request(url, headers=headers)
        
        if response and response.status_code == 200:
            breaches = response.json()
            
            # Format the breaches data
            formatted_breaches = []
            for breach in breaches:
                formatted_breaches.append({
                    'name': breach.get('Name', 'Unknown'),
                    'date': breach.get('BreachDate', 'Unknown'),
                    'description': breach.get('Description', 'No description'),
                    'data_classes': breach.get('DataClasses', [])
                })
            
            return formatted_breaches
        elif response and response.status_code == 404:
            # No breaches found
            return []
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving breach data: Status code {status_code}")
            return []
            
    except Exception as e:
        logger.error(f"Error checking haveibeenpwned: {str(e)}")
        return []

# Email Information Module
# Gathers information about email addresses

import os
import requests
import json
import re
import time
import logging
from utils import api_helper
import config

logger = logging.getLogger("osint_scout.email_info")

def get_email_info(email):
    """Gather information about an email address
    
    Args:
        email (str): The email address to investigate
        
    Returns:
        dict: Information about the email
    """
    result = {
        'email': email,
        'visualization_data': {
            'email': email,
            'domain': email.split('@')[1],
            'breaches': []
        }
    }
    
    try:
        # Start with basic validation
        validation = validate_email(email)
        result['validation'] = validation
        
        # Get domain information
        domain = email.split('@')[1]
        result['domain'] = domain
        
        # Check available APIs
        # Check haveibeenpwned if API key is available
        if config.API_KEYS.get('HAVEIBEENPWNED_API_KEY'):
            breaches = check_haveibeenpwned(email)
            if breaches:
                result['breaches'] = breaches
                result['breach_count'] = len(breaches)
                
                # Add to visualization data
                result['visualization_data']['breaches'] = [b['name'] for b in breaches]
                result['visualization_data']['breach_count'] = len(breaches)
        
        # Check emailrep.io if API key is available
        if config.API_KEYS.get('EMAILREP_API_KEY'):
            reputation = check_emailrep(email)
            if reputation:
                result['reputation'] = reputation
                
                # Add to visualization data
                result['visualization_data']['reputation'] = reputation.get('reputation', 'unknown')
                result['visualization_data']['suspicious'] = reputation.get('suspicious', False)
        
        # Check Hunter.io if API key is available
        if config.API_KEYS.get('HUNTER_API_KEY'):
            hunter_info = check_hunter(email)
            if hunter_info:
                result['hunter'] = hunter_info
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving email information: {str(e)}")
        return {'error': f"Error retrieving email information: {str(e)}"}

def validate_email(email):
    """Perform basic validation of an email address
    
    Args:
        email (str): The email to validate
    
    Returns:
        dict: Validation results
    """
    validation = {
        'format_valid': False,
        'has_mx_records': False,
        'disposable_domain': False,
        'free_provider': False
    }
    
    # Check format with regex
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    validation['format_valid'] = bool(re.match(email_regex, email))
    
    if validation['format_valid']:
        # Extract domain
        domain = email.split('@')[1]
        
        # Check for MX records
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            validation['has_mx_records'] = len(mx_records) > 0
        except Exception:
            validation['has_mx_records'] = False
        
        # Check if domain is a disposable email provider
        disposable_domains = [
            'temp-mail.org', 'guerrillamail.com', 'mailinator.com', 
            'tempmail.com', 'throwawaymail.com', '10minutemail.com',
            'yopmail.com', 'getairmail.com', 'dispostable.com',
            'maildrop.cc', 'mailnesia.com', 'mintemail.com'
        ]
        validation['disposable_domain'] = domain.lower() in disposable_domains
        
        # Check if domain is a free email provider
        free_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'protonmail.com', 'mail.com',
            'zoho.com', 'yandex.com', 'gmx.com'
        ]
        validation['free_provider'] = domain.lower() in free_providers
    
    return validation

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

def check_emailrep(email):
    """Check email reputation using emailrep.io
    
    Args:
        email (str): The email to check
    
    Returns:
        dict: Reputation information
    """
    try:
        api_key = config.API_KEYS.get('EMAILREP_API_KEY')
        url = f"https://emailrep.io/{email}"
        headers = {
            'Key': api_key,
            'User-Agent': 'OSINT-Scout'
        }
        
        response = api_helper.make_request(url, headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            
            # Extract the most relevant information
            reputation = {
                'reputation': data.get('reputation', 'unknown'),
                'suspicious': data.get('suspicious', False),
                'references': data.get('references', 0),
                'blacklisted': data.get('details', {}).get('blacklisted', False),
                'malicious_activity': data.get('details', {}).get('malicious_activity', False),
                'credential_leaked': data.get('details', {}).get('credentials_leaked', False),
                'first_seen': data.get('details', {}).get('first_seen', 'unknown'),
                'last_seen': data.get('details', {}).get('last_seen', 'unknown')
            }
            
            return reputation
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving email reputation: Status code {status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error checking emailrep.io: {str(e)}")
        return None

def check_hunter(email):
    """Check email information using Hunter.io
    
    Args:
        email (str): The email to check
    
    Returns:
        dict: Hunter.io information
    """
    try:
        api_key = config.API_KEYS.get('HUNTER_API_KEY')
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
        
        response = api_helper.make_request(url)
        
        if response and response.status_code == 200:
            data = response.json()
            
            if 'data' in data:
                result = data['data']
                
                # Extract the most relevant information
                hunter_info = {
                    'status': result.get('status', 'unknown'),
                    'result': result.get('result', 'unknown'),
                    'score': result.get('score', 0),
                    'domain': result.get('domain', 'unknown'),
                    'sources': len(result.get('sources', [])),
                    'webmail': result.get('webmail', False)
                }
                
                return hunter_info
            else:
                return None
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving Hunter.io data: Status code {status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error checking Hunter.io: {str(e)}")
        return None

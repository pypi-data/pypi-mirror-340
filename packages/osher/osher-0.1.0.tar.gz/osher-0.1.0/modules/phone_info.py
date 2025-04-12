# Phone Information Module
# Gathers information about phone numbers

import os
import requests
import json
import re
import logging
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from utils import api_helper
import config

logger = logging.getLogger("osint_scout.phone_info")

def get_phone_info(phone_number):
    """Gather information about a phone number
    
    Args:
        phone_number (str): The phone number to investigate (with country code)
        
    Returns:
        dict: Information about the phone number
    """
    result = {
        'phone': phone_number,
        'visualization_data': {}
    }
    
    try:
        # Start with basic validation and information using phonenumbers library
        validation_data = validate_phone(phone_number)
        
        if validation_data:
            result['validation'] = validation_data['validation']
            result['carrier'] = validation_data['carrier']
            result['location'] = validation_data['location']
            
            # Add to visualization data
            result['visualization_data'] = {
                'phone': phone_number,
                'formatted': validation_data['formatted'],
                'valid': validation_data['validation']['is_valid'],
                'country': validation_data['location']['country'],
                'region': validation_data['location']['region'],
                'carrier': validation_data['carrier']['name']
            }
        else:
            return {'error': "Could not parse phone number. Ensure it includes country code (e.g., +1XXXXXXXXXX)"}
        
        # Try to get additional data from NumVerify if API key is available
        if config.API_KEYS.get('NUMVERIFY_API_KEY'):
            numverify_data = get_numverify_data(phone_number)
            if numverify_data and 'error' not in numverify_data:
                # Update the carrier and location data with potentially more accurate information
                result['carrier']['name'] = numverify_data.get('carrier', result['carrier']['name'])
                result['carrier']['line_type'] = numverify_data.get('line_type', 'Unknown')
                
                result['location']['country'] = numverify_data.get('country_name', result['location']['country'])
                result['location']['country_code'] = numverify_data.get('country_code', result['location']['country_code'])
                
                # Update visualization data
                result['visualization_data']['carrier'] = numverify_data.get('carrier', result['visualization_data']['carrier'])
                result['visualization_data']['country'] = numverify_data.get('country_name', result['visualization_data']['country'])
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving phone information: {str(e)}")
        return {'error': f"Error retrieving phone information: {str(e)}"}

def validate_phone(phone_number):
    """Validate and extract information from a phone number
    
    Args:
        phone_number (str): The phone number to validate
    
    Returns:
        dict: Validation and extracted information
    """
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Basic validation
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        # Format the number in different formats
        formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        formatted_international = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        
        # Get region information
        country_code = parsed_number.country_code
        country = geocoder.country_name_for_number(parsed_number, "en")
        region = geocoder.description_for_number(parsed_number, "en")
        
        # Get carrier information
        carrier_name = carrier.name_for_number(parsed_number, "en")
        
        # Get timezone information
        tz = timezone.time_zones_for_number(parsed_number)
        
        # Gather number type
        number_type = phonenumbers.number_type(parsed_number)
        number_type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            99: "UNKNOWN"
        }
        number_type_str = number_type_map.get(number_type, "UNKNOWN")
        
        return {
            'validation': {
                'is_valid': is_valid,
                'is_possible': is_possible,
                'number_type': number_type_str
            },
            'formatted': {
                'e164': formatted_e164,
                'international': formatted_international,
                'national': formatted_national
            },
            'carrier': {
                'name': carrier_name if carrier_name else 'Unknown'
            },
            'location': {
                'country': country if country else 'Unknown',
                'country_code': f"+{country_code}" if country_code else 'Unknown',
                'region': region if region else 'Unknown',
                'timezone': ', '.join(tz) if tz else 'Unknown'
            }
        }
    
    except Exception as e:
        logger.error(f"Error validating phone number: {str(e)}")
        return None

def get_numverify_data(phone_number):
    """Get phone data from numverify API
    
    Args:
        phone_number (str): The phone number to look up
        
    Returns:
        dict: Information about the phone number
    """
    try:
        api_key = config.API_KEYS.get('NUMVERIFY_API_KEY')
        
        # Format the phone number (remove any non-digit characters except leading +)
        if phone_number.startswith('+'):
            formatted_number = '+' + ''.join(filter(str.isdigit, phone_number[1:]))
        else:
            formatted_number = ''.join(filter(str.isdigit, phone_number))
        
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={formatted_number}"
        response = api_helper.make_request(url)
        
        if response and response.status_code == 200:
            data = response.json()
            
            if data.get('valid', False):
                return {
                    'valid': data.get('valid', False),
                    'number': data.get('number', 'Unknown'),
                    'local_format': data.get('local_format', 'Unknown'),
                    'international_format': data.get('international_format', 'Unknown'),
                    'country_code': data.get('country_code', 'Unknown'),
                    'country_name': data.get('country_name', 'Unknown'),
                    'location': data.get('location', 'Unknown'),
                    'carrier': data.get('carrier', 'Unknown'),
                    'line_type': data.get('line_type', 'Unknown')
                }
            else:
                return {'error': 'Invalid phone number'}
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving data from NumVerify: Status code {status_code}")
            return {'error': f"API returned status code {status_code}"}
            
    except Exception as e:
        logger.error(f"Error retrieving data from NumVerify: {str(e)}")
        return {'error': str(e)}

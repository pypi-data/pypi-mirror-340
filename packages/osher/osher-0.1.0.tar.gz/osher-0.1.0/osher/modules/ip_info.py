# IP Information Module
# Gathers information about IP addresses using free public APIs

import os
import requests
import json
import socket
import time
from utils import api_helper
import logging
import config

logger = logging.getLogger("osint_scout.ip_info")

def get_ip_info(ip_address):
    """Gather information about an IP address
    
    Args:
        ip_address (str): The IP address to investigate
        
    Returns:
        dict: Information about the IP address
    """
    result = {
        'visualization_data': {}
    }
    
    try:
        # Get basic IP geolocation data from ipapi.co
        ipapi_data = get_ipapi_data(ip_address)
        if ipapi_data and 'error' not in ipapi_data:
            result.update({
                'IP': ip_address,
                'Type': 'IPv4' if '.' in ip_address else 'IPv6',
                'Country': ipapi_data.get('country_name', 'Unknown'),
                'Country Code': ipapi_data.get('country_code', 'Unknown'),
                'Region': ipapi_data.get('region', 'Unknown'),
                'City': ipapi_data.get('city', 'Unknown'),
                'Latitude': ipapi_data.get('latitude', 'Unknown'),
                'Longitude': ipapi_data.get('longitude', 'Unknown'),
                'ISP': ipapi_data.get('org', 'Unknown'),
                'ASN': ipapi_data.get('asn', 'Unknown'),
                'Timezone': ipapi_data.get('timezone', 'Unknown'),
                'Currency': ipapi_data.get('currency', 'Unknown'),
                'visualization_data': {
                    'latitude': ipapi_data.get('latitude'),
                    'longitude': ipapi_data.get('longitude'),
                    'city': ipapi_data.get('city'),
                    'country': ipapi_data.get('country_name')
                }
            })
        else:
            if ipapi_data and 'error' in ipapi_data:
                return {'error': f"API Error: {ipapi_data['error']}"}
            else:
                return {'error': "Failed to retrieve IP information"}
        
        # Try to get additional data from ipinfo.io if API key is available
        if config.API_KEYS.get('IPINFO_TOKEN'):
            ipinfo_data = get_ipinfo_data(ip_address)
            if ipinfo_data and 'error' not in ipinfo_data:
                result.update({
                    'Hostname': ipinfo_data.get('hostname', 'Unknown'),
                    'Abuse Contact': ipinfo_data.get('abuse', {}).get('email', 'Unknown'),
                    'ISP': ipinfo_data.get('org', result['ISP']),
                    'VPN/Proxy': ipinfo_data.get('privacy', {}).get('vpn', False) or 
                               ipinfo_data.get('privacy', {}).get('proxy', False),
                    'Hosting': ipinfo_data.get('privacy', {}).get('hosting', False)
                })
        
        # Try to get security data from VirusTotal if API key is available
        if config.API_KEYS.get('VIRUSTOTAL_API_KEY'):
            vt_data = get_virustotal_data(ip_address)
            if vt_data and 'error' not in vt_data:
                result.update({
                    'Malicious Reports': vt_data.get('malicious_count', 'Unknown'),
                    'Last Analysis Date': vt_data.get('last_analysis_date', 'Unknown')
                })
        
        # Try to get reverse DNS information
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            result['Reverse DNS'] = hostname
        except (socket.herror, socket.gaierror):
            result['Reverse DNS'] = 'No hostname found'
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving IP information: {str(e)}")
        return {'error': f"Error retrieving IP information: {str(e)}"}

def get_ipapi_data(ip_address):
    """Get IP data from ipapi.co (free tier)
    
    Args:
        ip_address (str): The IP address to look up
        
    Returns:
        dict: Information about the IP address
    """
    try:
        url = f"https://ipapi.co/{ip_address}/json/"
        response = api_helper.make_request(url)
        
        if response and response.status_code == 200:
            data = response.json()
            if 'error' in data:
                return {'error': data.get('reason', 'Unknown error')}
            return data
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving data from ipapi.co: Status code {status_code}")
            return {'error': f"API returned status code {status_code}"}
            
    except Exception as e:
        logger.error(f"Error retrieving data from ipapi.co: {str(e)}")
        return {'error': str(e)}

def get_ipinfo_data(ip_address):
    """Get IP data from ipinfo.io
    
    Args:
        ip_address (str): The IP address to look up
        
    Returns:
        dict: Information about the IP address
    """
    try:
        token = config.API_KEYS.get('IPINFO_TOKEN')
        url = f"https://ipinfo.io/{ip_address}/json?token={token}"
        response = api_helper.make_request(url)
        
        if response and response.status_code == 200:
            return response.json()
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving data from ipinfo.io: Status code {status_code}")
            return {'error': f"API returned status code {status_code}"}
            
    except Exception as e:
        logger.error(f"Error retrieving data from ipinfo.io: {str(e)}")
        return {'error': str(e)}

def get_virustotal_data(ip_address):
    """Get IP security data from VirusTotal
    
    Args:
        ip_address (str): The IP address to look up
        
    Returns:
        dict: Security information about the IP address
    """
    try:
        api_key = config.API_KEYS.get('VIRUSTOTAL_API_KEY')
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
        headers = {
            "x-apikey": api_key
        }
        
        response = api_helper.make_request(url, headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            attributes = data.get('data', {}).get('attributes', {})
            
            last_analysis_stats = attributes.get('last_analysis_stats', {})
            malicious_count = last_analysis_stats.get('malicious', 0)
            
            last_analysis_date = attributes.get('last_analysis_date')
            if last_analysis_date:
                last_analysis_date = time.strftime('%Y-%m-%d', time.localtime(last_analysis_date))
            
            return {
                'malicious_count': malicious_count,
                'last_analysis_date': last_analysis_date
            }
        else:
            status_code = response.status_code if response else 'No response'
            logger.error(f"Error retrieving data from VirusTotal: Status code {status_code}")
            return {'error': f"API returned status code {status_code}"}
            
    except Exception as e:
        logger.error(f"Error retrieving data from VirusTotal: {str(e)}")
        return {'error': str(e)}

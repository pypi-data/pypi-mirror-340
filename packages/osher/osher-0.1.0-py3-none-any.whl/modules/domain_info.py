# Domain Information Module
# Gathers information about domains using free public APIs

import os
import requests
import socket
import time
import json
import dns.resolver
import whois
import ssl
import OpenSSL
from datetime import datetime
import logging
from utils import api_helper
import config

logger = logging.getLogger("osint_scout.domain_info")

def get_domain_info(domain, full_scan=False):
    """Gather information about a domain
    
    Args:
        domain (str): The domain to investigate
        full_scan (bool): Whether to perform a full scan
        
    Returns:
        dict: Information about the domain
    """
    result = {
        'domain': domain,
        'visualization_data': {}
    }
    
    try:
        # Get WHOIS information
        whois_data = get_whois_info(domain)
        if whois_data:
            result['whois'] = whois_data
        
        # Get DNS records
        dns_records = get_dns_records(domain)
        if dns_records:
            result['dns'] = dns_records
        
        # Get SSL/TLS certificate info
        ssl_info = get_ssl_info(domain)
        if ssl_info:
            result['ssl'] = ssl_info
        
        # Get IP address
        try:
            ip_address = socket.gethostbyname(domain)
            result['ip_address'] = ip_address
        except socket.gaierror as e:
            result['ip_address'] = "Could not resolve domain"
        
        # Get HTTP headers
        headers = get_http_headers(domain)
        if headers:
            result['headers'] = headers
        
        # Get website technologies if full scan is requested
        if full_scan:
            techs = get_website_technologies(domain)
            if techs:
                result['technologies'] = techs
        
        # Prepare visualization data
        result['visualization_data'] = {
            'domain': domain,
            'ip': result.get('ip_address'),
            'created': result.get('whois', {}).get('Creation Date'),
            'expires': result.get('whois', {}).get('Expiration Date'),
            'nameservers': result.get('whois', {}).get('Name Servers', []),
            'dns_records': dns_records
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving domain information: {str(e)}")
        return {'error': f"Error retrieving domain information: {str(e)}"}

def get_whois_info(domain):
    """Get WHOIS information for a domain
    
    Args:
        domain (str): The domain to look up
        
    Returns:
        dict: WHOIS information
    """
    try:
        w = whois.whois(domain)
        
        # Clean up the data
        whois_data = {}
        
        # Extract creation date
        if w.creation_date:
            if isinstance(w.creation_date, list):
                whois_data['Creation Date'] = w.creation_date[0].strftime('%Y-%m-%d') if w.creation_date[0] else 'Unknown'
            else:
                whois_data['Creation Date'] = w.creation_date.strftime('%Y-%m-%d') if w.creation_date else 'Unknown'
        else:
            whois_data['Creation Date'] = 'Unknown'
        
        # Extract expiration date
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                whois_data['Expiration Date'] = w.expiration_date[0].strftime('%Y-%m-%d') if w.expiration_date[0] else 'Unknown'
            else:
                whois_data['Expiration Date'] = w.expiration_date.strftime('%Y-%m-%d') if w.expiration_date else 'Unknown'
        else:
            whois_data['Expiration Date'] = 'Unknown'
        
        # Extract registrar
        whois_data['Registrar'] = w.registrar if w.registrar else 'Unknown'
        
        # Extract name servers
        if w.name_servers:
            if isinstance(w.name_servers, list):
                whois_data['Name Servers'] = [ns.lower() for ns in w.name_servers if ns]
            else:
                whois_data['Name Servers'] = [w.name_servers.lower()] if w.name_servers else []
        else:
            whois_data['Name Servers'] = []
        
        # Extract registrant
        if hasattr(w, 'registrant') and w.registrant:
            whois_data['Registrant'] = w.registrant
        elif hasattr(w, 'org') and w.org:
            whois_data['Registrant'] = w.org
        else:
            whois_data['Registrant'] = 'Unknown'
        
        return whois_data
    
    except Exception as e:
        logger.error(f"Error retrieving WHOIS information: {str(e)}")
        return None

def get_dns_records(domain):
    """Get DNS records for a domain
    
    Args:
        domain (str): The domain to look up
        
    Returns:
        list: DNS records
    """
    records = []
    
    try:
        # Common DNS record types
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                
                for rdata in answers:
                    if record_type == 'SOA':
                        records.append({
                            'type': record_type,
                            'value': f"Primary NS: {rdata.mname}, Admin: {rdata.rname}, Serial: {rdata.serial}",
                            'ttl': answers.ttl
                        })
                    elif record_type == 'MX':
                        records.append({
                            'type': record_type,
                            'value': f"{rdata.preference} {rdata.exchange}",
                            'ttl': answers.ttl
                        })
                    else:
                        records.append({
                            'type': record_type,
                            'value': str(rdata),
                            'ttl': answers.ttl
                        })
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.DNSException:
                pass
        
        return records
    
    except Exception as e:
        logger.error(f"Error retrieving DNS records: {str(e)}")
        return []

def get_ssl_info(domain):
    """Get SSL/TLS certificate information for a domain
    
    Args:
        domain (str): The domain to look up
        
    Returns:
        dict: SSL/TLS information
    """
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(5.0)
        
        try:
            conn.connect((domain, 443))
            cert = conn.getpeercert()
            
            # Parse certificate
            ssl_info = {}
            ssl_info['Issuer'] = dict(x[0] for x in cert['issuer'])
            ssl_info['Subject'] = dict(x[0] for x in cert['subject'])
            ssl_info['Version'] = cert['version']
            
            # Parse validity dates
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            
            ssl_info['Valid From'] = not_before.strftime('%Y-%m-%d')
            ssl_info['Valid Until'] = not_after.strftime('%Y-%m-%d')
            ssl_info['Is Valid'] = (datetime.now() > not_before and datetime.now() < not_after)
            
            # Get more detailed information using OpenSSL
            try:
                cert_bin = OpenSSL.crypto.dump_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1,
                    OpenSSL.crypto.load_certificate(
                        OpenSSL.crypto.FILETYPE_PEM,
                        ssl.get_server_certificate((domain, 443))
                    )
                )
                
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_bin)
                ssl_info['Signature Algorithm'] = x509.get_signature_algorithm().decode('utf-8')
                
                # Get the certificate's fingerprints
                ssl_info['SHA1 Fingerprint'] = x509.digest('sha1').decode('utf-8')
                ssl_info['SHA256 Fingerprint'] = x509.digest('sha256').decode('utf-8')
                
            except Exception as e:
                logger.warning(f"Could not get detailed SSL info: {str(e)}")
            
            return ssl_info
            
        except socket.error as e:
            logger.warning(f"SSL connection failed: {str(e)}")
            return {'error': 'SSL connection failed'}
            
    except Exception as e:
        logger.error(f"Error retrieving SSL information: {str(e)}")
        return None
    finally:
        try:
            if 'conn' in locals() and conn:
                conn.close()
        except:
            pass

def get_http_headers(domain):
    """Get HTTP headers for a domain
    
    Args:
        domain (str): The domain to look up
        
    Returns:
        dict: HTTP headers
    """
    try:
        url = f"https://{domain}"
        response = api_helper.make_request(url, timeout=5)
        
        if response:
            headers = dict(response.headers)
            
            # Extract security headers specifically
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not set'),
                'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not set'),
                'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not set'),
                'X-Frame-Options': headers.get('X-Frame-Options', 'Not set'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not set')
            }
            
            return {
                'server': headers.get('Server', 'Not disclosed'),
                'security_headers': security_headers
            }
        
        return None
    
    except Exception as e:
        logger.error(f"Error retrieving HTTP headers: {str(e)}")
        return None

def get_website_technologies(domain):
    """Get technologies used by the website
    
    Args:
        domain (str): The domain to look up
        
    Returns:
        list: Technologies detected
    """
    try:
        # Check if Wappalyzer API key is available
        wappalyzer_api_key = config.API_KEYS.get('WAPPALYZER_API_KEY')
        
        if wappalyzer_api_key:
            url = f"https://api.wappalyzer.com/v2/lookup/?urls=https://{domain}"
            headers = {
                'x-api-key': wappalyzer_api_key
            }
            
            response = api_helper.make_request(url, headers=headers)
            
            if response and response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0].get('technologies', [])
        
        # If no Wappalyzer API key or request failed, use a simple alternative approach
        url = f"https://{domain}"
        response = api_helper.make_request(url, timeout=5)
        
        if response and response.status_code == 200:
            content = response.text.lower()
            detected = []
            
            # Simple detection based on common signatures
            if 'wordpress' in content:
                detected.append('WordPress')
            if 'joomla' in content:
                detected.append('Joomla')
            if 'drupal' in content:
                detected.append('Drupal')
            if 'bootstrap' in content:
                detected.append('Bootstrap')
            if 'jquery' in content:
                detected.append('jQuery')
            if 'react' in content:
                detected.append('React')
            if 'angular' in content:
                detected.append('Angular')
            if 'vue' in content:
                detected.append('Vue.js')
            
            return detected
        
        return []
    
    except Exception as e:
        logger.error(f"Error detecting website technologies: {str(e)}")
        return []

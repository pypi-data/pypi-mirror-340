# Report Generator Module
# Generates reports from OSINT data

import os
import sys
import json
import logging
from datetime import datetime
import html
from rich.console import Console

# Initialize logger
logger = logging.getLogger("osint_scout.report_generator")

# Initialize console
console = Console()

def generate_report(report_type, data, output_file, target):
    """Generate a report from OSINT data
    
    Args:
        report_type (str): Type of report to generate (ip, domain, username, email, phone)
        data (dict): Data to include in the report
        output_file (str): Path to save the report
        target (str): The target of the investigation
        
    Returns:
        bool: True if report was generated successfully, False otherwise
    """
    try:
        # Determine report format based on file extension
        if output_file.endswith('.html'):
            return generate_html_report(report_type, data, output_file, target)
        elif output_file.endswith('.json'):
            return generate_json_report(data, output_file)
        elif output_file.endswith('.txt'):
            return generate_text_report(report_type, data, output_file, target)
        else:
            # Default to HTML if no extension or unrecognized extension
            return generate_html_report(report_type, data, output_file + '.html', target)
            
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        console.print(f"[bold red]Error generating report: {str(e)}[/bold red]")
        return False

def generate_html_report(report_type, data, output_file, target):
    """Generate an HTML report
    
    Args:
        report_type (str): Type of report
        data (dict): Report data
        output_file (str): Output file path
        target (str): Investigation target
        
    Returns:
        bool: Success status
    """
    try:
        # Get the appropriate report template
        report_html = get_html_template(report_type, data, target)
        
        # Write the report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_html)
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        return False

def generate_json_report(data, output_file):
    """Generate a JSON report
    
    Args:
        data (dict): Report data
        output_file (str): Output file path
        
    Returns:
        bool: Success status
    """
    try:
        # Remove visualization_data to keep the report clean
        if 'visualization_data' in data:
            data_copy = data.copy()
            del data_copy['visualization_data']
        else:
            data_copy = data
        
        # Write the JSON data to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_copy, f, indent=4)
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating JSON report: {str(e)}")
        return False

def generate_text_report(report_type, data, output_file, target):
    """Generate a text report
    
    Args:
        report_type (str): Type of report
        data (dict): Report data
        output_file (str): Output file path
        target (str): Investigation target
        
    Returns:
        bool: Success status
    """
    try:
        # Get the appropriate report text
        report_text = get_text_template(report_type, data, target)
        
        # Write the report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating text report: {str(e)}")
        return False

def get_html_template(report_type, data, target):
    """Get HTML template for the report
    
    Args:
        report_type (str): Type of report
        data (dict): Report data
        target (str): Investigation target
        
    Returns:
        str: HTML report
    """
    # Start with the common header
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Scout Report - {escape_html(target)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        .success {{
            color: #27ae60;
        }}
        .warning {{
            color: #f39c12;
        }}
        .danger {{
            color: #e74c3c;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .metadata {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>OSINT Scout Report</h1>
        <div class="metadata">
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Target: {escape_html(target)}</p>
            <p>Report Type: {report_type.upper()}</p>
        </div>
    </div>
"""

    # Add report-specific content
    if report_type == 'ip':
        html += get_ip_html(data, target)
    elif report_type == 'domain':
        html += get_domain_html(data, target)
    elif report_type == 'username':
        html += get_username_html(data, target)
    elif report_type == 'email':
        html += get_email_html(data, target)
    elif report_type == 'phone':
        html += get_phone_html(data, target)
    
    # Add footer
    html += """
    <div class="footer">
        <p>Generated by OSINT Scout - A comprehensive OSINT tool</p>
    </div>
</body>
</html>
"""
    
    return html

def get_ip_html(data, target):
    """Get HTML for IP report
    
    Args:
        data (dict): IP data
        target (str): IP address
        
    Returns:
        str: HTML content
    """
    html = """
    <div class="container section">
        <h2>IP Information</h2>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
    
    # Add all IP properties
    for key, value in data.items():
        if key != 'visualization_data' and key != 'error':
            html += f"""
            <tr>
                <td>{escape_html(key)}</td>
                <td>{escape_html(str(value))}</td>
            </tr>
"""
    
    html += """
        </table>
    </div>
"""
    
    return html

def get_domain_html(data, target):
    """Get HTML for domain report
    
    Args:
        data (dict): Domain data
        target (str): Domain name
        
    Returns:
        str: HTML content
    """
    html = """
    <div class="container section">
        <h2>Domain Information</h2>
"""
    
    # WHOIS Information
    if 'whois' in data:
        html += """
        <h3>WHOIS Information</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['whois'].items():
            if isinstance(value, list):
                value = ', '.join(value)
            html += f"""
            <tr>
                <td>{escape_html(key)}</td>
                <td>{escape_html(str(value))}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    # DNS Records
    if 'dns' in data:
        html += """
        <h3>DNS Records</h3>
        <table>
            <tr>
                <th>Type</th>
                <th>Value</th>
                <th>TTL</th>
            </tr>
"""
        
        for record in data['dns']:
            html += f"""
            <tr>
                <td>{escape_html(record['type'])}</td>
                <td>{escape_html(record['value'])}</td>
                <td>{escape_html(str(record['ttl']))}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    # SSL Information
    if 'ssl' in data:
        html += """
        <h3>SSL/TLS Information</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['ssl'].items():
            if isinstance(value, dict):
                value = json.dumps(value)
            html += f"""
            <tr>
                <td>{escape_html(key)}</td>
                <td>{escape_html(str(value))}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    # HTTP Headers
    if 'headers' in data:
        html += """
        <h3>HTTP Headers</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        if 'server' in data['headers']:
            html += f"""
            <tr>
                <td>Server</td>
                <td>{escape_html(data['headers']['server'])}</td>
            </tr>
"""
        
        if 'security_headers' in data['headers']:
            for key, value in data['headers']['security_headers'].items():
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td>{escape_html(str(value))}</td>
                </tr>
"""
        
        html += """
        </table>
"""
    
    # Website Technologies
    if 'technologies' in data:
        html += """
        <h3>Website Technologies</h3>
        <ul>
"""
        
        for tech in data['technologies']:
            if isinstance(tech, dict):
                tech_name = tech.get('name', 'Unknown')
                html += f"<li>{escape_html(tech_name)}</li>"
            else:
                html += f"<li>{escape_html(tech)}</li>"
        
        html += """
        </ul>
"""
    
    html += """
    </div>
"""
    
    return html

def get_username_html(data, target):
    """Get HTML for username report
    
    Args:
        data (dict): Username data
        target (str): Username
        
    Returns:
        str: HTML content
    """
    html = """
    <div class="container section">
        <h2>Username Information</h2>
"""
    
    # Platform presence
    if 'platforms' in data:
        html += """
        <h3>Social Media Presence</h3>
        <table>
            <tr>
                <th>Platform</th>
                <th>Found</th>
                <th>URL</th>
            </tr>
"""
        
        for platform in data['platforms']:
            found_icon = "✓" if platform['found'] else "✗"
            found_class = "success" if platform['found'] else "danger"
            
            html += f"""
            <tr>
                <td>{escape_html(platform['name'])}</td>
                <td class="{found_class}">{found_icon}</td>
                <td><a href="{escape_html(platform['url'])}" target="_blank">{escape_html(platform['url'])}</a></td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    # Breaches information
    if 'breaches' in data:
        html += """
        <h3>Data Breaches</h3>
        <table>
            <tr>
                <th>Breach</th>
                <th>Date</th>
                <th>Description</th>
            </tr>
"""
        
        for breach in data['breaches']:
            html += f"""
            <tr>
                <td>{escape_html(breach['name'])}</td>
                <td>{escape_html(breach['date'])}</td>
                <td>{escape_html(breach['description'])}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    html += """
    </div>
"""
    
    return html

def get_email_html(data, target):
    """Get HTML for email report
    
    Args:
        data (dict): Email data
        target (str): Email address
        
    Returns:
        str: HTML content
    """
    html = """
    <div class="container section">
        <h2>Email Information</h2>
"""
    
    # Email validation
    if 'validation' in data:
        html += """
        <h3>Email Validation</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['validation'].items():
            if isinstance(value, bool):
                icon = "✓" if value else "✗"
                cls = "success" if value else "danger"
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td class="{cls}">{icon}</td>
                </tr>
"""
            else:
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td>{escape_html(str(value))}</td>
                </tr>
"""
        
        html += """
        </table>
"""
    
    # Reputation information
    if 'reputation' in data:
        html += """
        <h3>Email Reputation</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['reputation'].items():
            if isinstance(value, bool):
                icon = "✓" if not value else "✗"  # Inverted for reputation (blacklisted, etc.)
                cls = "success" if not value else "danger"
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td class="{cls}">{icon}</td>
                </tr>
"""
            else:
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td>{escape_html(str(value))}</td>
                </tr>
"""
        
        html += """
        </table>
"""
    
    # Breaches information
    if 'breaches' in data:
        html += """
        <h3>Data Breaches</h3>
        <table>
            <tr>
                <th>Breach</th>
                <th>Date</th>
                <th>Description</th>
                <th>Data Types</th>
            </tr>
"""
        
        for breach in data['breaches']:
            data_classes = ', '.join(breach.get('data_classes', []))
            html += f"""
            <tr>
                <td>{escape_html(breach['name'])}</td>
                <td>{escape_html(breach['date'])}</td>
                <td>{escape_html(breach['description'])}</td>
                <td>{escape_html(data_classes)}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    else:
        html += """
        <h3>Data Breaches</h3>
        <p class="success">No data breaches found for this email address.</p>
"""
    
    html += """
    </div>
"""
    
    return html

def get_phone_html(data, target):
    """Get HTML for phone report
    
    Args:
        data (dict): Phone data
        target (str): Phone number
        
    Returns:
        str: HTML content
    """
    html = """
    <div class="container section">
        <h2>Phone Number Information</h2>
"""
    
    # Phone validation
    if 'validation' in data:
        html += """
        <h3>Phone Validation</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['validation'].items():
            if isinstance(value, bool):
                icon = "✓" if value else "✗"
                cls = "success" if value else "danger"
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td class="{cls}">{icon}</td>
                </tr>
"""
            else:
                html += f"""
                <tr>
                    <td>{escape_html(key)}</td>
                    <td>{escape_html(str(value))}</td>
                </tr>
"""
        
        html += """
        </table>
"""
    
    # Carrier information
    if 'carrier' in data:
        html += """
        <h3>Carrier Information</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['carrier'].items():
            html += f"""
            <tr>
                <td>{escape_html(key)}</td>
                <td>{escape_html(str(value))}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    # Location information
    if 'location' in data:
        html += """
        <h3>Location Information</h3>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
"""
        
        for key, value in data['location'].items():
            html += f"""
            <tr>
                <td>{escape_html(key)}</td>
                <td>{escape_html(str(value))}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    html += """
    </div>
"""
    
    return html

def get_text_template(report_type, data, target):
    """Get text template for the report
    
    Args:
        report_type (str): Type of report
        data (dict): Report data
        target (str): Investigation target
        
    Returns:
        str: Text report
    """
    # Common header
    text = f"""OSINT Scout Report
=================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target: {target}
Report Type: {report_type.upper()}

"""
    
    # Add report-specific content
    if report_type == 'ip':
        text += get_ip_text(data, target)
    elif report_type == 'domain':
        text += get_domain_text(data, target)
    elif report_type == 'username':
        text += get_username_text(data, target)
    elif report_type == 'email':
        text += get_email_text(data, target)
    elif report_type == 'phone':
        text += get_phone_text(data, target)
    
    # Add footer
    text += """
Generated by OSINT Scout - A comprehensive OSINT tool
"""
    
    return text

def get_ip_text(data, target):
    """Get text for IP report
    
    Args:
        data (dict): IP data
        target (str): IP address
        
    Returns:
        str: Text content
    """
    text = """IP Information
--------------
"""
    
    # Add all IP properties
    for key, value in data.items():
        if key != 'visualization_data' and key != 'error':
            text += f"{key}: {value}\n"
    
    return text

def get_domain_text(data, target):
    """Get text for domain report
    
    Args:
        data (dict): Domain data
        target (str): Domain name
        
    Returns:
        str: Text content
    """
    text = """Domain Information
------------------
"""
    
    # WHOIS Information
    if 'whois' in data:
        text += "\nWHOIS Information:\n"
        text += "-------------------\n"
        
        for key, value in data['whois'].items():
            if isinstance(value, list):
                value = ', '.join(value)
            text += f"{key}: {value}\n"
    
    # DNS Records
    if 'dns' in data:
        text += "\nDNS Records:\n"
        text += "------------\n"
        
        for record in data['dns']:
            text += f"Type: {record['type']}, Value: {record['value']}, TTL: {record['ttl']}\n"
    
    # SSL Information
    if 'ssl' in data:
        text += "\nSSL/TLS Information:\n"
        text += "-------------------\n"
        
        for key, value in data['ssl'].items():
            if isinstance(value, dict):
                value = str(value)
            text += f"{key}: {value}\n"
    
    # HTTP Headers
    if 'headers' in data:
        text += "\nHTTP Headers:\n"
        text += "-------------\n"
        
        if 'server' in data['headers']:
            text += f"Server: {data['headers']['server']}\n"
        
        if 'security_headers' in data['headers']:
            text += "\nSecurity Headers:\n"
            for key, value in data['headers']['security_headers'].items():
                text += f"{key}: {value}\n"
    
    # Website Technologies
    if 'technologies' in data:
        text += "\nWebsite Technologies:\n"
        text += "--------------------\n"
        
        for tech in data['technologies']:
            if isinstance(tech, dict):
                tech_name = tech.get('name', 'Unknown')
                text += f"- {tech_name}\n"
            else:
                text += f"- {tech}\n"
    
    return text

def get_username_text(data, target):
    """Get text for username report
    
    Args:
        data (dict): Username data
        target (str): Username
        
    Returns:
        str: Text content
    """
    text = """Username Information
--------------------
"""
    
    # Platform presence
    if 'platforms' in data:
        text += "\nSocial Media Presence:\n"
        text += "---------------------\n"
        
        for platform in data['platforms']:
            found = "Found" if platform['found'] else "Not Found"
            text += f"{platform['name']}: {found} - {platform['url']}\n"
    
    # Breaches information
    if 'breaches' in data:
        text += "\nData Breaches:\n"
        text += "--------------\n"
        
        for breach in data['breaches']:
            text += f"Breach: {breach['name']}\n"
            text += f"Date: {breach['date']}\n"
            text += f"Description: {breach['description']}\n"
            text += "\n"
    
    return text

def get_email_text(data, target):
    """Get text for email report
    
    Args:
        data (dict): Email data
        target (str): Email address
        
    Returns:
        str: Text content
    """
    text = """Email Information
-----------------
"""
    
    # Email validation
    if 'validation' in data:
        text += "\nEmail Validation:\n"
        text += "----------------\n"
        
        for key, value in data['validation'].items():
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            text += f"{key}: {value}\n"
    
    # Reputation information
    if 'reputation' in data:
        text += "\nEmail Reputation:\n"
        text += "----------------\n"
        
        for key, value in data['reputation'].items():
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            text += f"{key}: {value}\n"
    
    # Breaches information
    if 'breaches' in data:
        text += "\nData Breaches:\n"
        text += "--------------\n"
        
        for breach in data['breaches']:
            text += f"Breach: {breach['name']}\n"
            text += f"Date: {breach['date']}\n"
            text += f"Description: {breach['description']}\n"
            data_classes = ', '.join(breach.get('data_classes', []))
            text += f"Data Types: {data_classes}\n"
            text += "\n"
    else:
        text += "\nData Breaches: None found\n"
    
    return text

def get_phone_text(data, target):
    """Get text for phone report
    
    Args:
        data (dict): Phone data
        target (str): Phone number
        
    Returns:
        str: Text content
    """
    text = """Phone Number Information
------------------------
"""
    
    # Phone validation
    if 'validation' in data:
        text += "\nPhone Validation:\n"
        text += "----------------\n"
        
        for key, value in data['validation'].items():
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            text += f"{key}: {value}\n"
    
    # Carrier information
    if 'carrier' in data:
        text += "\nCarrier Information:\n"
        text += "-------------------\n"
        
        for key, value in data['carrier'].items():
            text += f"{key}: {value}\n"
    
    # Location information
    if 'location' in data:
        text += "\nLocation Information:\n"
        text += "--------------------\n"
        
        for key, value in data['location'].items():
            text += f"{key}: {value}\n"
    
    return text

def escape_html(text):
    """Escape HTML special characters
    
    Args:
        text (str): Text to escape
        
    Returns:
        str: Escaped text
    """
    return html.escape(str(text))

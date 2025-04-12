from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import logging
from datetime import datetime
import modules.ip_info as ip_info
import modules.domain_info as domain_info
import modules.email_info as email_info
import modules.username_info as username_info
import modules.phone_info as phone_info
import modules.report_generator as report_generator
from utils.input_validator import is_valid_ip, is_valid_domain, is_valid_email, is_valid_username, is_valid_phone

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "osint-scout-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        # Get form data
        target = request.form.get('target', '').strip()
        scan_type = request.form.get('scan_type', '').strip()
        
        if not target or not scan_type:
            return jsonify({'error': 'Target and scan type are required'}), 400
        
        # Validate input based on scan type
        if scan_type == 'ip' and not is_valid_ip(target):
            return jsonify({'error': 'Invalid IP address format'}), 400
        elif scan_type == 'domain' and not is_valid_domain(target):
            return jsonify({'error': 'Invalid domain format'}), 400
        elif scan_type == 'email' and not is_valid_email(target):
            return jsonify({'error': 'Invalid email format'}), 400
        elif scan_type == 'username' and not is_valid_username(target):
            return jsonify({'error': 'Invalid username format'}), 400
        elif scan_type == 'phone' and not is_valid_phone(target):
            return jsonify({'error': 'Invalid phone number format (use +CountryCodeNumber)'}), 400
        
        # Perform the scan based on type
        results = {}
        if scan_type == 'ip':
            results = ip_info.get_ip_info(target)
        elif scan_type == 'domain':
            full_scan = request.form.get('full_scan', 'false').lower() == 'true'
            results = domain_info.get_domain_info(target, full_scan)
        elif scan_type == 'email':
            results = email_info.get_email_info(target)
        elif scan_type == 'username':
            results = username_info.get_username_info(target)
        elif scan_type == 'phone':
            results = phone_info.get_phone_info(target)
        else:
            return jsonify({'error': 'Invalid scan type'}), 400
        
        # Check for errors in the results
        if 'error' in results:
            return jsonify({'error': results['error']}), 400
        
        # Generate a timestamp for the results
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results['timestamp'] = timestamp
        results['target'] = target
        results['scan_type'] = scan_type
        
        # Return the results
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error in scan: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/report', methods=['POST'])
def generate_report():
    try:
        # Get form data
        report_type = request.form.get('report_type', '').strip()
        target = request.form.get('target', '').strip()
        report_format = request.form.get('format', 'html').strip().lower()
        data = request.form.get('data', '').strip()
        
        if not report_type or not target or not data:
            return jsonify({'error': 'Report type, target, and data are required'}), 400
        
        # Parse the data
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Generate a filename
        filename = f"report_{report_type}_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add extension based on format
        if report_format == 'json':
            filename += '.json'
        elif report_format == 'text':
            filename += '.txt'
        else:  # Default to HTML
            filename += '.html'
        
        # Create temp directory if it doesn't exist
        os.makedirs('temp', exist_ok=True)
        filepath = os.path.join('temp', filename)
        
        # Generate the report
        success = report_generator.generate_report(report_type, data, filepath, target)
        
        if not success:
            return jsonify({'error': 'Failed to generate report'}), 500
        
        # Return the report file
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error in report generation: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
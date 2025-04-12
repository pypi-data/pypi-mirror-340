# OSHER

A comprehensive OSINT (Open Source Intelligence) tool with multiple data sources.

## Features

- IP address intelligence - geolocation, ISP information, and security assessment
- Domain analysis - WHOIS data, DNS records, SSL certificate information
- Email verification - format validation, breach checks, reputation analysis
- Username search - presence checks across multiple social media platforms
- Phone number intelligence - carrier information, location, validation
- Report generation - export findings in HTML, JSON, or TXT formats
- Data visualization capabilities
- Both CLI and web interface

## Installation

```bash
pip install osher
```

## Usage

### Command Line Interface

```bash
# Get help
osher --help

# IP address lookup
osher ip 8.8.8.8

# Domain information
osher domain example.com

# Email analysis
osher email user@example.com

# Username search
osher username johndoe

# Phone number lookup
osher phone +12125551234

# Interactive mode
osher interactive
```

### Web Interface

```bash
# Start the web interface
osher-web
```

Then open your browser and navigate to http://localhost:5000

## API Keys

While OSHER works with free public APIs, some services require API keys for better results. The following optional API keys can be configured:

- VirusTotal API Key - for security assessment
- IPinfo.io Token - for additional IP intelligence
- HaveIBeenPwned API Key - for breach checks
- EmailRep API Key - for email reputation analysis
- Hunter.io API Key - for email verification
- NumVerify API Key - for phone number verification
- Wappalyzer API Key - for website technology detection

You can set these API keys as environment variables or configure them through the interactive mode.

## License

MIT
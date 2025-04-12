#!/usr/bin/env python3
# OSINT Scout - Comprehensive OSINT Tool
# Author: AI Assistant

import os
import sys
import click
import logging
import importlib
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import time
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("osint_scout")

# Initialize console
console = Console()

# Import modules
from modules import ip_info, domain_info, username_info, email_info, phone_info
from modules import visualization, report_generator
from utils import data_formatter, input_validator, api_helper

# ASCII Art logo
LOGO = """
 ██████╗ ███████╗██╗███╗   ██╗████████╗    ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ██╔════╝██╔════╝██╔═══██╗██║   ██║╚══██╔══╝
██║   ██║███████╗██║██╔██╗ ██║   ██║       ███████╗██║     ██║   ██║██║   ██║   ██║   
██║   ██║╚════██║██║██║╚██╗██║   ██║       ╚════██║██║     ██║   ██║██║   ██║   ██║   
╚██████╔╝███████║██║██║ ╚████║   ██║       ███████║╚██████╗╚██████╔╝╚██████╔╝   ██║   
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝       ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
                                                                               v1.0.0
"""

def show_intro():
    """Display the introduction screen"""
    console.print(LOGO, style="bold blue")
    console.print("\n[bold cyan]A comprehensive OSINT tool with multiple data sources[/bold cyan]")
    console.print("Gather intelligence on IPs, domains, usernames, emails and more")
    console.print("All data is collected from free public APIs\n")

def check_api_keys():
    """Check if necessary API keys are available"""
    missing_keys = []
    
    for key, value in config.API_KEYS.items():
        if not value:
            missing_keys.append(key)
    
    if missing_keys:
        console.print(f"[yellow]Warning: The following API keys are missing:[/yellow]")
        for key in missing_keys:
            console.print(f"[yellow]- {key}[/yellow]")
        console.print("[yellow]Some functionality may be limited.[/yellow]\n")

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """OSINT Scout - A comprehensive OSINT tool with multiple data sources"""
    show_intro()
    check_api_keys()

@cli.command()
@click.option('--address', '-a', help='The IP address to investigate', required=True)
@click.option('--output', '-o', help='Output file path for the report', default=None)
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization of the data')
def ip(address, output, visualize):
    """Gather information about an IP address"""
    if not input_validator.is_valid_ip(address):
        console.print(f"[bold red]Error: '{address}' is not a valid IP address[/bold red]")
        return
    
    console.print(f"[bold green]Investigating IP address: {address}[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("Gathering data...", total=None)
        
        # Gather IP information
        ip_data = ip_info.get_ip_info(address)
        
        if 'error' in ip_data:
            console.print(f"[bold red]Error: {ip_data['error']}[/bold red]")
            return
            
        # Display results
        ip_table = Table(title=f"Information for IP: {address}", box=box.ROUNDED)
        ip_table.add_column("Property", style="cyan")
        ip_table.add_column("Value", style="green")
        
        for key, value in ip_data.items():
            if key != 'visualization_data':
                ip_table.add_row(key, str(value))
        
        console.print(ip_table)
        
        # Generate visualization if requested
        if visualize and 'visualization_data' in ip_data:
            console.print("[bold blue]Generating visualization...[/bold blue]")
            visualization.generate_ip_viz(ip_data['visualization_data'], address)
            console.print("[bold green]Visualization complete![/bold green]")
        
        # Generate report if requested
        if output:
            console.print(f"[bold blue]Generating report to {output}...[/bold blue]")
            report_generator.generate_report("ip", ip_data, output, address)
            console.print(f"[bold green]Report saved to {output}[/bold green]")

@cli.command()
@click.option('--domain', '-d', help='The domain to investigate', required=True)
@click.option('--output', '-o', help='Output file path for the report', default=None)
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization of the data')
@click.option('--full-scan', '-f', is_flag=True, help='Perform a full scan of the domain')
def domain(domain, output, visualize, full_scan):
    """Gather information about a domain"""
    if not input_validator.is_valid_domain(domain):
        console.print(f"[bold red]Error: '{domain}' is not a valid domain[/bold red]")
        return
    
    console.print(f"[bold green]Investigating domain: {domain}[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("Gathering data...", total=None)
        
        # Gather domain information
        domain_data = domain_info.get_domain_info(domain, full_scan)
        
        if 'error' in domain_data:
            console.print(f"[bold red]Error: {domain_data['error']}[/bold red]")
            return
        
        # Display general domain information
        console.print(Panel(f"[bold cyan]Domain Information: {domain}[/bold cyan]"))
        
        # Whois Information
        if 'whois' in domain_data:
            whois_table = Table(title="WHOIS Information", box=box.ROUNDED)
            whois_table.add_column("Property", style="cyan")
            whois_table.add_column("Value", style="green")
            
            for key, value in domain_data['whois'].items():
                whois_table.add_row(key, str(value))
            
            console.print(whois_table)
        
        # DNS Information
        if 'dns' in domain_data:
            dns_table = Table(title="DNS Records", box=box.ROUNDED)
            dns_table.add_column("Type", style="cyan")
            dns_table.add_column("Value", style="green")
            dns_table.add_column("TTL", style="yellow")
            
            for record in domain_data['dns']:
                dns_table.add_row(record['type'], record['value'], str(record['ttl']))
            
            console.print(dns_table)
        
        # SSL/TLS Information
        if 'ssl' in domain_data:
            ssl_table = Table(title="SSL/TLS Information", box=box.ROUNDED)
            ssl_table.add_column("Property", style="cyan")
            ssl_table.add_column("Value", style="green")
            
            for key, value in domain_data['ssl'].items():
                ssl_table.add_row(key, str(value))
            
            console.print(ssl_table)
        
        # Generate visualization if requested
        if visualize and 'visualization_data' in domain_data:
            console.print("[bold blue]Generating visualization...[/bold blue]")
            visualization.generate_domain_viz(domain_data['visualization_data'], domain)
            console.print("[bold green]Visualization complete![/bold green]")
        
        # Generate report if requested
        if output:
            console.print(f"[bold blue]Generating report to {output}...[/bold blue]")
            report_generator.generate_report("domain", domain_data, output, domain)
            console.print(f"[bold green]Report saved to {output}[/bold green]")

@cli.command()
@click.option('--username', '-u', help='The username to investigate', required=True)
@click.option('--output', '-o', help='Output file path for the report', default=None)
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization of the data')
def username(username, output, visualize):
    """Find information about a username across various platforms"""
    if not input_validator.is_valid_username(username):
        console.print(f"[bold red]Error: '{username}' contains invalid characters for a username[/bold red]")
        return
    
    console.print(f"[bold green]Investigating username: {username}[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("Gathering data...", total=None)
        
        # Gather username information
        username_data = username_info.get_username_info(username)
        
        if 'error' in username_data:
            console.print(f"[bold red]Error: {username_data['error']}[/bold red]")
            return
        
        # Display results
        console.print(Panel(f"[bold cyan]Username Information: {username}[/bold cyan]"))
        
        # Social Media Presence
        if 'platforms' in username_data:
            platforms_table = Table(title="Social Media Presence", box=box.ROUNDED)
            platforms_table.add_column("Platform", style="cyan")
            platforms_table.add_column("Found", style="green")
            platforms_table.add_column("URL", style="blue")
            
            for platform in username_data['platforms']:
                found_text = "✓" if platform['found'] else "✗"
                found_style = "green" if platform['found'] else "red"
                url = platform['url'] if platform['found'] else "N/A"
                platforms_table.add_row(platform['name'], f"[{found_style}]{found_text}[/{found_style}]", url)
            
            console.print(platforms_table)
        
        # Generate visualization if requested
        if visualize and 'visualization_data' in username_data:
            console.print("[bold blue]Generating visualization...[/bold blue]")
            visualization.generate_username_viz(username_data['visualization_data'], username)
            console.print("[bold green]Visualization complete![/bold green]")
        
        # Generate report if requested
        if output:
            console.print(f"[bold blue]Generating report to {output}...[/bold blue]")
            report_generator.generate_report("username", username_data, output, username)
            console.print(f"[bold green]Report saved to {output}[/bold green]")

@cli.command()
@click.option('--email', '-e', help='The email address to investigate', required=True)
@click.option('--output', '-o', help='Output file path for the report', default=None)
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization of the data')
def email(email, output, visualize):
    """Gather information about an email address"""
    if not input_validator.is_valid_email(email):
        console.print(f"[bold red]Error: '{email}' is not a valid email address[/bold red]")
        return
    
    console.print(f"[bold green]Investigating email address: {email}[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("Gathering data...", total=None)
        
        # Gather email information
        email_data = email_info.get_email_info(email)
        
        if 'error' in email_data:
            console.print(f"[bold red]Error: {email_data['error']}[/bold red]")
            return
        
        # Display results
        console.print(Panel(f"[bold cyan]Email Information: {email}[/bold cyan]"))
        
        # Email Validation
        if 'validation' in email_data:
            validation_table = Table(title="Email Validation", box=box.ROUNDED)
            validation_table.add_column("Property", style="cyan")
            validation_table.add_column("Value", style="green")
            
            for key, value in email_data['validation'].items():
                if isinstance(value, bool):
                    value_text = "✓" if value else "✗"
                    value_style = "green" if value else "red"
                    validation_table.add_row(key, f"[{value_style}]{value_text}[/{value_style}]")
                else:
                    validation_table.add_row(key, str(value))
            
            console.print(validation_table)
        
        # Data Breaches
        if 'breaches' in email_data and email_data['breaches']:
            breaches_table = Table(title="Data Breaches", box=box.ROUNDED)
            breaches_table.add_column("Name", style="cyan")
            breaches_table.add_column("Date", style="yellow")
            breaches_table.add_column("Description", style="green")
            
            for breach in email_data['breaches']:
                breaches_table.add_row(breach['name'], breach['date'], breach['description'])
            
            console.print(breaches_table)
        elif 'breaches' in email_data:
            console.print("[green]No data breaches found for this email.[/green]")
        
        # Generate visualization if requested
        if visualize and 'visualization_data' in email_data:
            console.print("[bold blue]Generating visualization...[/bold blue]")
            visualization.generate_email_viz(email_data['visualization_data'], email)
            console.print("[bold green]Visualization complete![/bold green]")
        
        # Generate report if requested
        if output:
            console.print(f"[bold blue]Generating report to {output}...[/bold blue]")
            report_generator.generate_report("email", email_data, output, email)
            console.print(f"[bold green]Report saved to {output}[/bold green]")

@cli.command()
@click.option('--number', '-n', help='The phone number to investigate (with country code)', required=True)
@click.option('--output', '-o', help='Output file path for the report', default=None)
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization of the data')
def phone(number, output, visualize):
    """Gather information about a phone number"""
    if not input_validator.is_valid_phone(number):
        console.print(f"[bold red]Error: '{number}' is not a valid phone number format. Include country code (e.g., +1XXXXXXXXXX)[/bold red]")
        return
    
    console.print(f"[bold green]Investigating phone number: {number}[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("Gathering data...", total=None)
        
        # Gather phone information
        phone_data = phone_info.get_phone_info(number)
        
        if 'error' in phone_data:
            console.print(f"[bold red]Error: {phone_data['error']}[/bold red]")
            return
        
        # Display results
        console.print(Panel(f"[bold cyan]Phone Number Information: {number}[/bold cyan]"))
        
        # Phone Validation
        if 'validation' in phone_data:
            validation_table = Table(title="Phone Validation", box=box.ROUNDED)
            validation_table.add_column("Property", style="cyan")
            validation_table.add_column("Value", style="green")
            
            for key, value in phone_data['validation'].items():
                if isinstance(value, bool):
                    value_text = "✓" if value else "✗"
                    value_style = "green" if value else "red"
                    validation_table.add_row(key, f"[{value_style}]{value_text}[/{value_style}]")
                else:
                    validation_table.add_row(key, str(value))
            
            console.print(validation_table)
        
        # Carrier Information
        if 'carrier' in phone_data:
            carrier_table = Table(title="Carrier Information", box=box.ROUNDED)
            carrier_table.add_column("Property", style="cyan")
            carrier_table.add_column("Value", style="green")
            
            for key, value in phone_data['carrier'].items():
                carrier_table.add_row(key, str(value))
            
            console.print(carrier_table)
        
        # Location Information
        if 'location' in phone_data:
            location_table = Table(title="Location Information", box=box.ROUNDED)
            location_table.add_column("Property", style="cyan")
            location_table.add_column("Value", style="green")
            
            for key, value in phone_data['location'].items():
                location_table.add_row(key, str(value))
            
            console.print(location_table)
        
        # Generate visualization if requested
        if visualize and 'visualization_data' in phone_data:
            console.print("[bold blue]Generating visualization...[/bold blue]")
            visualization.generate_phone_viz(phone_data['visualization_data'], number)
            console.print("[bold green]Visualization complete![/bold green]")
        
        # Generate report if requested
        if output:
            console.print(f"[bold blue]Generating report to {output}...[/bold blue]")
            report_generator.generate_report("phone", phone_data, output, number)
            console.print(f"[bold green]Report saved to {output}[/bold green]")

@cli.command()
def interactive():
    """Launch interactive mode for OSINT Scout"""
    console.print("\n[bold cyan]OSINT Scout Interactive Mode[/bold cyan]")
    console.print("Select a module to run interactively\n")
    
    options = [
        "IP Address Investigation",
        "Domain Investigation",
        "Username Investigation",
        "Email Investigation", 
        "Phone Number Investigation",
        "Exit Interactive Mode"
    ]
    
    while True:
        for i, option in enumerate(options, 1):
            console.print(f"[bold]{i}.[/bold] {option}")
        
        choice = Prompt.ask("\nEnter your choice", choices=[str(i) for i in range(1, len(options)+1)])
        choice = int(choice)
        
        if choice == 6:
            console.print("[yellow]Exiting interactive mode...[/yellow]")
            break
        
        # Get common parameters
        visualize = Prompt.ask("Generate visualization? (y/n)", choices=["y", "n"]) == "y"
        output = Prompt.ask("Save report to file? (Enter filename or leave empty for no report)")
        output = output if output else None
        
        if choice == 1:  # IP
            address = Prompt.ask("Enter IP address to investigate")
            if input_validator.is_valid_ip(address):
                # Reuse the CLI command logic
                ip.callback(address=address, output=output, visualize=visualize)
            else:
                console.print(f"[bold red]Error: '{address}' is not a valid IP address[/bold red]")
        
        elif choice == 2:  # Domain
            domain_name = Prompt.ask("Enter domain name to investigate")
            full_scan = Prompt.ask("Perform full scan? (y/n)", choices=["y", "n"]) == "y"
            if input_validator.is_valid_domain(domain_name):
                # Reuse the CLI command logic
                domain.callback(domain=domain_name, output=output, visualize=visualize, full_scan=full_scan)
            else:
                console.print(f"[bold red]Error: '{domain_name}' is not a valid domain[/bold red]")
        
        elif choice == 3:  # Username
            username_val = Prompt.ask("Enter username to investigate")
            if input_validator.is_valid_username(username_val):
                # Reuse the CLI command logic
                username.callback(username=username_val, output=output, visualize=visualize)
            else:
                console.print(f"[bold red]Error: '{username_val}' contains invalid characters for a username[/bold red]")
        
        elif choice == 4:  # Email
            email_val = Prompt.ask("Enter email address to investigate")
            if input_validator.is_valid_email(email_val):
                # Reuse the CLI command logic
                email.callback(email=email_val, output=output, visualize=visualize)
            else:
                console.print(f"[bold red]Error: '{email_val}' is not a valid email address[/bold red]")
        
        elif choice == 5:  # Phone
            phone_val = Prompt.ask("Enter phone number to investigate (with country code)")
            if input_validator.is_valid_phone(phone_val):
                # Reuse the CLI command logic
                phone.callback(number=phone_val, output=output, visualize=visualize)
            else:
                console.print(f"[bold red]Error: '{phone_val}' is not a valid phone number format. Include country code (e.g., +1XXXXXXXXXX)[/bold red]")
        
        console.print("\n[bold cyan]---------------------------------------------[/bold cyan]\n")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        if os.environ.get("DEBUG"):
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)

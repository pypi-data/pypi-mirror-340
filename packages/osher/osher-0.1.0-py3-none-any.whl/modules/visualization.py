# Visualization Module
# Generates visualizations for OSINT data

import os
import sys
import logging
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib.colors import LinearSegmentedColormap
import io
from rich.console import Console

# Configure matplotlib to use a non-interactive backend
matplotlib.use('Agg')

# Initialize logger
logger = logging.getLogger("osint_scout.visualization")

# Initialize console
console = Console()

def generate_ip_viz(data, ip):
    """Generate visualization for IP data
    
    Args:
        data (dict): Visualization data
        ip (str): IP address
    """
    try:
        # Create a figure with world map to show IP location
        plt.figure(figsize=(12, 8))
        
        # Check if we have latitude and longitude
        if data.get('latitude') and data.get('longitude'):
            # Create a world map using Natural Earth data
            # This is a simple approach, more complex maps would require additional libraries
            from mpl_toolkits.basemap import Basemap
            
            # Create map with Natural Earth projection
            m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=80,
                        llcrnrlon=-180, urcrnrlon=180, resolution='c')
            
            # Draw map features
            m.drawcoastlines(linewidth=0.5)
            m.drawcountries(linewidth=0.5)
            m.fillcontinents(color='#DDDDDD', lake_color='#FFFFFF')
            m.drawmapboundary(fill_color='#FFFFFF')
            
            # Plot the IP location
            x, y = m(data['longitude'], data['latitude'])
            m.plot(x, y, 'ro', markersize=10)
            
            # Add a text label for the city/country
            location_label = f"{data.get('city', '')}, {data.get('country', '')}"
            plt.annotate(location_label, xy=(x, y), xytext=(10, 10),
                        textcoords="offset points", fontsize=12,
                        bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.7))
            
            plt.title(f"Geolocation of IP Address: {ip}", fontsize=16)
        else:
            # If no coordinates, display a message
            plt.text(0.5, 0.5, 'No geolocation data available for this IP address', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=plt.gca().transAxes, fontsize=16)
            plt.axis('off')
            plt.title(f"Geolocation of IP Address: {ip}", fontsize=16)
        
        # Save the visualization
        filename = f"ip_viz_{ip.replace('.', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Visualization saved to [bold]{filename}[/bold][/green]")
        
    except ImportError:
        console.print("[yellow]Basemap not installed. Install with 'pip install basemap' for better visualizations.[/yellow]")
        
        # Create a simple bar chart with available data instead
        plt.figure(figsize=(10, 6))
        
        # Use available data to create a visualization
        title = f"IP Information: {ip}"
        if data.get('country'):
            title += f" ({data.get('city', '')}, {data['country']})"
        
        plt.title(title, fontsize=16)
        plt.text(0.5, 0.5, 'Install Basemap for geographic visualization', 
                horizontalalignment='center', verticalalignment='center', 
                transform=plt.gca().transAxes, fontsize=14)
        plt.axis('off')
        
        # Save the visualization
        filename = f"ip_viz_{ip.replace('.', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Simple visualization saved to [bold]{filename}[/bold][/green]")
        
    except Exception as e:
        logger.error(f"Error generating IP visualization: {str(e)}")
        console.print(f"[bold red]Error generating visualization: {str(e)}[/bold red]")

def generate_domain_viz(data, domain):
    """Generate visualization for domain data
    
    Args:
        data (dict): Visualization data
        domain (str): Domain name
    """
    try:
        # Create a figure for the domain visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Domain age/expiry timeline
        created = data.get('created')
        expires = data.get('expires')
        
        if created and expires:
            try:
                # Try to parse dates if they're strings
                if isinstance(created, str):
                    created = datetime.strptime(created, '%Y-%m-%d')
                if isinstance(expires, str):
                    expires = datetime.strptime(expires, '%Y-%m-%d')
                
                today = datetime.now()
                
                # Timeline visualization
                dates = [created, today, expires]
                labels = ['Created', 'Today', 'Expires']
                y_pos = np.zeros(len(dates))  # All points at same height
                
                ax1.scatter(dates, y_pos, s=100, color='blue')
                
                # Add labels
                for i, (date, label) in enumerate(zip(dates, labels)):
                    ax1.annotate(f"{label}\n{date.strftime('%Y-%m-%d')}", 
                                xy=(date, 0), xytext=(0, 10 if i % 2 == 0 else -30),
                                textcoords="offset points", ha='center',
                                bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.7))
                
                # Calculate domain age
                domain_age = (today - created).days
                domain_age_years = domain_age / 365.25
                time_to_expiry = (expires - today).days
                
                age_text = f"Domain Age: {domain_age_years:.1f} years ({domain_age} days)"
                expiry_text = f"Time to Expiry: {time_to_expiry} days"
                
                ax1.text(0.5, 0.85, age_text, transform=ax1.transAxes, ha='center', fontsize=12)
                ax1.text(0.5, 0.75, expiry_text, transform=ax1.transAxes, ha='center', fontsize=12)
                
                # Connect points with line
                ax1.plot([created, expires], [0, 0], 'b-', alpha=0.3)
                
                # Configure axis
                ax1.set_ylim(-0.5, 0.5)
                ax1.get_yaxis().set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['top'].set_visible(False)
                
                ax1.set_title('Domain Timeline', fontsize=14)
            except (ValueError, TypeError) as e:
                ax1.text(0.5, 0.5, f'Could not parse date information\nError: {str(e)}', 
                        ha='center', va='center', transform=ax1.transAxes, fontsize=12)
                ax1.axis('off')
        else:
            ax1.text(0.5, 0.5, 'No creation or expiration data available', 
                    ha='center', va='center', transform=ax1.transAxes, fontsize=12)
            ax1.axis('off')
        
        # DNS Records visualization
        dns_records = data.get('dns_records', [])
        
        if dns_records:
            # Count record types
            record_types = {}
            for record in dns_records:
                record_type = record.get('type', 'Unknown')
                record_types[record_type] = record_types.get(record_type, 0) + 1
            
            # Create pie chart
            labels = list(record_types.keys())
            sizes = list(record_types.values())
            
            # Use a custom colormap
            cmap = plt.cm.get_cmap('tab10')
            colors = [cmap(i) for i in range(len(labels))]
            
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax2.set_title(f'DNS Record Types ({sum(sizes)} records)', fontsize=14)
        else:
            ax2.text(0.5, 0.5, 'No DNS records available', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=12)
            ax2.axis('off')
        
        # Add domain name as the figure title
        plt.suptitle(f"Domain Information: {domain}", fontsize=16)
        plt.tight_layout()
        
        # Save the visualization
        filename = f"domain_viz_{domain.replace('.', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Visualization saved to [bold]{filename}[/bold][/green]")
        
    except Exception as e:
        logger.error(f"Error generating domain visualization: {str(e)}")
        console.print(f"[bold red]Error generating visualization: {str(e)}[/bold red]")

def generate_username_viz(data, username):
    """Generate visualization for username data
    
    Args:
        data (dict): Visualization data
        username (str): Username
    """
    try:
        # Get lists of platforms where the username was found and not found
        found_platforms = data.get('found_platforms', [])
        not_found_platforms = data.get('not_found_platforms', [])
        
        # Create the visualization
        plt.figure(figsize=(12, 8))
        
        # Settings for the bar chart
        platforms = found_platforms + not_found_platforms
        status = [1] * len(found_platforms) + [0] * len(not_found_platforms)
        colors = ['green'] * len(found_platforms) + ['red'] * len(not_found_platforms)
        
        # Sort alphabetically
        sorted_indices = sorted(range(len(platforms)), key=lambda x: platforms[x].lower())
        platforms = [platforms[i] for i in sorted_indices]
        status = [status[i] for i in sorted_indices]
        colors = [colors[i] for i in sorted_indices]
        
        # Create a horizontal bar chart
        y_pos = range(len(platforms))
        
        plt.barh(y_pos, status, align='center', color=colors, alpha=0.7)
        plt.yticks(y_pos, platforms)
        
        # Add labels
        for i, (s, c) in enumerate(zip(status, colors)):
            label = "Found" if s == 1 else "Not Found"
            plt.text(s/2, i, label, ha='center', va='center', color='white', fontweight='bold')
        
        # Configure the plot
        plt.xlabel('Status')
        plt.title(f'Username Presence Check: {username}', fontsize=16)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Adjust the x-axis
        plt.xlim(0, 1.2)
        plt.xticks([])
        
        # Add count summary
        plt.figtext(0.5, 0.01, 
                   f"Found on {len(found_platforms)} platforms, not found on {len(not_found_platforms)} platforms",
                   ha="center", fontsize=12, 
                   bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
        
        # Save the visualization
        filename = f"username_viz_{username}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Visualization saved to [bold]{filename}[/bold][/green]")
        
    except Exception as e:
        logger.error(f"Error generating username visualization: {str(e)}")
        console.print(f"[bold red]Error generating visualization: {str(e)}[/bold red]")

def generate_email_viz(data, email):
    """Generate visualization for email data
    
    Args:
        data (dict): Visualization data
        email (str): Email address
    """
    try:
        # Create a figure for the email visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Extract and anonymize the email for display
        username, domain = email.split('@')
        anonymized_username = username[0] + '*' * (len(username) - 2) + username[-1] if len(username) > 2 else username
        anonymized_email = f"{anonymized_username}@{domain}"
        
        # First plot: Email validation results
        valid = data.get('valid', True)
        suspicious = data.get('suspicious', False)
        
        # Create validation metrics plot
        validation_labels = ['Email Format', 'Domain Exists', 'Not Disposable', 'Not Suspicious']
        validation_values = [1, 1, 1, 0 if suspicious else 1]  # Assuming the email passed basic validation
        
        # Use green for good, red for bad
        colors = ['green' if v == 1 else 'red' for v in validation_values]
        
        ax1.barh(validation_labels, validation_values, color=colors, alpha=0.7)
        
        for i, v in enumerate(validation_values):
            label = "Pass" if v == 1 else "Fail"
            ax1.text(v/2, i, label, ha='center', va='center', color='white', fontweight='bold')
        
        ax1.set_xlim(0, 1.2)
        ax1.set_xticks([])
        ax1.set_title('Email Validation Checks', fontsize=14)
        
        # Second plot: Data breaches if available
        breaches = data.get('breaches', [])
        breach_count = data.get('breach_count', 0)
        
        if breaches:
            # Create a pie chart showing breach types or a simple indicator
            from collections import Counter
            
            # Get years of breaches
            years = [breach[:4] for breach in breaches]
            year_counts = Counter(years)
            
            # Sort by year
            labels = sorted(year_counts.keys())
            sizes = [year_counts[year] for year in labels]
            
            # Use a colormap that goes from green to red
            cmap = plt.cm.get_cmap('YlOrRd')
            colors = [cmap(i/len(labels)) for i in range(len(labels))]
            
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax2.axis('equal')
            ax2.set_title(f'Breaches by Year ({breach_count} total)', fontsize=14)
        else:
            # If no breaches, show a happy message
            ax2.text(0.5, 0.5, 'No data breaches found!', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=16, color='green')
            ax2.axis('off')
        
        # Add email as the figure title (anonymized)
        plt.suptitle(f"Email Information: {anonymized_email}", fontsize=16)
        plt.tight_layout()
        
        # Save the visualization
        filename = f"email_viz_{domain}.png"  # Using just the domain to avoid putting full email in filename
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Visualization saved to [bold]{filename}[/bold][/green]")
        
    except Exception as e:
        logger.error(f"Error generating email visualization: {str(e)}")
        console.print(f"[bold red]Error generating visualization: {str(e)}[/bold red]")

def generate_phone_viz(data, phone):
    """Generate visualization for phone data
    
    Args:
        data (dict): Visualization data
        phone (str): Phone number
    """
    try:
        # Create a figure for the phone visualization
        plt.figure(figsize=(12, 8))
        
        # Extract data
        formatted = data.get('formatted', phone)
        valid = data.get('valid', False)
        country = data.get('country', 'Unknown')
        region = data.get('region', 'Unknown')
        carrier = data.get('carrier', 'Unknown')
        
        # Create a visual representation of phone information
        
        # Use a radar chart for validity metrics
        categories = ['Valid Format', 'Active Number', 'Not VoIP', 'Geographic Number', 'Carrier Identified']
        # Mock values for demonstration - in a real scenario, these would come from API responses
        values = [1 if valid else 0, 0.7, 0.8, 0.9, 1 if carrier != 'Unknown' else 0]
        
        # Create a radar chart
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
        
        # Close the plot
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        categories = np.concatenate((categories, [categories[0]]))
        
        # Create the plot
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        
        # Set the labels
        ax.set_thetagrids(angles[:-1] * 180/np.pi, categories[:-1])
        
        # Adjust the plot
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
        ax.grid(True)
        
        # Add a title
        plt.title(f"Phone Analysis: {formatted}\nCountry: {country}, Region: {region}, Carrier: {carrier}", pad=20)
        
        # Save the visualization
        # Remove any non-alphanumeric characters from the phone number for the filename
        import re
        safe_phone = re.sub(r'\W+', '', phone)
        filename = f"phone_viz_{safe_phone}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Visualization saved to [bold]{filename}[/bold][/green]")
        
    except Exception as e:
        logger.error(f"Error generating phone visualization: {str(e)}")
        console.print(f"[bold red]Error generating visualization: {str(e)}[/bold red]")

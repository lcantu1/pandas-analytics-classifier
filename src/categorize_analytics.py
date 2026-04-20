import pandas as pd
import re
import os
from pathlib import Path

# Set up robust file paths
SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'raw_analytics_6_months.csv'

def get_primary_category(row):
    """Categorizes URLs into high-level site sections based on path and custom dimensions."""
    path = str(row.get('Page path', '')).lower()
    page_type = str(row.get('custom_page_type', '')).lower()

    if re.search(r'webapp|webappeloqua|hubspot|webappceros', path):
        return 'Landing Pages'
    elif re.search(r'/myaccount/', path):
        return 'Account Management'
    elif re.search(r'accessorie|asset|shop|battery|charger|dock|mount|ethernet-station', path) or 'accessory' in page_type:
        return 'Accessories & Assets'
    elif re.search(r'/sales/|sales.html', path):
        return 'Corporate'
    elif re.search(r'/products/|pdp|pxp|product detail', page_type) or re.search(r'/products/', path):
        return 'Product Details (PDP)'
    elif re.search(r'/partner-central/', path):
        return 'Partner Portal'
    elif re.search(r'blog', page_type):
        return 'Blog'
    elif re.search(r'/topic/', path) or re.search(r'topics:', page_type):
        return 'Topic Hubs'
    # Normalize varied localized homepage extensions
    elif re.search(r'en_us\.html|fr_fr\.html|de_xc\.html|es_xl\.html|pt_xl\.html', path) or 'homepage' in page_type:
        return 'Homepage'
    elif re.search(r'/application-catalog|/product-catalog', path):
        return 'Catalogs'
    elif re.search(r'policy|privacy|legal|terms', path):
        return 'Legal & Privacy'
    elif '/customers/' in path or 'case-study' in path:
        return 'Customer Stories'
    elif re.search(r'support|training', path) or 'support' in page_type:
        return 'Support & Training'
    elif re.search(r'/about|careers|investors|newsroom', path) or 'company pages' in page_type:
        return 'Corporate'
    elif re.search(r'contact|solution-finder|builder|how-to-buy|preference-center', path):
        return 'Conversion Funnel'
    elif re.search(r'/solutions|/industries', path) or re.search(r'all industries|product subcategory', page_type):
        return 'Solutions & Industries'
    elif re.search(r'404|error|search|site-map|/test.html|-testing-', path) or re.search(r'search|404', page_type):
        return 'Utility & Error'
    else:
        return 'Other'

def get_secondary_category(row):
    """Provides granular product and service categorization for deep-dive analysis."""
    path = str(row.get('Page path', '')).lower()

    if path in ['/en_us.html', '/en_us']: return "Homepage"

    # General Product Branching
    if '/product' in path:
        if re.search(r'accessorie|battery|charger', path): return "Hardware - Accessories"
        if re.search(r'enterprise-hardware|business-radio', path): return "Hardware - Enterprise"
        if re.search(r'consumer-hardware', path): return "Hardware - Consumer"
        if re.search(r'video|camera|security', path): return "Video Systems - L1"
        if re.search(r'software|command|application', path): return "Software - L1"
        if re.search(r'infrastructure|system', path): return "Infrastructure Systems"

    # Granular Software & Services Routing
    if re.search(r'dispatch|integration|mission-critical|scada', path): return "Hardware - Core Systems"
    if re.search(r'commercial-business|pymes|pequenas-medias', path): return "Hardware - SMB"
    if re.search(r'broadband|lte|wave', path): return "Network - LTE/Broadband"
    if re.search(r'community-engagement', path): return "Software - Community Engagement"
    if re.search(r'emergency-call', path): return "Software - Emergency Routing"
    if re.search(r'command-and-control|computer-aided', path): return "Software - Control Systems"
    if re.search(r'real-time-intelligence|data-management', path): return "Software - Data Management"
    if re.search(r'managed-support|services /', path): return "Services - Managed IT"
    if re.search(r'cybersecurity', path): return "Services - Cybersecurity"
    
    # Granular Video & Analytics Routing
    if re.search(r'video-security-access-control', path): return "Video - Access Control"
    if re.search(r'body-worn-camera|wearables', path): return "Video - Wearables"
    if re.search(r'in-car-video-system', path): return "Video - Vehicle Systems"
    if re.search(r'license-plate-recognition|lpr', path): return "Video - LPR Analytics"
    if re.search(r'fixed-cameras|dome-cameras', path): return "Video - Fixed Hardware"
    if re.search(r'video-security-analytics\.html|surveillance', path): return "Video - Analytics L1"

    # Catch-all Corporate & Support Routing
    if re.search(r'/about|/investors|/newsroom|/careers|/legal', path): return "Corporate & General"
    if re.search(r'partner', path): return "Partners & Resellers"
    if re.search(r'/support|/myaccount|/self-service|warranty|billing', path): return "Support & Billing"
    if re.search(r'contact-us|how-to-buy|subscribe|events|webinar', path): return "Lead Generation"
    if re.search(r'404|error|search|site-map', path): return "Utility & Error"
    
    return "Other"

def get_normalized_page_type(row):
    """Normalizes the custom page type tracking dimension into standardized buckets."""
    page_type = str(row.get('custom_page_type', '')).lower() if pd.notnull(row.get('custom_page_type')) else ""
    path = str(row.get('Page path', '')).lower() if pd.notnull(row.get('Page path')) else ""

    if re.search(r'home|homepage', page_type): return "Homepage"
    if re.search(r'404|401', page_type): return "404 / Error"
    if re.search(r'blog', page_type): return "Blog"
    if re.search(r'topics', page_type): return "Topics"
    if re.search(r'story|case-study', page_type): return "Customer Story"    
    if re.search(r'product detail|pdp template|accessory detail|pxp', page_type): return "Product Detail (PDP)"
    if re.search(r'all products solutions|product line|product subcategory', page_type): return "Products & Solutions Index"
    if re.search(r'all industries', page_type): return "Industries Index"
    if re.search(r'company pages|investors|press release|newsroom', page_type): return "Company & News"
    if re.search(r'cart|checkout|quickorder|saved-carts', page_type): return "Cart & Checkout"
    if re.search(r'search', page_type): return "Search Results"
    if re.search(r'landing', page_type) or re.search(r'webapp|hubspot', path): return "Landing Pages"
    if re.search(r'general content|deep content|full width|long_scroll', page_type): return "General Content"
   
    return "Other / Not Set"

def generate_full_url(row):
    """Reconstructs the full URL from the relative page path."""
    path = str(row.get('Page path', '')).lower()
    return 'https://www.example-enterprise.com' + path

# --- Main Execution Block ---

if not INPUT_FILE.exists():
    print(f"❌ ERROR: File not found at {INPUT_FILE}")
    print(f"Make sure the CSV is in this folder: {SCRIPT_DIR}")
else:
    print(f"✅ Found file! Processing...")
   
    # low_memory=False prevents DtypeWarning on large mixed-type datasets
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    # Apply categorization functions to create new dimensions
    df['Primary_Category'] = df.apply(get_primary_category, axis=1)
    df['Secondary_Category'] = df.apply(get_secondary_category, axis=1)
    df['Page_Type_Normalized'] = df.apply(get_normalized_page_type, axis=1)
    df['Full_URL'] = df.apply(generate_full_url, axis=1)

    # Dynamic file naming to prevent overwriting previous exports
    base_name = 'Categorized_Analytics_Master'
    extension = '.csv'
   
    output_file = SCRIPT_DIR / f"{base_name}{extension}"
    counter = 1
   
    while output_file.exists():
        output_file = SCRIPT_DIR / f"{base_name}_v{counter}{extension}"
        counter += 1

    df.to_csv(output_file, index=False)
    print(f"🚀 Success! Categorized dataset saved as: {output_file.name}")

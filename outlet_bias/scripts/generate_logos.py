import pandas as pd
import requests
from urllib.parse import urlparse
import os

df = pd.read_csv("merged_outlet_bias_data.csv")


def extract_domain(url):
    """Extract domain from URL."""
    if not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # Remove www. prefix if present
        domain = domain.replace("www.", "")
        return domain
    except:
        return None


def download_favicon(domain, filename, output_dir="favicons"):
    """Download favicon from DuckDuckGo API."""
    if not domain:
        return None
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    favicon_url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
    
    try:
        response = requests.get(favicon_url, timeout=5)
        if response.status_code == 200:
            output_path = os.path.join(output_dir, f"{filename}.ico")
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
    except Exception as e:
        print(f"Error downloading favicon for {domain}: {e}")
    
    return None


# Extract domain and download favicons
if "url_b" in df.columns and "twitter" in df.columns:
    df["domain"] = df["url_b"].apply(extract_domain)
    df["favicon_path"] = df.apply(
        lambda row: download_favicon(row["domain"], row["twitter"]),
        axis=1
    )
    
    # Save the updated dataframe
    df.to_csv("merged_outlet_bias_data_with_logos.csv", index=False)

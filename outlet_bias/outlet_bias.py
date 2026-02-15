import os
import pandas as pd

_csv_path = os.path.join(os.path.dirname(__file__), "merged_outlet_bias_data.csv")
df = pd.read_csv(_csv_path)

class NewsOutlet:
    def __init__(self, url):
        self._outlet_data = self._find_outlet_by_url(url)
        self.name = self._outlet_data.get("news_source")
        self.rating = self._outlet_data.get("rating")
        self.logo_url = f"https://mucube.github.io/news-outlet-favicons/favicons/{self._outlet_data.get('twitter')}.ico"
    
    def _find_outlet_by_url(self, url):
        from urllib.parse import urlparse
        
        # Extract domain from article URL
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        
        # Search for matching outlet in dataframe
        matches = df[df["url_b"].str.contains(domain, case=False, na=False)]
        
        if not matches.empty:
            return matches.iloc[0].to_dict()
        
        return None
    
    def json(self):
        return {
            "name": self.name,
            "rating": self.rating,
            "logo_url": self.logo_url
        }

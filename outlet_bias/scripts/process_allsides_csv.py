import pandas as pd
import re

def extract_twitter_handle(url):
    if not isinstance(url, str):
        return None
    match = re.search(r'twitter\.com/@?([a-zA-Z0-9_]+)', url)
    out = match.group(1) if match else None
    return out.lower() if out else None

allsides_df = pd.read_csv("allsides_data.csv")

allsides_df["twitter"] = allsides_df["twitter"].apply(extract_twitter_handle)

allsides_df.to_csv("fixed_allsides.csv", index=False)
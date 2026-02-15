import pandas as pd

allsides_df = pd.read_csv("fixed_allsides.csv")
urls_df = pd.read_csv("sites_with_url.csv")

merged_df = allsides_df.join(urls_df.set_index("twitter"), on="twitter", how="inner", lsuffix="_a", rsuffix="_b").to_csv("merged_outlet_bias_data.csv", index=False)

merged_df = pd.read_csv("merged_outlet_bias_data.csv")
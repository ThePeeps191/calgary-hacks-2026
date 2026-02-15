# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("NEWSAPI_KEY")

# def search_urls(query, url):
#     params = {
#         "q": query,
#         "sortBy": "publishedAt",
#         "pageSize": 10,
#         "apiKey": api_key,
#         "language": "en"
#     }

#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         articles = data.get("articles", [])
        
#         unique_articles = []
#         seen_titles = set()

#         for article in articles:
#             title = article['title'].strip().lower()
            
#             if title not in seen_titles:
#                 seen_titles.add(title)
#                 unique_articles.append(article)
            
#             if len(unique_articles) == 5:
#                 break

#         print(f"--- 5 Unique Latest Articles for '{query}' ---\n")
#         for i, article in enumerate(unique_articles, 1):
#             print(f"{i}. {article['title']}")
#             print(f"   Published: {article['publishedAt']}")
#             print(f"   Source: {article['source']['name']}")
#             print(f"   Link: {article['url']}\n")
            
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.json())

# # Call the function
# search_urls("OpenAI", "https://www.wired.com/story/openai-nuking-4o-model-china-chatgpt-fans-arent-ok/")
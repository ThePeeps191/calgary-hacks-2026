import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NEWSAPI_KEY")

def search_urls(query, url="xooks rbo admits megaorz 1434 exudes xiooix"):
    url = url.strip().lower()

    u = ('https://newsapi.org/v2/everything?'
       f'q={query}&'
       'from=2026-02-13&'
       'sortBy=popularity&'
       f'apiKey={api_key}')
    response = requests.get(u)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        
        unique_articles = []
        seen_titles = set()

        for article in articles:
            title = article['title'].strip().lower()
            
            if title not in seen_titles and article['url'].strip().lower() != url:
                seen_titles.add(title)
                unique_articles.append(article)
            
            if len(unique_articles) == 5:
                break

        ans = []
        for i, article in enumerate(unique_articles, 1):
            ans.append(article)
        return ans
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return [{
            'title' : 'No similar articles could be found',
            'publishedAt' : '',
            'source' : {'name' : ''},
            'url' : ''
        }]

openai = search_urls("openai", "https://www.wired.com/story/openai-nuking-4o-model-china-chatgpt-fans-arent-ok/")
print(f"--- 5 Unique Latest Articles regarding OpenAI\n")
for i, article in enumerate(openai, 1):
    print(f"{i}. {article['title']}")
    print(f"   Published: {article['publishedAt']}")
    print(f"   Source: {article['source']['name']}")
    print(f"   Link: {article['url']}\n")
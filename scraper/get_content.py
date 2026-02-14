from newspaper import Article

def get_content(url):
    article = Article(url)
    article.download()
    article.parse()

    # Article content
    authors = article.authors
    date = article.publish_date.strftime("%Y-%m-%d")
    text = article.text
    top_image = article.top_image

    # Natural Language Processing
    article.nlp()
    keywords = article.keywords
    summary = article.summary

    content_dict = {
        "authors" : authors,
        "date" : date,
        "text" : text,
        "top_image" : top_image,
        "keywords" : keywords,
        "summary" : summary
    }

    return content_dict
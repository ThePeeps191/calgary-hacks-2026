import newspaper

print("newspaper has been imported.")

def get_content(url):
    """
    Get content from a url such as authrow, date, text, and keywords
    """
    article = newspaper.article(url)
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

if __name__ == "__main__":
    content_dict = get_content("https://edition.cnn.com/2023/10/29/sport/nfl-week-8-how-to-watch-spt-intl/index.html")
    print(content_dict)
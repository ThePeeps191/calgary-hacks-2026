import newspaper

print("newspaper has been imported.")

def get_content(url):
    article = newspaper.article(url)
    article.download()
    article.parse()

    # Article content
    authors = article.authors
    if article.publish_date.strftime("%Y-%m-%d") is not None:
        date = article.publish_date.strftime("%Y-%m-%d")
    else:   
        date = "No Date"
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
    content_dict = get_content("https://www.cnn.com/2026/02/14/politics/former-federal-workers-doge-cuts")
    print(content_dict['text'])
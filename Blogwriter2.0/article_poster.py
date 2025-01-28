import os
import requests
from pathlib import Path

# Configuration
WP_URL = "https://jimmyschannel.nl/wp-json/wp/v2"
WP_USER = "jimthecreator"
WP_APP_PASSWORD = "ijNK DiHT 1VOd YMpc onij VAdh"
ARTICLE_FOLDER = r"C:\Users\verst\Desktop\RewrittenArticles"

def post_article(title, content, category=None, tags=None):
    """
    Posts an article to WordPress.
    """
    url = f"{WP_URL}/posts"
    auth = (WP_USER, WP_APP_PASSWORD)
    data = {
        "title": title,
        "content": content,
        "status": "draft",  # Set to 'draft' if you don't want it published immediately
    }
    if category:
        data["categories"] = category
    if tags:
        data["tags"] = tags

    response = requests.post(url, auth=auth, json=data)
    if response.status_code == 201:
        print(f"Posted: {title}")
    else:
        print(f"Failed to post: {title} - {response.content}")

def read_articles(folder):
    """
    Reads articles from the specified folder.
    """
    for file in Path(folder).glob("*.txt"):  # Change to '*.md' or '*.html' as needed
        with open(file, "r", encoding="utf-8") as f:
            yield file.name, f.read()

def main():
    for filename, content in read_articles(ARTICLE_FOLDER):
        title = filename.rsplit(".", 1)[0]  # Extract title from filename
        post_article(title, content)

if __name__ == "__main__":
    main()

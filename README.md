# automatic-blog-poster
This is my first draft of an automatic blog poster, it now works using a scraper, which isn't really ethical, so I dissaprove of anyone using this (for now). 
README.md

This suite of scripts streamlines the process of scraping articles from websites, rewriting them for a broader audience, and posting them to a WordPress site. The process is divided into three stages:
1. Scraping Articles

    Script: scraper.py
    Description: This script utilizes Selenium to scrape articles from a specified website. It extracts titles and content, saving them as .txt files in a user-defined output folder.
    Key Features:
        Supports various website structures through XPath selectors.
        Ensures unique article links to avoid duplication.
        Runs in headless mode for seamless operation.
    Input: Website URL and output folder (selected via a GUI).
    Output: Scraped articles saved as .txt files in the specified folder.

2. Rewriting Articles

    Script: rewriter.py
    Description: This script takes scraped articles and rewrites them in a less formal tone. It expands the content with additional facts and information and categorizes the articles based on keywords.
    Key Features:
        Assigns categories (e.g., Technology, Health) based on content.
        Uses a local AI model for rewriting (ensure compatibility with the dolphin-mistral model).
        Saves rewritten articles in a designated folder.
    Input: .txt files from the scraping stage.
    Output: Rewritten and categorized articles saved in the RewrittenArticles folder.

3. Posting Articles

    Script: article_poster.py
    Description: This script posts the rewritten articles to a WordPress site as draft posts.
    Key Features:
        Utilizes the WordPress REST API for seamless integration.
        Requires WordPress credentials and API configuration (WP_USER, WP_APP_PASSWORD, and WP_URL).
        Posts titles and content while optionally assigning categories and tags.
    Input: .txt files from the rewriting stage.
    Output: Articles uploaded as draft posts on the WordPress site.

Setup and Usage

    Environment Setup:
        Install dependencies: pip install selenium webdriver-manager requests.
        Configure WordPress credentials in article_poster.py.
    Run Scripts:
        Step 1: Execute scraper.py to scrape articles.
        Step 2: Automatically triggered: rewriter.py rewrites and categorizes articles.
        Step 3: Automatically triggered: article_poster.py posts rewritten articles to WordPress.
    Adjust Settings:
        Update folder paths and model names as needed in the scripts.
        Ensure correct XPath selectors in scraper.py for the target website.

Overarching Requirements

    Python 3.x environment.
    Selenium with ChromeDriver installed and functional.
    WordPress site with REST API credentials (Application Passwords plugin recommended).
    Local AI model installed (dolphin-mistral or equivalent).

By following these instructions, you can automate article management efficiently from scraping to publication.

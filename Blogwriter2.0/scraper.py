import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import filedialog, simpledialog


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def scrape_articles(output_folder, website_url):
    driver = initialize_driver()
    print(f"Initialized WebDriver. Navigating to: {website_url}")

    try:
        driver.get(website_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print(f"Successfully loaded website: {website_url}")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")

        # XPaths to locate articles using various identifiers
        article_links_xpaths = [
            "//div[@class='search-txt']//a",  # Technology blog
            "//div[@class='item-title']//a",  # Item title class
            "//div[@class='sc-c6f6255e-0 eGcloy']//a", #BBC
            "//div[@class='container__headline-text']//a",
                                                                    ]

        article_links = []
        for xpath in article_links_xpaths:
            try:
                article_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath))
                )
                links = [elem.get_attribute("href") for elem in article_elements if elem.get_attribute("href")]
                article_links.extend(links)
            except Exception as e:
                print(f"Error locating articles with XPath {xpath}: {e}")

        # Remove duplicate links
        article_links = list(set(article_links))

        for idx, article_url in enumerate(article_links[:10], start=1):  # Limit to 10 articles
            print(f"Opening article link: {article_url}")
            scrape_single_article(driver, output_folder, article_url, idx)

    finally:
        driver.quit()
        print("WebDriver session ended.")


def scrape_single_article(driver, output_folder, article_url, index):
    try:
        driver.get(article_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # XPath to locate title and paragraphs
        title_xpath = "//h1"  # Adjust based on the page structure
        paragraph_xpath = "//p"  # Selects all <p> elements

        title = None
        content = []
        try:
            # Extract title
            title = driver.find_element(By.XPATH, title_xpath).text
        except Exception as e:
            print(f"Title not found for article {index}: {e}")

        try:
            # Extract all paragraphs
            paragraph_elements = driver.find_elements(By.XPATH, paragraph_xpath)
            content = [p.text for p in paragraph_elements if p.text.strip()]  # Only include non-empty paragraphs
        except Exception as e:
            print(f"Content not found for article {index}: {e}")

        if title and content:
            # Combine paragraphs into a single string
            full_content = "\n\n".join(content)

            # Sanitize the title to create a valid filename
            sanitized_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in title).strip()
            file_name = f"{sanitized_title}.txt"

            # Save to file
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Title: {title}\n\nLink: {article_url}\n\n{full_content}")
            print(f"Saved article '{title}' content to: {file_path}")
    except Exception as e:
        print(f"Error scraping article {index} at URL {article_url}: {e}")

    # Return to the main page
    driver.back()
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(3)  # Throttle requests


def user_interface():
    root = tk.Tk()
    root.withdraw()

    website_url = simpledialog.askstring("Input", "Enter the website URL to scrape:")
    if not website_url:
        print("No website URL provided. Exiting.")
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        print("No output folder selected. Exiting.")
        return

    scrape_articles(output_folder, website_url)


if __name__ == "__main__":
    try:
        user_interface()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Runs the second script that opens the local AI
import subprocess

if __name__ == "__main__":
    try:
        user_interface()  # Run the scraping script
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Run another script after this one finishes
        another_script = "rewriter.py"  # Replace with the path to your other script
        try:
            print(f"Running the next script: {another_script}")
            subprocess.run(["python", another_script], check=True)  # Run the other script
        except Exception as e:
            print(f"Failed to run {another_script}: {e}")
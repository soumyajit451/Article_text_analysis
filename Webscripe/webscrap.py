# -*- coding: utf-8 -*-
"""Webscrap.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lJ9S7T0XriVGvvUovFdE5iYXdo5Zg76V
"""

import requests,re,lxml
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

project_dir = '/content/drive/MyDrive/Blackcoffer/Data'

dir_path = os.path.join(project_dir)
if not os.path.exists(project_dir):
   os.makedirs(dir_path)
   print(f"Created directory: {dir_path}")
else:
   print(f"Directory already exists: {dir_path}")

df = pd.read_excel("Input.xlsx")
df

def extract_article_data(url):
    static_data_count = 0  # Counter for data points within this function

    def fetch_and_process_data():
        nonlocal static_data_count  # Access the outer counter

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")

        # Find the article title and content elements
        title = soup.find("h1", class_="entry-title")
        content = soup.find("div", class_="td-post-content tagdiv-type")

        # Remove unwanted content within <pre> tag
        unwanted_content = content.find("pre", class_="wp-block-preformatted")
        if unwanted_content:
            unwanted_content.decompose()

        if title and content:
            article_title = title.text.strip()
            article_text = content.get_text(separator='\n').strip()
            return article_title, article_text
        else:
            return None, None

    while True:  # Loop until data is successfully fetched
        result = fetch_and_process_data()
        if result is not None:
            return result

        static_data_count += 1
        if static_data_count % 5 == 0:  # Check for time lapse
            print("Pausing for 5 seconds within extract_article_data...")
            time.sleep(5)

for index, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]
    try:
        article_title, article_text = extract_article_data(url)

        if article_title and article_text:
            file_path = os.path.join(project_dir, f"{url_id}.txt")  # Construct full file path
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(article_title + "\n\n")
                f.write(article_text)
            print(f"Data saved to: {file_path}")
        else:
            print(f"Extraction failed for URL: {url}")

    except:
        print(f"Extraction failed for URL: {url}")

## I checked Manually , I found ther is some article not scrapped {14,10,29,36,43,49,83,84,92,99,100}
## reason there class are different
unscraped_url_ID = [
    "blackassign0014",
    "blackassign0020",
    "blackassign0029",
    "blackassign0036",
    "blackassign0043",
    "blackassign0049",
    "blackassign0083",
    "blackassign0084",
    "blackassign0092",
    "blackassign0099",
    "blackassign0100",
]

headers = {
    'authority': 'insights.blackcoffer.com',
    'method': 'GET',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,or;q=0.7,hi;q=0.6',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://colab.research.google.com/',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def extract_article_data1(url):
    static_data_count = 0  # Counter for data points within this function

    def fetch_and_process_data():
        nonlocal static_data_count  # Access the outer counter

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        # Find the article title and content elements
        title = soup.find("h1", class_="tdb-title-text")
        text = soup.findAll("div", class_="tdb-block-inner td-fix-index")
        # Remove unwanted content within <pre> tag
        unwanted_content = text.find("pre", class_="wp-block-preformatted")
        if unwanted_content:
            unwanted_content.decompose()


        if title and text:
            article_title = title.text.strip()
            html_content = ''.join(str(tag) for tag in text)
            soup_1 = BeautifulSoup(html_content, 'html.parser')
            paragraphs = soup_1.find_all('p')
            article_text = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
            return article_title, article_text
        else:
            return None, None

    while True:  # Loop until data is successfully fetched
        result = fetch_and_process_data()
        if result is not None:
            return result

        static_data_count += 1
        if static_data_count % 5 == 0:  # Check for time lapse
            print("Pausing for 4 seconds within extract_article_data...")
            time.sleep(4)

for index, row in df.iterrows():
    url_id = row["URL_ID"]
    if url_id in unscraped_url_ID:
        url = row["URL"]  # Retrieve the actual URL
        try:
            article_title, article_text = extract_article_data1(url)  # Pass the URL directly
            if article_title and article_text:
                file_path = os.path.join(project_dir, f"{url_id}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(article_title + "\n\n")
                    f.write(str(article_text))
                print(f"Data saved to: {file_path}")
            else:
                print(f"Extraction failed for URL: {url}")
        except:
            print(f"Extraction failed for URL: {url}")



 ####   I checked manually 36 and 49 url  is not opening.





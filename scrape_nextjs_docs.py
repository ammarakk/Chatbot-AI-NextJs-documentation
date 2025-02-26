import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nextjs_docs():
    base_url = "https://nextjs.org/docs"
    
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing Next.js documentation: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    topics = []

    # Extract all documentation links
    for link in soup.select("a"):
        topic = link.get_text(strip=True)
        doc_link = link.get("href")

        if not topic or not doc_link:
            continue
        
        if not doc_link.startswith("http"):
            doc_link = "https://nextjs.org" + doc_link
        
        # Fetch content from the page
        try:
            doc_response = requests.get(doc_link, timeout=10)
            doc_soup = BeautifulSoup(doc_response.text, "html.parser")
            
            # Extract the main content
            content = doc_soup.find("article")
            content_text = content.get_text(strip=True) if content else "Content not available."

        except requests.exceptions.RequestException:
            content_text = "Could not fetch content."

        topics.append({
            "keyword": topic.lower(),
            "description": topic,
            "content": content_text  # Store actual content
        })

    return topics

# Fetch documentation
doc_topics = scrape_nextjs_docs()

if doc_topics:
    df = pd.DataFrame(doc_topics)
    df.to_csv("nextjs_docs.csv", index=False, encoding="utf-8")
    print("✅ Next.js documentation CSV with content created successfully!")
else:
    print("❌ No data scraped. Check the website structure or internet connection.")

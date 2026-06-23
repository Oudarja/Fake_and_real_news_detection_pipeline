import requests
from bs4 import BeautifulSoup
from readability import Document
from .search_google import serach_google
from .retrieve_summarization import generate_summarization
import time
import re

def clean_summary(text):
    # Remove markdown headings and bold/italic symbols
    text = re.sub(r'\*\*|__|\*|-', '', text)
    
    # Replace multiple newlines and tabs with a single space
    text = re.sub(r'[\n\r\t]+', ' ', text)
    
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def scrape_related_text_and_summarize(test_news):
    related_links = serach_google(test_news)
    full_summarization = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/142.0.0.0 Safari/537.36"
    }

    for link in related_links:
        # Skip obvious non-HTML links
        if link.lower().endswith((".pdf", ".xml", ".doc", ".zip")):
            print(f"Skipping non-HTML link: {link}")
            continue

        try:
            response = requests.get(link, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch {link} (status {response.status_code})")
                continue

            # Remove NULL bytes / control characters
            html = response.text.replace("\x00", "")

            # Use Readability to extract main content
            try:
                doc = Document(html)
                main_content_html = doc.summary()
            except Exception as e:
                print(f"Error extracting main content from {link}: {e}")
                continue

            # Convert to plain text
            soup = BeautifulSoup(main_content_html, "html.parser")
            all_text = soup.get_text("\n")
            lines = [line.strip() for line in all_text.split("\n")]
            all_text = "\n".join(lines)
            if all_text:
                # Pass content argument explicitly to avoid missing parameter error
                summarized_description = generate_summarization(content=all_text)
                full_summarization.append(summarized_description)

            # Small delay to avoid overwhelming servers
            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing {link}: {e}")
            continue

    # Combine all summaries into a single string
    final_summarization = "\n".join(full_summarization)
    print(final_summarization)
    print(clean_summary(final_summarization))
    return clean_summary(final_summarization)


# text=input()
# scrape_related_text_and_summarize(text)





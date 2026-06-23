from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

TRUSTED_SITES = [
    # Top National Newspapers (Bangla)
    "prothomalo.com",
    "bdnews24.com",
    "jugantor.com",
    "kalerkantho.com",
    "samakal.com",
    "banglanews24.com",
    "ntvbd.com",
    "sangbad.net.bd",
    "bhorerkagoj.com",
    "ittefaq.com.bd",
    "dailynayadiganta.com",
    "dailyjanakantha.com",
    "dailyinqilab.com",
    "dainikamadershomoy.com",
    "manobkantha.com.bd",
    "dailyprobashirdiganta.com",
    "dainikshiksha.com",
    "dainikazadi.org",
    "bangladeshpost.net",
    "dailysangram.com",
    "dailyvorerpata.com",
    "dailyprotidinerbangladesh.com",
    "ourtimebd.com",

    # Online-Only Popular Portals
    "bdnews24bd.com",
    "barta24.com",
    "dhakapost.com",
    "dhakatribune.com",
    "duaa-news.com",
    "rtvonline.com",
    "themorningbellbd.com",
    "jagonews24.com",
    "risingbd.com",
    "sharebiz.net",
    "tbsnews.net",
    "thedailycampus.com",

    # English Newspapers
    "thedailystar.net",
    "newagebd.net",
    "observerbd.com",
    "thefinancialexpress.com.bd",
    "theindependentbd.com",
    "businesspostbd.com",
    "businessbangladesh.com.bd",
    "daily-sun.com",

    # TV Channel News Portals
    "somoynews.tv",
    "jamuna.tv",
    "channel24bd.tv",
    "independent24.com",
    "boishakhionline.com",
    "atntvnews.com",
    "desh.tv",
    "banglavision.tv",
    "nagorik.com",
    "maasranga.tv",

    # Additional Trusted BD Media
    "kalerkantho.com",
    "thebangladeshtoday.com",
    "dailyasianage.com",
    "dailybonikbarta.com",
    "mtnews24.com",
    "bd24live.com",
    "rumorscanner.com"
]


def scrape_google(query):
    options = Options()
    # options.add_argument("--headless")  # চাইলে ব্যাকগ্রাউন্ডে চালাও
    options.add_argument("--disable-blink-features=AutomationControlled")
    

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    driver.get(search_url)
    time.sleep(2)

    #  FULL PAGE HTML DUMP
    html = driver.page_source  

    driver.quit()

    # Parse HTML to extract links
    soup = BeautifulSoup(html, "html.parser")

    all_links = []

    # Collect ALL <a> tags from full page
    for tag in soup.find_all("a", href=True):
        link = tag['href']
        # Exclude Google redirects
        if link.startswith("http") and "google.com" not in link:
            all_links.append(link)

    # Remove duplicates
    all_links = list(set(all_links))

    # Filter trusted links
    trusted_links = []
    for link in all_links:
        domain = urlparse(link).netloc.lower().replace("www.", "")
        for site in TRUSTED_SITES:
            if site in domain:
                trusted_links.append(link)

    return all_links, trusted_links


if __name__ == "__main__":
    query = input("input your subject: ")
    print("\n Google html from google...\n")

    all_links, trusted_links = scrape_google(query)

    print(f" total link: {len(all_links)}")
    print(f"trusted link: {len(trusted_links)}\n")

    print(" all link:")
    for i, link in enumerate(all_links, 1):
        print(f"{i}. {link}")

    print("\n Trusted News Links:")
    for i, link in enumerate(trusted_links, 1):
        print(f"{i}. {link}")
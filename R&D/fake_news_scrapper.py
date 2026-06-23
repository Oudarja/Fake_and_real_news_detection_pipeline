# This script is for creating data set of fake news 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from llm_to_create_fake_news import generate_fake_news

def get_chrome_options():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    return options

def scrape_fake():

    url="https://rumorscanner.com/category/fact-check"
    driver = uc.Chrome(options=get_chrome_options())
    driver.get(url)
    driver.implicitly_wait(5)
    fake_news_items = set()

    try:
        cards= driver.find_elements(By.CLASS_NAME, "td-module-thumb")
        print(f"Found {len(cards)} news cards")
        for card in cards:
            try:
                # Find the inner <a> tag inside the container
                a_tag = card.find_element(By.TAG_NAME, "a")
                title = a_tag.get_attribute('title')
                link=a_tag.get_attribute("href")
            except Exception as e:
                print(f"No <a> found in this container: {e}")

             # Extract description
            try:
                driver1 = None
                try:
                    # driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=options)
                    driver1 = uc.Chrome(options=get_chrome_options())
                    driver1.set_page_load_timeout(20)  # Maximum time to wait for page load
                    driver1.get(link)

                    # Optional: wait a few seconds for JS content to load if needed
                    driver1.implicitly_wait(20)  # Not strictly necessary, but can help
                    # Scrape all <p> text
                    description_text = " ".join(
                        p.text.strip()
                        for p in driver1.find_elements(By.TAG_NAME, "p")
                        if p.text.strip()
                    )
                finally:
                    if driver1 is not None:
                        driver1.quit()

                fake_news=generate_fake_news(title,description_text[:100])
                fake_news_items.add(fake_news)
                time.sleep(0.5)
            except Exception as e:
                 print(f"An error occurred: {type(e).__name__} - {e}")

    except Exception as error:
        print(f"An error occurred: {type(error).__name__} - {error}")


    
    cnt=0

    
    while cnt<=99:
         # Locate the pagination container
        page_nav = driver.find_element(By.CSS_SELECTOR, ".page-nav.td-pb-padding-side")
        # Find all children (span and a tags) inside pagination
        children = page_nav.find_elements(By.XPATH, "./*")

        found_current = False
        next_link = None

        for child in children:
            if child.tag_name.lower() == "span" and "current" in child.get_attribute("class").split():
                # Found the current page
                found_current = True
            elif found_current and child.tag_name.lower() == "a":
                # The first <a> after current
                next_link = child.get_attribute("href")
                break

        driver.get(next_link)
        driver.implicitly_wait(5)

        try:
            cards= driver.find_elements(By.CLASS_NAME, "td-module-thumb")
            print(f"Found {len(cards)} news cards")
            
            for card in cards:
                try:
                    # Find the inner <a> tag inside the container
                    a_tag = card.find_element(By.TAG_NAME, "a")
                    title = a_tag.get_attribute('title')
                    link=a_tag.get_attribute("href")
                except Exception as e:
                    print(f"No <a> found in this container: {e}")
                
                  # Extract description
                try:
                    driver1 = None
                    try:
                        # driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                        driver1 = uc.Chrome(options=get_chrome_options())
                        driver1.set_page_load_timeout(20)  # Maximum time to wait for page load
                        driver1.get(link)

                        # Optional: wait a few seconds for JS content to load if needed
                        driver1.implicitly_wait(20)  # Not strictly necessary, but can help
                        # Scrape all <p> text
                        description_text = " ".join(
                            p.text.strip()
                            for p in driver1.find_elements(By.TAG_NAME, "p")
                            if p.text.strip()
                        )
                    finally:
                        if driver1 is not None:
                            driver1.quit() 

                    fake_news=generate_fake_news(title,description_text[:100])
                    fake_news_items.add(fake_news)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"An error occurred: {type(e).__name__} - {e}")

        except Exception as error:
            print(f"An error occurred: {type(error).__name__} - {error}")
        
        cnt=cnt+1
    
    driver.quit()

if __name__ == "__main__":
    scrape_fake()
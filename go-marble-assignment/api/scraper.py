from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_reviews(url):
    # Configure Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(r"C:\Users\Samath\Downloads\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)

    # Define CSS selectors (replace with dynamic LLM-generated selectors)
    css_selectors = {
        "Review Container": ".review",
        "Review Title": ".review-title",
        "Review Body": ".review-body",
        "Review Rating": ".review-rating",
        "Reviewer Name": ".reviewer-name",
        "Next Button": ".next-page"
    }

    # Extract review data
    review_data = []
    page_number = 1

    while True:
        print(f"Scraping page {page_number}...")

        # Wait for review containers to load
        wait = WebDriverWait(driver, 10)
        review_containers = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selectors["Review Container"]))
        )

        # Scrape reviews from the current page
        for review in review_containers:
            try:
                title = review.find_element(By.CSS_SELECTOR, css_selectors["Review Title"]).text
            except:
                title = "N/A"

            try:
                body = review.find_element(By.CSS_SELECTOR, css_selectors["Review Body"]).text
            except:
                body = "N/A"

            try:
                rating = review.find_element(By.CSS_SELECTOR, css_selectors["Review Rating"]).text
            except:
                rating = "N/A"

            try:
                reviewer = review.find_element(By.CSS_SELECTOR, css_selectors["Reviewer Name"]).text
            except:
                reviewer = "N/A"

            review_data.append({
                "title": title,
                "body": body,
                "rating": rating,
                "reviewer": reviewer
            })

        # Check if there is a "Next" button and click it
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, css_selectors["Next Button"])
            if "disabled" in next_button.get_attribute("class"):
                print("No more pages to scrape.")
                break
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            page_number += 1
        except:
            print("No more pages to scrape.")
            break

    driver.quit()
    return review_data
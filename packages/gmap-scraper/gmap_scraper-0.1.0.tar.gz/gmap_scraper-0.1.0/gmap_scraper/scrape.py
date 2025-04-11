

import streamlit as st
import json
import csv
import time
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_google_maps(keyword):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Optional: run in headless mode
    chrome_options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    results = []

    try:
        driver.get(f'https://www.google.com/maps/search/{keyword}/')

        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
        except Exception:
            pass

        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        driver.execute_script("""
            var scrollableDiv = arguments[0];
            function scrollWithinElement(scrollableDiv) {
                return new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    var distance = 1000;
                    var scrollDelay = 3000;

                    var timer = setInterval(() => {
                        var scrollHeightBefore = scrollableDiv.scrollHeight;
                        scrollableDiv.scrollBy(0, distance);
                        totalHeight += distance;

                        if (totalHeight >= scrollHeightBefore) {
                            totalHeight = 0;
                            setTimeout(() => {
                                var scrollHeightAfter = scrollableDiv.scrollHeight;
                                if (scrollHeightAfter > scrollHeightBefore) {
                                    return;
                                } else {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, scrollDelay);
                        }
                    }, 200);
                });
            }
            return scrollWithinElement(scrollableDiv);
        """, scrollable_div)

        items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

        for item in items:
            data = {}

            try:
                data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
            except:
                pass
            try:
                data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            except:
                pass
            try:
                data['website'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] div > a').get_attribute('href')
            except:
                pass
            try:
                rating_text = item.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span[role="img"]').get_attribute('aria-label')
                rating_numbers = [float(piece.replace(",", ".")) for piece in rating_text.split(" ") if piece.replace(",", ".").replace(".", "", 1).isdigit()]
                if rating_numbers:
                    data['stars'] = rating_numbers[0]
                    data['reviews'] = int(rating_numbers[1]) if len(rating_numbers) > 1 else 0
            except:
                pass
            try:
                text_content = item.text
                phone_pattern = r'((\+?\d{1,2}[ -]?)?(\(?\d{3}\)?[ -]?\d{3,4}[ -]?\d{4}|\(?\d{2,3}\)?[ -]?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}))'
                matches = re.findall(phone_pattern, text_content)
                phone_numbers = [match[0] for match in matches]
                unique_phone_numbers = list(set(phone_numbers))
                data['phone'] = unique_phone_numbers[0] if unique_phone_numbers else None
            except:
                pass

            if data.get('title'):
                results.append(data)

        # Save JSON
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Save CSV
        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link", "website", "stars", "reviews", "phone"])
            writer.writeheader()
            for row in results:
                writer.writerow(row)

        return "results.json", "results.csv", results

    finally:
        time.sleep(5)
        driver.quit()


st.set_page_config(page_title="Google Maps Scraper", layout="centered")
st.title("Google Maps Business Scraper")
keyword = st.text_input("Enter search keyword", "CA in Hyderabad India")

if st.button("Scrape"):
    with st.spinner("Scraping... Please wait."):
        json_file, csv_file, data = scrape_google_maps(keyword)
        st.success(f"Scraped {len(data)} entries!")

        with open(json_file, "rb") as jf:
            st.download_button("Download JSON", jf, file_name="results.json", mime="application/json")
        with open(csv_file, "rb") as cf:
            st.download_button("Download CSV", cf, file_name="results.csv", mime="text/csv")

        
        if data:
            st.subheader("Sample Result")
            st.json(data[0])

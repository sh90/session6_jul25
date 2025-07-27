import csv
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# --- Setup Selenium ---
browser = webdriver.Firefox()
browser.get('https://www.amazon.in')
browser.maximize_window()

# --- Search for Product ---
search_box = browser.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys("Smartphones under 10000")
search_box.send_keys(Keys.RETURN)


# --- Wait until results load ---
# WebDriverWait(browser, ).until(
#     EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
# )

time.sleep(5)
# --- Scrape products ---
products = browser.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
print(len(products))
scraped_data = []

for i, product in enumerate(products[3:10]):

    #product.get_attribute("innerHTML"))
    try:
        # --- Title ---
        try:
            title_elem = product.find_element(By.XPATH, ".//h2/span")
            title = title_elem.text.strip()
        except:
            title = "N/A"

        # --- Link ---
        try:
            link_elem = product.find_element(By.XPATH, ".//a[contains(@class, 'a-link-normal') and contains(@href, '/dp/')]")
            link = link_elem.get_attribute("href")
        except:
            link = "N/A"

        # --- Price ---
        try:
            price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            price = f"₹{price_whole}.{price_fraction}"
        except:
            try:
                price = product.find_element(By.XPATH, ".//span[@class='a-price']").text.strip()
            except:
                price = "N/A"


        # --- Print to console ---
        print(f"{i+1}. {title}\n   Price: {price} |  Link: {link}\n")

        # --- Save to list for CSV ---
        scraped_data.append({
            "Title": title,
            "Price": price,
            "Link": link
        })

    except Exception as e:
        print(f"Error parsing product {i}: {e}")

# --- Save to CSV ---
csv_file = "amazon_products.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Price","Link"])
    writer.writeheader()
    writer.writerows(scraped_data)

print(f"\n✅ Saved {len(scraped_data)} products to {csv_file}")

# --- Optional: close browser ---
# browser.quit()

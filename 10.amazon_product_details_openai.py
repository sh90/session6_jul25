from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import data_info



browser = webdriver.Firefox()
browser.get('https://www.amazon.in')
browser.maximize_window()

# Search for products
search_box = browser.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys("Smartphones under 10000")
search_box.send_keys(Keys.RETURN)

WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
)

products = browser.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

for i, product in enumerate(products[:2]):
    try:
        # 🟡 Get full HTML of the product element
        product_html = product.get_attribute("outerHTML")

        # 🟢 Send to GPT-4o-mini
        prompt = f"""
        The following is an HTML block of a product from Amazon. Analyze and extract:
        - Product title
        - Price (in ₹)
        - Brand
        - URL/Link
        - Rating
        
        HTML:
        {product_html}
        """

        client = OpenAI(api_key=data_info.open_ai_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=0,
        )

        gpt_response = response.output_text
        print(f"\nProduct {i+1} Analysis:\n{gpt_response}\n{'-'*80}")

    except Exception as e:
        print(f"Error analyzing product {i+1}: {e}")

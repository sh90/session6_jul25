# pip install google-search-results
from serpapi import GoogleSearch
import data_info

# Replace with your actual SerpAPI key
api_key = data_info.SERPE_API_KEY

# Define the search parameters
params = {
    "engine": "amazon",
    "amazon_domain": "amazon.in",   # or amazon.in, amazon.co.uk, etc.
    "k": "Smartphones under 10000",
    "api_key": api_key
}

# Execute the search
search = GoogleSearch(params)
results = search.get_dict()

# Print product titles and prices
for product in results.get("organic_results", []):
    title = product.get("title")
    price = product.get("price")
    link = product.get("link")
    print(f"Title: {title}\nPrice: {price}\nLink: {link}\n")

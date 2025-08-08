import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# CONFIG
DOMAIN = "example.com"  # Change to your Trustpilot domain
PAGES_TO_SCRAPE = 27     # Number of pages of reviews to grab

BASE_URL = f"https://uk.trustpilot.com/review/ukstoragecompany.co.uk/{DOMAIN}?page={{}}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

all_reviews = []

for page in range(1, PAGES_TO_SCRAPE + 1):
    url = BASE_URL.format(page)
    print(f"Scraping: {url}")
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    for review in soup.select("section.styles_reviewCard__hcAvl"):
        title = review.select_one("h2").get_text(strip=True) if review.select_one("h2") else ""
        body = review.select_one("p").get_text(strip=True) if review.select_one("p") else ""
        rating_tag = review.select_one("div.star-rating img")
        rating = rating_tag["alt"] if rating_tag else ""
        date_tag = review.select_one("time")
        date = date_tag["datetime"] if date_tag else ""
        all_reviews.append({
            "Title": title,
            "Body": body,
            "Rating": rating,
            "Date": date
        })

# Save to Excel
filename = f"trustpilot_reviews_{datetime.date.today()}.xlsx"
df = pd.DataFrame(all_reviews)
df.to_excel(filename, index=False)
print(f"✅ Saved {filename}")

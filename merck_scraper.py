import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.merck.com/wp-json/wp/v2/news_item/?per_page=10&page=1&tags=289"
params = {
    "page": 1,
    "per_page": 10
}
response = requests.get(url, params=params)
data = response.json()

merck_press_release_data = []
for item in data:
    title = item['title']['rendered']
    date = item['date']
    link = item['link']
    # excerpt = item['excerpt']
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Link: {link}")
    # print(f"Excerpt: {excerpt}")
    print("---")
    
    merck_press_release_data.append({
            'Title': title,
            'Date': date,
            'Link': link,
        })

merck_press_release_df = pd.DataFrame(merck_press_release_data)
save_to_excel(merck_press_release_df, "merck_press_releases.xlsx")
print(merck_press_release_df)

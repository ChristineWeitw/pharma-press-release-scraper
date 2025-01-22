import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.pfizer.com/newsroom/press-releases?page=2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

press_release_data = []

# Find all press release items
press_release_items = soup.find_all('li', class_='grid-x')

for item in press_release_items:
    date = item.find('p', class_='date')
    title = item.find('h5')
    link = item.find('a')
    categories = item.find_all('a', class_='tag tag--primary')
    
    if date and title and link:
        date_text = date.text.strip()
        title_text = title.text.strip()
        link_href = 'https://www.pfizer.com' + link['href']
        categories_text = ', '.join([tag.text.strip() for tag in categories]) if categories else ''
        
        press_release_data.append({
            'Date': date_text,
            'Title': title_text,
            'Link': link_href,
            'Categories': categories_text
        })

press_release_df = pd.DataFrame(press_release_data)
save_to_excel(press_release_df, "pfizer_press_releases.xlsx")
print(press_release_df)

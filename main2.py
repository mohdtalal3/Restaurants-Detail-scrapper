from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import requests
# Create an HTML session and get the webpage content
session = HTMLSession()
r = session.get("https://www.visitomaha.com/listings/gather-in-omaha/66943/")

# Render the page
r.html.render()

soup = BeautifulSoup(r.html.raw_html, "html.parser")
detail_top = soup.find('div', class_='detail-top')

if detail_top:
    h1_tag = detail_top.find('div', class_='info-section').find('h1')
    text = h1_tag.get_text()
    print(text)
    info_list = detail_top.find('ul', class_='info-list')
    # Fetch the region
    region_label = info_list.find('span', class_='meta-label', text='Region:')
    region = region_label.next_sibling.strip() if region_label else None

    # Fetch the address
    street_address = info_list.find('span', class_='street-address').get_text() if info_list.find('span', class_='street-address') else None
    city_state_zip = info_list.find('span', class_='city-state-zip').get_text() if info_list.find('span', class_='city-state-zip') else None
    full_address = f"{street_address}, {city_state_zip}" if street_address and city_state_zip else None
    email = info_list.find('a', href=lambda href: href and "mailto:" in href).get_text() if info_list.find('a', href=lambda href: href and "mailto:" in href) else None

    # Fetch the telephone number
    phone = info_list.find('a', href=lambda href: href and "tel:" in href).get_text().strip() if info_list.find('a', href=lambda href: href and "tel:" in href) else None
    description_div = detail_top.find('div', class_='description hide-expander')
    content_div = description_div.find('div', class_='content')
    # Extract and print the text content inside the content_div
    if content_div:
        content_text = content_div.get_text(strip=True)
        print(content_text)
    else:
        print("Content not found")
    print("Region:", region)
    print("Address:", full_address)
    print("Telephone:", phone)
    print("Email:", email)
else:
    print("Detail section not found")

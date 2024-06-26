from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import requests
# Create an HTML session and get the webpage content
session = HTMLSession()
r = session.get("https://www.visitomaha.com/listings/spaghetti-works-ralston/57221/")

# Render the page
r.html.render()

soup = BeautifulSoup(r.html.raw_html, "html.parser")
detail_top = soup.find('div', class_='detail-top')

if detail_top:
    h1_tag = detail_top.find('div', class_='info-section').find('h1')
    title = h1_tag.get_text()
    info_list = detail_top.find('ul', class_='info-list')
    region_label = info_list.find('span', class_='meta-label', string='Region:')
    region = region_label.next_sibling.strip() if region_label else None
    street_address = info_list.find('span', class_='street-address').get_text() if info_list.find('span', class_='street-address') else None
    city_state_zip = info_list.find('span', class_='city-state-zip').get_text() if info_list.find('span', class_='city-state-zip') else None
    full_address = f"{street_address}, {city_state_zip}" if street_address and city_state_zip else None
    email = info_list.find('a', href=lambda href: href and "mailto:" in href).get_text().strip() if info_list.find('a', href=lambda href: href and "mailto:" in href) else None
    phone = info_list.find('a', href=lambda href: href and "tel:" in href).get_text().strip() if info_list.find('a', href=lambda href: href and "tel:" in href) else None
    about_section = soup.find('div', class_='description').find('div', class_='content').get_text().strip()

else:
    print("Detail section not found")

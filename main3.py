import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sqlite3
import time

# Establish SQLite3 connection and cursor
conn = sqlite3.connect('gather_in_omaha.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        region TEXT,
        full_address TEXT,
        email TEXT,
        phone TEXT,
        about TEXT
    )
''')

# Read CSV file using Pandas
df = pd.read_csv('full_urls.csv')
c = 0

# Function to fetch and parse data from URL
def fetch_data(url):
    session = HTMLSession()
    global c
    c = c + 1
    if c == 20:
        time.sleep(40)
        c = 0
    try:
        r = session.get(url)
        r.html.render(sleep=4)  # Render the JavaScript content
    except Exception as e:
        print(f"MaxRetries exception occurred: {e}. Retrying after 60 seconds...")
        time.sleep(90)
        r = session.get(url)
        r.html.render(sleep=4)  # Retry rendering after sleeping
    print(url)
    soup = BeautifulSoup(r.html.raw_html, "html.parser")

    detail_top = soup.find('div', class_='detail-top')

    # Initialize variables with default values
    title = None
    region = None
    full_address = None
    email = None
    phone = None
    about_section = None
    street_address=None
    city_state_zip=None
    if detail_top:
        try:
            h1_tag = detail_top.find('div', class_='info-section').find('h1')
            title = h1_tag.get_text() if h1_tag else None
        except Exception as e:
            print(f"No title: {e}")

        info_list = detail_top.find('ul', class_='info-list')
        try:
            region_label = info_list.find('span', class_='meta-label', string='Region:')
            region = region_label.next_sibling.strip() if region_label else None
        except Exception as e:
            print(f"No region: {e}")

        try:
            street_address_tag = info_list.find('span', class_='street-address')
            street_address = street_address_tag.get_text().strip() if street_address_tag else None
        except Exception as e:
            print(f"No street address: {e}")

        try:
            city_state_zip_tag = info_list.find('span', class_='city-state-zip')
            city_state_zip = city_state_zip_tag.get_text().strip() if city_state_zip_tag else None
        except Exception as e:
            print(f"No city/state/zip: {e}")
        try:
            full_address = f"{street_address}, {city_state_zip}" if street_address and city_state_zip else None
        except:
            print("No address")
        try:
            email_tag = info_list.find('a', href=lambda href: href and "mailto:" in href)
            email = email_tag.get_text().strip() if email_tag else None
        except Exception as e:
            print(f"No email: {e}")

        try:
            phone_tag = info_list.find('a', href=lambda href: href and "tel:" in href)
            phone = phone_tag.get_text().strip() if phone_tag else None
        except Exception as e:
            print(f"No phone number: {e}")

        try:
            about_section_tag = soup.find('div', class_='description').find('div', class_='content')
            about_section = about_section_tag.get_text().strip() if about_section_tag else None
        except Exception as e:
            print(f"No about section: {e}")

        # Insert into SQLite3 database
        cursor.execute('''
            INSERT INTO listings (title, region, full_address, email, phone, about)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, region, full_address, email, phone, about_section))

        conn.commit()
    else:
        print(f"Detail section not found for URL: {url}")

# Iterate over each row in the DataFrame and fetch data
for index, row in df.iterrows():
    link = row['links']
    fetch_data(link)

# Close SQLite3 connection
conn.close()

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time

session = HTMLSession()
count = 0
main_list = []

while count <= 696:
    try:
        r = session.get(f"https://www.visitomaha.com/restaurants/?skip={count}&bounds=false&view=list&sort=qualityScore")
        print(count)
        
        # Check if the response status code is 200
        if r.status_code == 200:
            # Render the page
            r.html.render(sleep=3)
            
            # Check if the render is successful
            if r.html.raw_html is not None:
                soup = BeautifulSoup(r.html.raw_html, "html.parser")
                content_list = soup.find('div', class_='content list')
                
                # Find all h4 tags within the content list
                h4_tags = content_list.find_all('h4')
                
                # Extract all href attributes from the a tags within those h4 tags
                hrefs = [a_tag['href'] for h4 in h4_tags for a_tag in h4.find_all('a')]
                main_list.extend(hrefs)
                count += 12
            else:
                raise Exception("Rendering the page returned None")
        else:
            raise Exception(f"Failed to retrieve the page, status code: {r.status_code}")
    except Exception as e:
        print("Count has a problem")
        print(f"Count: {count}, Error: {e}")

# Save raw links to a CSV file
df = pd.DataFrame(main_list, columns=["links"])
df.to_csv("links.csv", index=False)
print("Data saved to links.csv")

# Prepend the base URL to each element in the list
full_urls = ["https://www.visitomaha.com" + url for url in main_list]

# Create a DataFrame from the list
df = pd.DataFrame(full_urls, columns=["URLs"])

# Save the DataFrame as a CSV file
df.to_csv("urls.csv", index=False)
print("Data saved to urls.csv")

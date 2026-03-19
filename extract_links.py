import requests
from bs4 import BeautifulSoup
import os

url_sub="https://skilltechonline.com/ac-brackets/ac-bracket/"
def extract_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Looking for links that are likely product links
    # On many sites they are inside a product card or have a specific class
    # Based on the user's example, they look like: https://skilltechonline.com/tablet-mounts/tablet-mounts/slug/
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Normalize relative links
        if href.startswith('/'):
            href = 'https://skilltechonline.com' + href
        
        if url_sub in href:
            # Avoid the category page itself
            path = href.replace(url_sub, '').strip('/')
            if path and '/' not in path: # It's a direct product link
                links.append(href)
    
    return sorted(list(set(links)))

def main():
    target_url = url_sub
    product_links = extract_links(target_url)
    
    print(f"Found {len(product_links)} product links:")
    for link in product_links:
        print(link)

    # Save to file
    with open('tablet_mount_urls.txt', 'w') as f:
        for link in product_links:
            f.write(link + '\n')

if __name__ == "__main__":
    main()

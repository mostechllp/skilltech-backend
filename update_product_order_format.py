import os
import django
import requests
from bs4 import BeautifulSoup
import sys
from decimal import Decimal

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import SubCategory, Product

def normalize(s):
    return "".join(s.split()).upper()

def sync_and_format_all():
    subcategories = SubCategory.objects.all()
    print(f"Starting full synchronization and reformatting for {subcategories.count()} subcategories...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    total_matched = 0

    for sc in subcategories:
        if not sc.category:
            continue

        # Construct live URL
        url = f"https://skilltechonline.com/{sc.category.slug}/{sc.slug}/"
        print(f"\nFetching {sc.name} from {url}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"  Failed to fetch (Status: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            product_divs = soup.select('.new-product-list')
            
            if not product_divs:
                print(f"  No products found on live page.")
                continue

            print(f"  Found {len(product_divs)} products on live site. Matching...")
            
            local_products = list(Product.objects.filter(subcategory=sc))
            
            # 1. Reset orders for this subcategory
            for lp in local_products:
                lp.order = Decimal('90.000')
                lp.save()

            # 2. First Pass: Sync based on live position
            sub_matched = 0
            for index, div in enumerate(product_divs):
                h3 = div.find('h3')
                if not h3: continue
                
                sku_span = h3.find('span', class_='sku')
                live_sku = sku_span.get_text().strip().upper() if sku_span else ""
                live_title = h3.get_text().strip().upper()
                
                matched_lp = None
                
                # Priority 1: Match by SKU exactly (normalized)
                if live_sku:
                    norm_live_sku = normalize(live_sku)
                    for lp in local_products:
                        if normalize(lp.name) == norm_live_sku:
                            matched_lp = lp
                            break
                
                # Priority 2: Match if local product name is in the live title (normalized)
                if not matched_lp:
                    for lp in local_products:
                        if normalize(lp.name) in normalize(live_title):
                            matched_lp = lp
                            break
                
                if matched_lp:
                    matched_lp.order = Decimal(index + 1)
                    matched_lp.save()
                    sub_matched += 1

            # 3. Second Pass: Reformat to 0.100, 0.200, 0.300...
            ordered_products = Product.objects.filter(subcategory=sc).order_by('order', 'name')
            for i, p in enumerate(ordered_products):
                new_val = Decimal(str(round((i + 1) * 0.1, 3))).quantize(Decimal('0.000'))
                p.order = new_val
                p.save()

            print(f"  Successfully synced and reformatted {sub_matched} products.")
            total_matched += sub_matched

        except Exception as e:
            print(f"  Error processing {sc.name}: {e}")

    print(f"\nFinished. Total products synchronized: {total_matched}")

if __name__ == "__main__":
    sync_and_format_all()

import sys
import os
import argparse

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
import requests
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Product

def translate_text(text, source_lang='en', target_lang='ar'):
    if not text:
        return ''
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={requests.utils.quote(text)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        parts = response.json()[0]
        translated = ''.join([part[0] for part in parts if part and part[0]])
        return translated
    except Exception as e:
        print(f"❌ Error translating: {e}")
        return None

def run():
    parser = argparse.ArgumentParser(description="Translate products to Arabic.")
    parser.add_argument("--limit", type=int, default=0, help="Max number of products to process (0 for unlimited)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay in seconds between translation requests")
    args = parser.parse_args()

    # Find products that need translation (at least one of the Arabic fields is missing)
    products = Product.objects.filter(
        django.db.models.Q(title_ar__isnull=True) | django.db.models.Q(title_ar="") |
        django.db.models.Q(short_description_ar__isnull=True) | django.db.models.Q(short_description_ar="") |
        django.db.models.Q(description_ar__isnull=True) | django.db.models.Q(description_ar="") |
        django.db.models.Q(tags_ar__isnull=True) | django.db.models.Q(tags_ar="")
    ).order_by('id')
    
    total_count = products.count()
    print(f"Found {total_count} products needing translation.")
    
    limit = args.limit
    if limit > 0:
        products = products[:limit]
        print(f"Limiting execution to the first {limit} products.")
        
    updated_count = 0
    failed_count = 0
    
    for idx, product in enumerate(products, 1):
        print(f"\n[{idx}/{products.count() if limit > 0 else total_count}] Processing Product ID {product.id} ({product.name})")
        modified = False
        
        # 1. Translate Title
        if not product.title_ar and product.title:
            print(f"  - Translating Title: '{product.title[:40]}...'")
            trans = translate_text(product.title)
            if trans:
                product.title_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)  # Cooldown on failure
                
        # 2. Translate Short Description
        if not product.short_description_ar and product.short_description:
            print(f"  - Translating Short Description: '{product.short_description[:40]}...'")
            trans = translate_text(product.short_description)
            if trans:
                product.short_description_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)
                
        # 3. Translate Description
        if not product.description_ar and product.description:
            print(f"  - Translating Description: '{product.description[:40]}...'")
            trans = translate_text(product.description)
            if trans:
                product.description_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)
                
        # 4. Translate Tags
        if not product.tags_ar and product.tags:
            print(f"  - Translating Tags: '{product.tags[:40]}...'")
            trans = translate_text(product.tags)
            if trans:
                product.tags_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)

        if modified:
            product.save()
            updated_count += 1
            print(f"  ✅ Saved Product {product.id}")
            
    print(f"\n🎉 Translation pass complete. Updated: {updated_count}, Failed fields: {failed_count}")

if __name__ == "__main__":
    run()

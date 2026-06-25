import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
import requests
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Gallery

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
        print(f"❌ Error translating '{text[:30]}...': {e}")
        return None

def run():
    gallery_items = Gallery.objects.all()
    print(f"Found {gallery_items.count()} gallery items to process.")
    
    cache = {}
    updated_count = 0
    for item in gallery_items:
        modified = False
        
        # Translate Title
        if not item.title_ar and item.title:
            clean_title = item.title.strip()
            if not clean_title:
                continue
                
            if clean_title in cache:
                translated = cache[clean_title]
            else:
                print(f"Translating Title for Gallery ID {item.id}: '{clean_title}'...")
                translated = translate_text(clean_title)
                if translated:
                    cache[clean_title] = translated
                    time.sleep(0.5)
            
            if translated:
                item.title_ar = translated
                modified = True
                print(f"  └─ Applied: '{clean_title}' -> '{translated}'")

        if modified:
            item.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} gallery items.")

if __name__ == "__main__":
    run()

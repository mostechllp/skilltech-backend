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

from catalog.models import Catalogue

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
    catalogues = Catalogue.objects.all()
    print(f"Found {catalogues.count()} catalogues to process.")
    
    updated_count = 0
    for cat in catalogues:
        modified = False
        
        # Translate Title
        if not cat.title_ar and cat.title:
            print(f"Translating Title for Catalogue ID {cat.id}: '{cat.title}'...")
            translated = translate_text(cat.title)
            if translated:
                cat.title_ar = translated
                modified = True
                print(f"  └─ Success: '{cat.title}' -> '{translated}'")
                time.sleep(0.5)

        if modified:
            cat.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} catalogues.")

if __name__ == "__main__":
    run()

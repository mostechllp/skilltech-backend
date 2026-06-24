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

from catalog.models import GlobalLocation

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
    locations = GlobalLocation.objects.all()
    print(f"Found {locations.count()} global locations to process.")
    
    updated_count = 0
    for loc in locations:
        modified = False
        
        # Translate Country
        if not loc.country_ar and loc.country:
            print(f"Translating Country for Location ID {loc.id}: '{loc.country}'...")
            translated = translate_text(loc.country)
            if translated:
                loc.country_ar = translated
                modified = True
                print(f"  └─ Success: '{loc.country}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Address
        if not loc.address_ar and loc.address:
            print(f"Translating Address for Location ID {loc.id} (length: {len(loc.address)})...")
            translated = translate_text(loc.address)
            if translated:
                loc.address_ar = translated
                modified = True
                print(f"  └─ Success Address")
                time.sleep(0.5)

        if modified:
            loc.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} global locations.")

if __name__ == "__main__":
    run()

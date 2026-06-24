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

from catalog.models import SiteSettings

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
    settings = SiteSettings.objects.all()
    print(f"Found {settings.count()} site settings records to process.")
    
    updated_count = 0
    for s in settings:
        modified = False
        
        # Translate Address Heading (translate if it's the English default or empty)
        if not s.address_heading_ar or s.address_heading_ar == "Our Office" or s.address_heading_ar == s.address_heading:
            print(f"Translating Address Heading for SiteSettings ID {s.id}: '{s.address_heading}'...")
            translated = translate_text(s.address_heading)
            if translated:
                s.address_heading_ar = translated
                modified = True
                print(f"  └─ Success: '{s.address_heading}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Address
        if not s.address_ar or s.address_ar == s.address:
            print(f"Translating Address for SiteSettings ID {s.id} (length: {len(s.address)})...")
            translated = translate_text(s.address)
            if translated:
                s.address_ar = translated
                modified = True
                print(f"  └─ Success Address")
                time.sleep(0.5)

        if modified:
            s.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} site settings records.")

if __name__ == "__main__":
    run()

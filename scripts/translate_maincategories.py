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

from catalog.models import MainCategory

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
    main_categories = MainCategory.objects.all()
    print(f"Found {main_categories.count()} main categories to process.")
    
    updated_count = 0
    for mc in main_categories:
        modified = False
        
        # Translate Name
        if not mc.name_ar and mc.name:
            print(f"Translating Name for Main Category ID {mc.id}: '{mc.name}'...")
            translated = translate_text(mc.name)
            if translated:
                mc.name_ar = translated
                modified = True
                print(f"  └─ Success: '{mc.name}' -> '{translated}'")
                time.sleep(0.5)

        if modified:
            mc.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} main categories.")

if __name__ == "__main__":
    run()

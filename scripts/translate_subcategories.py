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

from catalog.models import SubCategory

def translate_text(text, source_lang='en', target_lang='ar'):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={requests.utils.quote(text)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        translated = response.json()[0][0][0]
        return translated
    except Exception as e:
        print(f"❌ Error translating '{text}': {e}")
        return None

def run():
    subcategories = SubCategory.objects.all()
    print(f"Found {subcategories.count()} subcategories to process.")
    
    updated_count = 0
    for subcategory in subcategories:
        # Check if already translated or we want to overwrite
        if not subcategory.name_ar:
            print(f"Translating SubCategory ID {subcategory.id}: '{subcategory.name}'...")
            translated_name = translate_text(subcategory.name)
            
            if translated_name:
                subcategory.name_ar = translated_name
                subcategory.save()
                print(f"  └─ Success: '{subcategory.name}' -> '{translated_name}'")
                updated_count += 1
                # Small sleep to avoid rate limiting
                time.sleep(0.5)
            else:
                print(f"  └─ Failed to translate '{subcategory.name}'")
        else:
            print(f"SubCategory ID {subcategory.id} '{subcategory.name}' already has Arabic name: '{subcategory.name_ar}'")

    print(f"\n✅ Translation run complete. Updated {updated_count} subcategories.")

if __name__ == "__main__":
    run()

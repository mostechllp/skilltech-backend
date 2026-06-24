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

from catalog.models import Category

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
    categories = Category.objects.all()
    print(f"Found {categories.count()} categories to process.")
    
    updated_count = 0
    for category in categories:
        # Check if already translated or we want to overwrite
        if not category.name_ar:
            print(f"Translating Category ID {category.id}: '{category.name}'...")
            translated_name = translate_text(category.name)
            
            if translated_name:
                category.name_ar = translated_name
                category.save()
                print(f"  └─ Success: '{category.name}' -> '{translated_name}'")
                updated_count += 1
                # Small sleep to avoid rate limiting
                time.sleep(0.5)
            else:
                print(f"  └─ Failed to translate '{category.name}'")
        else:
            print(f"Category ID {category.id} '{category.name}' already has Arabic name: '{category.name_ar}'")

    print(f"\n✅ Translation run complete. Updated {updated_count} categories.")

if __name__ == "__main__":
    run()

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

from catalog.models import HomeStatistic

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
    stats = HomeStatistic.objects.all()
    print(f"Found {stats.count()} statistics to process.")
    
    updated_count = 0
    for stat in stats:
        modified = False
        
        # Translate Label
        if not stat.label_ar and stat.label:
            print(f"Translating Label for Stat ID {stat.id}: '{stat.label}'...")
            translated = translate_text(stat.label)
            if translated:
                stat.label_ar = translated
                modified = True
                print(f"  └─ Success: '{stat.label}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Value (override)
        if not stat.value_ar and stat.value is not None:
            val_str = str(stat.value)
            print(f"Translating Value for Stat ID {stat.id}: '{val_str}'...")
            translated_val = translate_text(val_str)
            if translated_val:
                stat.value_ar = translated_val
                modified = True
                print(f"  └─ Success: '{val_str}' -> '{translated_val}'")
                time.sleep(0.5)

        if modified:
            stat.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} statistics.")

if __name__ == "__main__":
    run()

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

from catalog.models import ProductBulletFeature

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
    parser = argparse.ArgumentParser(description="Translate product bullet features to Arabic.")
    parser.add_argument("--limit", type=int, default=0, help="Max number of bullet features to process (0 for unlimited)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay in seconds between translation requests")
    args = parser.parse_args()

    # Find bullet features needing translation
    features = ProductBulletFeature.objects.filter(
        django.db.models.Q(title_ar__isnull=True) | django.db.models.Q(title_ar="") |
        django.db.models.Q(text_ar__isnull=True) | django.db.models.Q(text_ar="")
    ).order_by('id')
    
    total_count = features.count()
    print(f"Found {total_count} bullet features needing translation.")
    
    limit = args.limit
    if limit > 0:
        features = features[:limit]
        print(f"Limiting execution to the first {limit} bullet features.")
        
    updated_count = 0
    failed_count = 0
    
    for idx, feature in enumerate(features, 1):
        modified = False
        
        # 1. Translate Title
        if not feature.title_ar and feature.title:
            print(f"[{idx}/{features.count() if limit > 0 else total_count}] Feature ID {feature.id} - Translating Title: '{feature.title[:30]}...'")
            trans = translate_text(feature.title)
            if trans:
                feature.title_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)  # Cooldown
                
        # 2. Translate Text
        if not feature.text_ar and feature.text:
            print(f"[{idx}/{features.count() if limit > 0 else total_count}] Feature ID {feature.id} - Translating Text: '{feature.text[:30]}...'")
            trans = translate_text(feature.text)
            if trans:
                feature.text_ar = trans
                modified = True
                time.sleep(args.delay)
            else:
                failed_count += 1
                time.sleep(3)  # Cooldown

        if modified:
            feature.save()
            updated_count += 1
            
    print(f"\n🎉 Translation pass complete. Updated: {updated_count}, Failed fields: {failed_count}")

if __name__ == "__main__":
    run()

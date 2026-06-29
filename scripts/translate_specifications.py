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

from catalog.models import ProductSpecification

# Translation cache to avoid translating same terms repeatedly
translation_cache = {}

def translate_text_with_cache(text, source_lang='en', target_lang='ar', delay=0.5):
    if not text:
        return ''
    
    # Check cache first
    cleaned_text = text.strip()
    if cleaned_text in translation_cache:
        return translation_cache[cleaned_text]
        
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={requests.utils.quote(cleaned_text)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        parts = response.json()[0]
        translated = ''.join([part[0] for part in parts if part and part[0]])
        
        # Populate cache
        translation_cache[cleaned_text] = translated
        
        # Respect the rate-limit delay
        time.sleep(delay)
        return translated
    except Exception as e:
        print(f"❌ Error translating '{cleaned_text}': {e}")
        return None

def run():
    parser = argparse.ArgumentParser(description="Translate product specifications to Arabic.")
    parser.add_argument("--limit", type=int, default=0, help="Max number of specifications to process (0 for unlimited)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay in seconds between translation API requests")
    args = parser.parse_args()

    # Find specifications needing translation
    specs = ProductSpecification.objects.filter(
        django.db.models.Q(key_ar__isnull=True) | django.db.models.Q(key_ar="") |
        django.db.models.Q(value_ar__isnull=True) | django.db.models.Q(value_ar="")
    ).order_by('id')
    
    total_count = specs.count()
    print(f"Found {total_count} specifications needing translation.")
    
    limit = args.limit
    if limit > 0:
        specs = specs[:limit]
        print(f"Limiting execution to the first {limit} specifications.")
        
    updated_count = 0
    api_calls_count = 0
    failed_count = 0
    
    # Pre-populate cache with already translated terms from database to resume efficiently
    print("Pre-populating translation cache from database...")
    existing_specs = ProductSpecification.objects.exclude(
        key_ar__isnull=True, value_ar__isnull=True
    ).exclude(
        key_ar="", value_ar=""
    )
    for s in existing_specs:
        if s.key and s.key_ar:
            translation_cache[s.key.strip()] = s.key_ar
        if s.value and s.value_ar:
            translation_cache[s.value.strip()] = s.value_ar
    print(f"Cache pre-populated with {len(translation_cache)} unique translations.")

    for idx, spec in enumerate(specs, 1):
        modified = False
        
        # 1. Translate Key
        if not spec.key_ar and spec.key:
            # Check if key is already in cache
            cleaned_key = spec.key.strip()
            if cleaned_key in translation_cache:
                spec.key_ar = translation_cache[cleaned_key]
                modified = True
            else:
                print(f"[{idx}/{specs.count() if limit > 0 else total_count}] Spec ID {spec.id} - Translating Key: '{cleaned_key}'")
                api_calls_count += 1
                trans = translate_text_with_cache(spec.key, delay=args.delay)
                if trans:
                    spec.key_ar = trans
                    modified = True
                else:
                    failed_count += 1
                    time.sleep(3) # Cooldown on error
                
        # 2. Translate Value
        if not spec.value_ar and spec.value:
            cleaned_val = spec.value.strip()
            if cleaned_val in translation_cache:
                spec.value_ar = translation_cache[cleaned_val]
                modified = True
            else:
                print(f"[{idx}/{specs.count() if limit > 0 else total_count}] Spec ID {spec.id} - Translating Value: '{cleaned_val}'")
                api_calls_count += 1
                trans = translate_text_with_cache(spec.value, delay=args.delay)
                if trans:
                    spec.value_ar = trans
                    modified = True
                else:
                    failed_count += 1
                    time.sleep(3) # Cooldown on error

        if modified:
            spec.save()
            updated_count += 1
            if idx % 100 == 0:
                print(f"  Processed {idx} records (Cache hits utilized)...")
            
    print(f"\n🎉 Translation pass complete.")
    print(f"  - Total records processed: {updated_count}")
    print(f"  - Total external translation API calls made: {api_calls_count}")
    print(f"  - Cache hits: {updated_count * 2 - api_calls_count}")
    print(f"  - Failed fields: {failed_count}")

if __name__ == "__main__":
    run()

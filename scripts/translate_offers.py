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

from catalog.models import Offer

def translate_text(text, source_lang='en', target_lang='ar'):
    if not text:
        return ''
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
    offers = Offer.objects.all()
    print(f"Found {offers.count()} offers to process.")
    
    updated_count = 0
    for offer in offers:
        modified = False
        
        # Translate Title
        if not offer.title_ar and offer.title:
            print(f"Translating Title for Offer ID {offer.id}: '{offer.title}'...")
            translated = translate_text(offer.title)
            if translated:
                offer.title_ar = translated
                modified = True
                print(f"  └─ Success: '{offer.title}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Subtitle
        if not offer.subtitle_ar and offer.subtitle:
            print(f"Translating Subtitle for Offer ID {offer.id}: '{offer.subtitle}'...")
            translated = translate_text(offer.subtitle)
            if translated:
                offer.subtitle_ar = translated
                modified = True
                print(f"  └─ Success: '{offer.subtitle}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Button Text
        if not offer.button_text_ar and offer.button_text:
            print(f"Translating Button Text for Offer ID {offer.id}: '{offer.button_text}'...")
            translated = translate_text(offer.button_text)
            if translated:
                offer.button_text_ar = translated
                modified = True
                print(f"  └─ Success: '{offer.button_text}' -> '{translated}'")
                time.sleep(0.5)

        # Generate Arabic Link (Localize link by prefixing /ar)
        if not offer.button_link_ar and offer.button_link:
            link = offer.button_link.strip()
            if link.startswith('/') and not link.startswith('/ar/'):
                offer.button_link_ar = f"/ar{link}"
            else:
                offer.button_link_ar = link
            modified = True
            print(f"Set button_link_ar: '{offer.button_link_ar}'")

        if modified:
            offer.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} offers.")

if __name__ == "__main__":
    run()

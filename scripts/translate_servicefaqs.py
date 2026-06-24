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

from catalog.models import ServiceFAQ

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
    faqs = ServiceFAQ.objects.all()
    print(f"Found {faqs.count()} FAQs to process.")
    
    updated_count = 0
    for faq in faqs:
        modified = False
        
        # Translate Question
        if not faq.question_ar and faq.question:
            print(f"Translating Question for FAQ ID {faq.id}: '{faq.question}'...")
            translated = translate_text(faq.question)
            if translated:
                faq.question_ar = translated
                modified = True
                print(f"  └─ Success: '{faq.question}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Answer
        if not faq.answer_ar and faq.answer:
            print(f"Translating Answer for FAQ ID {faq.id}: '{faq.answer[:40]}...'...")
            translated = translate_text(faq.answer)
            if translated:
                faq.answer_ar = translated
                modified = True
                print(f"  └─ Success: '{faq.answer[:40]}...' -> '{translated[:40]}...'")
                time.sleep(0.5)

        if modified:
            faq.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} FAQs.")

if __name__ == "__main__":
    run()

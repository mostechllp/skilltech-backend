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

from catalog.models import Service, InstallationType, TVSize, AvailableTime

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
    print("--- Translating Services ---")
    services = Service.objects.all()
    for s in services:
        modified = False
        if not s.name_ar and s.name:
            print(f"Translating Service Name '{s.name}'...")
            trans = translate_text(s.name)
            if trans:
                s.name_ar = trans
                modified = True
                print(f"  └─ Success: '{trans}'")
                time.sleep(0.5)
        if not s.description_ar and s.description:
            print(f"Translating Service Description...")
            trans = translate_text(s.description)
            if trans:
                s.description_ar = trans
                modified = True
                print(f"  └─ Success: '{trans}'")
                time.sleep(0.5)
        if modified:
            s.save()

    print("--- Translating Installation Types ---")
    installs = InstallationType.objects.all()
    for i in installs:
        if not i.name_ar and i.name:
            print(f"Translating Installation Type Name '{i.name}'...")
            trans = translate_text(i.name)
            if trans:
                i.name_ar = trans
                i.save()
                print(f"  └─ Success: '{trans}'")
                time.sleep(0.5)

    print("--- Translating TV Sizes ---")
    sizes = TVSize.objects.all()
    for t in sizes:
        if not t.size_ar and t.size:
            print(f"Translating TV Size '{t.size}'...")
            trans = translate_text(t.size)
            if trans:
                t.size_ar = trans
                t.save()
                print(f"  └─ Success: '{trans}'")
                time.sleep(0.5)

    print("--- Translating Available Times ---")
    times = AvailableTime.objects.all()
    for a in times:
        if not a.time_slot_ar and a.time_slot:
            print(f"Translating Time Slot '{a.time_slot}'...")
            trans = translate_text(a.time_slot)
            if trans:
                a.time_slot_ar = trans
                a.save()
                print(f"  └─ Success: '{trans}'")
                time.sleep(0.5)

    print("\n✅ Translation run complete.")

if __name__ == "__main__":
    run()

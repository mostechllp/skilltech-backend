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

from catalog.models import Project

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
    projects = Project.objects.all()
    print(f"Found {projects.count()} projects to process.")
    
    updated_count = 0
    for project in projects:
        modified = False
        
        # Translate Title
        if not project.title_ar and project.title:
            print(f"Translating Title for Project ID {project.id}: '{project.title}'...")
            translated = translate_text(project.title)
            if translated:
                project.title_ar = translated
                modified = True
                print(f"  └─ Success: '{project.title}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Subtitle
        if not project.subtitle_ar and project.subtitle:
            print(f"Translating Subtitle for Project ID {project.id}: '{project.subtitle}'...")
            translated = translate_text(project.subtitle)
            if translated:
                project.subtitle_ar = translated
                modified = True
                print(f"  └─ Success: '{project.subtitle}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Location
        if not project.location_ar and project.location:
            print(f"Translating Location for Project ID {project.id}: '{project.location}'...")
            translated = translate_text(project.location)
            if translated:
                project.location_ar = translated
                modified = True
                print(f"  └─ Success: '{project.location}' -> '{translated}'")
                time.sleep(0.5)

        if modified:
            project.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} projects.")

if __name__ == "__main__":
    run()

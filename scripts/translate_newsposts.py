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

from catalog.models import NewsPost

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
    posts = NewsPost.objects.all()
    print(f"Found {posts.count()} news posts to process.")
    
    updated_count = 0
    for post in posts:
        modified = False
        
        # Translate Title
        if not post.title_ar and post.title:
            print(f"Translating Title for NewsPost ID {post.id}: '{post.title}'...")
            translated = translate_text(post.title)
            if translated:
                post.title_ar = translated
                modified = True
                print(f"  └─ Success: '{post.title}' -> '{translated}'")
                time.sleep(0.5)

        # Translate Content
        if not post.content_ar and post.content:
            print(f"Translating Content for NewsPost ID {post.id}: '{post.content[:40]}...'...")
            translated = translate_text(post.content)
            if translated:
                post.content_ar = translated
                modified = True
                print(f"  └─ Success: '{post.content[:40]}...' -> '{translated[:40]}...'")
                time.sleep(0.5)

        if modified:
            post.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} news posts.")

if __name__ == "__main__":
    run()

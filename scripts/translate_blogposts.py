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

from catalog.models import BlogPost

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
    posts = BlogPost.objects.all()
    print(f"Found {posts.count()} blog posts to process.")
    
    updated_count = 0
    for post in posts:
        modified = False
        
        # Translate Title
        print(f"Translating Title for BlogPost ID {post.id}: '{post.title}'...")
        translated = translate_text(post.title)
        if translated:
            post.title_ar = translated
            modified = True
            print(f"  └─ Success: '{post.title}' -> '{translated}'")
            time.sleep(0.5)

        # Translate Content
        print(f"Translating Content for BlogPost ID {post.id} (length: {len(post.content)})...")
        translated = translate_text(post.content)
        if translated:
            post.content_ar = translated
            modified = True
            print(f"  └─ Success Content (length: {len(translated)})")
            time.sleep(0.5)

        # Translate Short Description
        if post.short_description:
            print(f"Translating Short Description for BlogPost ID {post.id}...")
            translated = translate_text(post.short_description)
            if translated:
                post.short_description_ar = translated
                modified = True
                print(f"  └─ Success Short Description")
                time.sleep(0.5)

        # Translate Author
        if post.author:
            print(f"Translating Author for BlogPost ID {post.id}: '{post.author}'...")
            translated = translate_text(post.author)
            if translated:
                post.author_ar = translated
                modified = True
                print(f"  └─ Success: '{post.author}' -> '{translated}'")
                time.sleep(0.5)

        if modified:
            post.save()
            updated_count += 1

    print(f"\n✅ Translation run complete. Updated {updated_count} blog posts with FULL translations.")

if __name__ == "__main__":
    run()

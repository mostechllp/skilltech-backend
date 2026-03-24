import os
import django
import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote, urlparse
import time
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import (
    MainCategory, Category, SubCategory, Product, 
    ProductSpecification, ProductBulletFeature, 
    ProductImage, ProductSeo
)
from django.utils.text import slugify

def download_image(url, model_instance, field_name, filename_prefix="product"):
    if not url:
        return
    if not url.startswith('http'):
        url = 'https://skilltechonline.com/' + url.lstrip('/')
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            ext = os.path.splitext(urlparse(url).path)[1]
            if not ext:
                ext = '.jpg'
            
            filename = f"{filename_prefix}_{model_instance.pk}{ext}"
            getattr(model_instance, field_name).save(filename, ContentFile(response.content), save=True)
            return True
    except Exception as e:
        print(f"  Error downloading image {url}: {e}")
    return False

def scrape_product(url, target_main_cat=None, target_cat=None, target_subcat=None):
    print(f"\nScraping: {url}")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"  Error fetching URL: {e}")
        return False

    soup = BeautifulSoup(response.content, 'html.parser')

    # 1. Model and Title
    h2 = soup.find('h2')
    if h2:
        model_span = h2.find('span')
        if model_span:
            model_name = model_span.get_text(strip=True)
            model_span.extract()
            title = h2.get_text(strip=True)
        else:
            txt = h2.get_text(strip=True)
            parts = txt.split(' ', 1)
            model_name = parts[0]
            title = parts[1] if len(parts) > 1 else txt
    else:
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else "Unknown"
        model_name = title.split(' ')[0]

    # Clean model name (remove prefix 'SH-' if redundant or just keep as is)
    model_name = model_name.strip()
    print(f"  Model: {model_name} | Title: {title}")

    # 2. Categories
    main_cat, _ = MainCategory.objects.get_or_create(name=target_main_cat)
    category, _ = Category.objects.get_or_create(
        name=target_cat, 
        defaults={'main_category': main_cat, 'slug': slugify(target_cat)}
    )
    subcategory, _ = SubCategory.objects.get_or_create(
        name=target_subcat, 
        defaults={'category': category, 'slug': slugify(target_subcat)}
    )

    # 3. Create Product
    p_slug = slugify(model_name)
    product, created = Product.objects.update_or_create(
        slug=p_slug,
        defaults={
            'name': model_name,
            'title': title,
            'subcategory': subcategory,
            'active': True,
            'show_in_home': True,
        }
    )
    
    # Update slug_path
    product.slug_path = f"{subcategory.category.slug}/{subcategory.slug}/{product.slug}"
    product.save()

    # 4. Tabs Mapping
    tab_map = {}
    for link in soup.find_all('a', class_='nav-link'):
        label = link.get_text(strip=True).upper()
        target_id = link.get('href', '').replace('#', '')
        if target_id: tab_map[label] = target_id

    # 5. Description
    d_id = tab_map.get('DESCRIPTION') or tab_map.get('DETAILS')
    if d_id:
        desc_div = soup.find('div', id=d_id)
        if desc_div: product.description = str(desc_div)

    # 6. Specifications
    s_id = tab_map.get('SPECIFICATION')
    spec_p = soup.find('div', id=s_id) if s_id else soup.find('div', class_='pdesc')
    ProductSpecification.objects.filter(product=product).delete()
    if spec_p:
        table = spec_p.find('table')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    k = cols[0].get_text(strip=True).replace(':', '')
                    v = cols[1].get_text(strip=True)
                    if k and v: ProductSpecification.objects.create(product=product, key=k, value=v)

    # 7. Bullet Features
    f_id = tab_map.get('FEATURES')
    ProductBulletFeature.objects.filter(product=product).delete()
    if f_id:
        feat_div = soup.find('div', id=f_id)
        if feat_div:
            for i, li in enumerate(feat_div.find_all('li')):
                txt = li.get_text(strip=True)
                if not txt: continue
                strong = li.find('strong')
                if strong:
                    k = strong.get_text(strip=True).rstrip(':').rstrip('–').strip()
                    v = txt.replace(strong.get_text(), '').strip().lstrip('–').lstrip(':').lstrip('-').strip()
                else:
                    k, v = "", txt
                ProductBulletFeature.objects.create(product=product, title=k, text=v, order=i)

    # 8. Images
    # Main Image
    ez = soup.find('div', class_='easyzoom')
    if ez and ez.find('a'):
        img_url = ez.find('a').get('href')
        download_image(img_url, product, 'main_image', f"main_{product.slug}")

    # Gallery
    ProductImage.objects.filter(product=product).delete()
    thumbnails = soup.select('ul.thumbnails a')
    for i, t in enumerate(thumbnails):
        gal_url = t.get('href')
        if gal_url:
            pi = ProductImage(product=product, order=i)
            pi.save()
            download_image(gal_url, pi, 'image', f"gallery_{product.slug}_{i}")

    # Drawing Image
    dr_id = tab_map.get('DRAWING')
    if dr_id:
        dr_div = soup.find('div', id=dr_id)
        dr_img = dr_div.find('img') if dr_div else None
        if dr_img:
            download_image(dr_img.get('src'), product, 'drawing_image', f"drawing_{product.slug}")

    # 9. Datasheet
    ds = soup.find('a', href=re.compile(r'Datasheet\.pdf$', re.I))
    if ds:
        ds_url = ds.get('href')
        if not ds_url.startswith('http'): ds_url = 'https://skilltechonline.com/' + ds_url.lstrip('/')
        try:
            ds_resp = requests.get(ds_url, timeout=15)
            if ds_resp.status_code == 200:
                product.datasheet.save(f"datasheet_{product.slug}.pdf", ContentFile(ds_resp.content), save=True)
        except: pass

    # 10. SEO
    ProductSeo.objects.update_or_create(
        product=product,
        defaults={
            'meta_title': soup.find('title').text.strip() if soup.find('title') else "",
            'meta_description': (soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})).get('content', '') if soup.find('meta') else "",
        }
    )

    product.save()
    print(f"  SUCCESS: {model_name} added/updated.")
    return True

def run():
    tasks = [
        {
            'url': 'https://skilltechonline.com/ergonomic-mounts/gas-spring-monitor-arm/sh35-t01/',
            'main': 'Mounting Solutions', 'cat': 'Ergonomic Mounts', 'subcat': 'Gas Spring Monitor Arm'
        },
        {
            'url': 'https://skilltechonline.com/kiosk-stand/kiosk-stands/sh-k55004k/',
            'main': 'Displays', 'cat': 'Kiosk Stands', 'subcat': 'Kiosk Stands'
        },
        {
            'url': 'https://skilltechonline.com/kiosk-stand/kiosk-stands/sh-k50504k/',
            'main': 'Displays', 'cat': 'Kiosk Stands', 'subcat': 'Kiosk Stands'
        },
        {
            'url': 'https://skilltechonline.com/kiosk-stand/kiosk-stands/sh-k43004k/',
            'main': 'Displays', 'cat': 'Kiosk Stands', 'subcat': 'Kiosk Stands'
        },
        {
            'url': 'https://skilltechonline.com/hdmi-cables/hdmi-cables/sh-hde015m/',
            'main': 'Cables & Wires', 'cat': 'HDMI Cables', 'subcat': 'HDMI Cables'
        },
        {
            'url': 'https://skilltechonline.com/hdmi-cables/hdmi-cables/sh-hds15m/',
            'main': 'Cables & Wires', 'cat': 'HDMI Cables', 'subcat': 'HDMI Cables'
        },
    ]

    for task in tasks:
        scrape_product(task['url'], task['main'], task['cat'], task['subcat'])
        time.sleep(1)

if __name__ == "__main__":
    run()

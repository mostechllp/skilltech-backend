import os
import django
import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote, urlparse
import time
import xml.etree.ElementTree as ET

# Setup Django environment
sys.path.append('D:\\Projects\\Skilltech\\skilltech-website-2026-be-py')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import (
    MainCategory, Category, SubCategory, Product, 
    ProductSpecification, ProductBulletFeature, 
    ProductImage, ProductSeo
)
from django.utils.text import slugify

def scrape_any_product(url):
    print(f"Fetching data from: {url}...")
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return False

    soup = BeautifulSoup(response.content, 'html.parser')

    # 1. Basic Info
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

    if not model_name or model_name == "Unknown":
         print(f"Could not find model name for {url}. Skipping.")
         return False

    print(f"Found Product: {model_name} | Title: {title}")

    # 2. DYNAMIC Category & SubCategory
    cat_name = "General"
    subcat_name = "General"
    
    breadcrumb_div = soup.find(lambda tag: tag.name == "div" and "Home" in tag.text and "»" in tag.text)
    
    if breadcrumb_div:
        links = breadcrumb_div.find_all('a')
        if len(links) >= 2:
            cat_name = links[1].get_text(strip=True)
        if len(links) >= 3:
            subcat_name = links[2].get_text(strip=True)
        elif len(links) == 2:
            subcat_name = cat_name

    # Database logic
    main_cat_name = "Mounting Solutions"
    if "CABLE" in cat_name.upper(): main_cat_name = "Cables & Wires"
    elif "GAMING" in cat_name.upper(): main_cat_name = "Gaming"
    elif "LED" in cat_name.upper(): main_cat_name = "Displays"
    elif "PROJECTOR" in cat_name.upper(): main_cat_name = "Mounting Solutions"
    elif "TV" in cat_name.upper() and ("SMART" in cat_name.upper() or "NORMAL" in cat_name.upper()): main_cat_name = "Mounting Solutions"
    elif "DESKTOP" in cat_name.upper(): main_cat_name = "Mounting Solutions"
    elif "STAND" in cat_name.upper() or "FLOOR" in cat_name.upper(): main_cat_name = "Mounting Solutions"

    main_cat, _ = MainCategory.objects.get_or_create(name=main_cat_name)
    category, _ = Category.objects.get_or_create(
        slug=slugify(cat_name), 
        defaults={'name': cat_name, 'main_category': main_cat, 'show_in_home': True}
    )
    subcategory, _ = SubCategory.objects.get_or_create(
        slug=slugify(subcat_name), 
        defaults={'name': subcat_name, 'category': category}
    )

    # 3. Product Object
    p_slug = slugify(model_name)
    p_slug_path = f"{category.slug}/{subcategory.slug}/{p_slug}"
    # ✅ Skip if already exists
    if Product.objects.filter(slug=p_slug).exists():
        print(f"SKIPPED: {model_name} already exists.")
        return False
    
    product, created = Product.objects.update_or_create(
        slug=p_slug,
        defaults={
            'name': model_name,
            'title': title,
            'subcategory': subcategory,
            'slug_path': p_slug_path,
            'active': True,
            'show_in_home': True,
        }
    )

    # 4. Map Tabs Dynamically
    tab_map = {}
    for link in soup.find_all('a', class_='nav-link'):
        label = link.get_text(strip=True).upper()
        target_id = link.get('href', '').replace('#', '')
        if target_id: tab_map[label] = target_id
    
    # 5. Description
    d_id = tab_map.get('DESCRIPTION') or tab_map.get('DETAILS')
    if d_id:
        p = soup.find('div', id=d_id)
        if p: product.description = p.get_text(strip=True)

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
                    k, v = cols[0].get_text(strip=True).replace(':', ''), cols[1].get_text(strip=True)
                    if k and v: ProductSpecification.objects.create(product=product, key=k, value=v)

    # 7. CBM from calculatebx
    cbx = soup.find('div', class_='calculatebx')
    if cbx:
        tbl = cbx.find('table')
        if tbl:
            for row in tbl.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    k, v = cols[0].get_text(strip=True), cols[1].get_text(strip=True)
                    if "Quantity per Carton" in k:
                        nums = re.findall(r'\d+', v)
                        if nums: product.units_per_carton = int(nums[0])
                    elif "Gross Weight" in k:
                        w = re.search(r'\d+\.?\d*', v)
                        if w: product.gross_weight_per_carton_kg = float(w.group())
                    elif "Net Weight" in k:
                        w = re.search(r'\d+\.?\d*', v)
                        if w: product.net_weight_per_carton_kg = float(w.group())
                    elif "Carton Dimension" in k:
                        dims = re.findall(r'\d+\.?\d*', v)
                        if len(dims) >= 3:
                            product.carton_length_cm, product.carton_width_cm, product.carton_height_cm = map(float, dims[:3])
        product.show_cbm_calculator = True

    # 8. Features (Bullet Features)
    f_id = tab_map.get('FEATURES')
    ProductBulletFeature.objects.filter(product=product).delete()
    if f_id:
        p = soup.find('div', id=f_id)
        if p:
            for i, li in enumerate(p.find_all('li')):
                txt = li.get_text(strip=True)
                if not txt: continue
                strong = li.find('strong')
                if strong:
                    k = strong.get_text(strip=True).rstrip(':').rstrip('–').strip()
                    v = txt.replace(strong.get_text(), '').strip().lstrip('–').lstrip(':').lstrip('-').strip()
                elif ' – ' in txt:
                    parts = txt.split(' – ', 1)
                    k = parts[0].strip()
                    v = parts[1].strip()
                else:
                    k = ""
                    v = txt
                ProductBulletFeature.objects.create(product=product, title=k, text=v, order=i)

    # 9. DYNAMIC Tags
    t_id = tab_map.get('TAGS')
    if t_id:
        p = soup.find('div', id=t_id)
        if p: product.tags = p.get_text(strip=True)

    # 10. DYNAMIC Video
    v_id = tab_map.get('VIDEO')
    v_url = None
    if v_id:
        p = soup.find('div', id=v_id)
        if p and p.find('iframe'): v_url = p.find('iframe').get('src')
    if not v_url:
        for f in soup.find_all('iframe'):
            if 'youtube' in f.get('src', '') or 'vimeo' in f.get('src', ''):
                v_url = f.get('src'); break
    product.video_url = v_url

    # 11. Media
    def get_rel(u): return unquote(u.split('assets/')[-1]) if 'assets/' in u else unquote(os.path.basename(u))
    
    ez = soup.find('div', class_='easyzoom')
    if ez and ez.find('a'): product.main_image = f"assets/{get_rel(ez.find('a').get('href'))}"
    
    ProductImage.objects.filter(product=product).delete()
    for i, t in enumerate(soup.select('ul.thumbnails a')[1:]):
        if t.get('href'):
            ProductImage.objects.create(
                product=product,
                image=f"assets/{get_rel(t.get('href'))}",
                order=i
            )

    # DYNAMIC Drawing Image
    dr_id = tab_map.get('DRAWING')
    if dr_id:
        p = soup.find('div', id=dr_id)
        img = p.find('img') if p else None
        if img: product.drawing_image = f"assets/{get_rel(img.get('src'))}"
    
    if not product.drawing_image:
        for img in soup.find_all('img'):
            if 'Drawing' in img.get('src', ''):
                product.drawing_image = f"assets/{get_rel(img.get('src'))}"; break

    # Datasheet
    ds = soup.find('a', href=re.compile(r'Datasheet\.pdf$', re.I))
    if ds: product.datasheet = f"assets/{get_rel(ds.get('href'))}"

    # 12. SEO
    product.save()
    ProductSeo.objects.update_or_create(
        product=product,
        defaults={
            'meta_title': soup.find('title').text.strip() if soup.find('title') else "",
            'meta_description': (soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})).get('content', '') if soup.find('meta') else "",
            'canonical_url': soup.find('link', rel='canonical').get('href') if soup.find('link', rel='canonical') else None
        }
    )
    product.save()
    print(f"SUCCESS: Imported {model_name}.")
    return True

def main():
    sitemap_path = 'D:\\Projects\\Skilltech\\sitemap (1).xml'
    
    if not os.path.exists(sitemap_path):
        print(f"Sitemap not found at {sitemap_path}")
        return

    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # Standard sitemap namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for url_tag in root.findall('ns:url', namespace):
        loc = url_tag.find('ns:loc', namespace).text
        if loc:
            parsed = urlparse(loc)
            path_parts = [p for p in parsed.path.split('/') if p]
            
            # Heuristic for product URL: 
            # 1. More than 2 segments (e.g. /cat/subcat/prod/)
            # 2. Doesn't contain 'cat/' or 'about/' or 'contact/' etc.
            if len(path_parts) >= 3:
                # Basic exclusions
                if path_parts[0] in ['cat', 'about', 'contact', 'support', 'gallery', 'tv-installation']:
                    continue
                urls.append(loc)
            # Special case for some categories that might be deep but not products? 
            # Actually most 3+ segment URLs in this sitemap ARE products.
    
    print(f"Found {len(urls)} potential product URLs.")
    
    count = 0
    total = len(urls)
    for i, url in enumerate(urls):
        print(f"[{i+1}/{total}] ", end="")
        success = scrape_any_product(url)
        if success:
            count += 1
        
        # Polite delay
        time.sleep(0.5)
        
    print(f"Finished. Successfully processed {count} products.")

if __name__ == "__main__":
    main()

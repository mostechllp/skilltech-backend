import os
import sys
import csv
from urllib.parse import urlparse

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'skilltech-website-2026-be-py'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from catalog.models import Product

def main():
    csv_file = 'p.csv'
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return

    updated_count = 0
    not_found_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row['model_number_slug'].strip()
            full_url = row['description'].strip()
            
            if not slug or not full_url:
                continue
                
            # Parse URL and get path
            # https://skilltechonline.com/assets/images/uploads/product_tabs/image_name.jpeg
            parsed_url = urlparse(full_url)
            # Remove leading slash to get: assets/images/uploads/product_tabs/image_name.jpeg
            image_path = parsed_url.path.lstrip('/')
            
            # Find product by slug (exact) or case-insensitive
            try:
                product = Product.objects.get(slug__iexact=slug)
                product.box_3d_image = image_path
                product.box_3d_image_alt = f"{product.name} 3D Box"
                product.save()
                updated_count += 1
                print(f"Updated: {slug} -> {image_path}")
            except Product.DoesNotExist:
                # Try by name if slug fails
                try:
                    product = Product.objects.get(name__iexact=slug)
                    product.box_3d_image = image_path
                    product.box_3d_image_alt = f"{product.name} 3D Box"
                    product.save()
                    updated_count += 1
                    print(f"Updated (by name): {slug} -> {image_path}")
                except Product.DoesNotExist:
                    print(f"Product not found: {slug}")
                    not_found_count += 1
                except Product.MultipleObjectsReturned:
                    print(f"Multiple products found for name: {slug}")
                    not_found_count += 1
            except Product.MultipleObjectsReturned:
                print(f"Multiple products found for slug: {slug}")
                not_found_count += 1

    print("\nSummary:")
    print(f"Total Updated: {updated_count}")
    print(f"Total Not Found: {not_found_count}")

if __name__ == "__main__":
    main()

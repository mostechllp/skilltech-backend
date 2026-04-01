import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Product, Arm


ARM_MAP = {
    'single': 'Single Arm',
    'double': 'Double Arm',
    'triple': 'Triple Arm',
    'four': 'Quad Arm',
    'five': 'Five Arm',
    'six': 'Six Arm',
}


def run():
    # Step 1: Create Arm objects
    arm_objects = {}
    for key, value in ARM_MAP.items():
        arm_obj, _ = Arm.objects.get_or_create(name=value,slug=key)
        arm_objects[key] = arm_obj

    print("✅ Arm records created")

    # Step 2: Map products
    updated_count = 0

    for product in Product.objects.filter(subcategory__category__slug='desktop-mounts'):
        if product.arm:
            key = product.arm.strip().lower()

            if key in ARM_MAP:
                product.arm_fk = arm_objects[key]
                product.save()
                updated_count += 1
            else:
                print(f"⚠️ Unknown arm value: {product.arm}")

    print(f"✅ Updated {updated_count} products")


if __name__ == "__main__":
    run()
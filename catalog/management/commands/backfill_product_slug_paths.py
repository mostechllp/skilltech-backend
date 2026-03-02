from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from catalog.models import Product  # change "catalog" if your app name differs


class Command(BaseCommand):
    help = "Backfill Product.slug_path as category/subcategory/product for all products."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print changes but do not write to DB.",
        )
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Update only products where slug_path is empty.",
        )
        parser.add_argument(
            "--fill-missing-slugs",
            action="store_true",
            help="If category/subcategory/product slug is empty, generate it using slugify and save.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        only_missing = options["only_missing"]
        fill_missing_slugs = options["fill_missing_slugs"]

        qs = Product.objects.select_related("subcategory", "subcategory__category")

        if only_missing:
            qs = qs.filter(slug_path__isnull=True) | qs.filter(slug_path="")

        updated = 0
        skipped = 0

        for p in qs.iterator(chunk_size=500):
            sub = p.subcategory
            cat = getattr(sub, "category", None)

            if cat is None:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"Skipping Product {p.id}: subcategory has no category relation"))
                continue

            # Ensure slugs exist if requested
            if fill_missing_slugs:
                changed = False

                if not getattr(cat, "slug", None):
                    cat.slug = slugify(getattr(cat, "name", "") or str(cat.id))
                    changed = True

                if not getattr(sub, "slug", None):
                    sub.slug = slugify(getattr(sub, "name", "") or str(sub.id))
                    changed = True

                if not p.slug:
                    p.slug = slugify(p.name or str(p.id))
                    # NOTE: if Product.slug is unique and slugify(name) clashes, this may fail.
                    # If you expect duplicates, you should implement a unique-slug generator.
                    # For now, we assume names are unique enough.
                    changed = True

                if changed and not dry_run:
                    cat.save(update_fields=["slug"])
                    sub.save(update_fields=["slug"])
                    p.save(update_fields=["slug"])

            # Build slug_path
            new_path = f"{cat.slug}/{sub.slug}/{p.slug}"

            # Skip if no change
            if (p.slug_path or "") == new_path:
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(f"[DRY RUN] Product {p.id}: '{p.slug_path}' -> '{new_path}'")
            else:
                p.slug_path = new_path
                p.save(update_fields=["slug_path"])

            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Updated: {updated}, Skipped: {skipped}"))
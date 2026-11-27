import json
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.db import transaction
from catalog.models import (
    MainCategory,
    Category,
    SubCategory,
    Product,
    Arm,
    Feature,
    ProductBulletFeature,
    ProductSpecification,
    Offer,
    Catalogue,
    Certificate,
    BlogPost,
    Project,
    Service,
    InstallationType,
    TVSize,
    AvailableTime,
    ServiceFAQ,
    HomeStatistic,
    ServiceStatistic,
    NewsPost,
    BranchLocation,
    CountrySetting,
)

LANG_SUFFIXES = ("_ar", "_hi", "_es", "_pt", "_fr", "_ru")

# (ModelClass, lookup_fields)
MODEL_SPECS = [
    (MainCategory, ["slug"]),
    (Category, ["slug"]),
    (SubCategory, ["slug"]),
    (Product, ["slug"]),
    (Arm, ["slug"]),
    (Feature, ["title"]),
    (Offer, ["title"]),
    (Catalogue, ["title"]),
    (Certificate, ["title"]),
    (BlogPost, ["slug"]),
    (Project, ["title"]),
    (Service, ["name"]),
    (InstallationType, ["name"]),
    (TVSize, ["size"]),
    (AvailableTime, ["time_slot"]),
    (ServiceFAQ, ["question"]),
    (HomeStatistic, ["label"]),
    (ServiceStatistic, ["label"]),
    (NewsPost, ["slug"]),
    (BranchLocation, ["title"]),
    (CountrySetting, ["country_code"]),
    (ProductBulletFeature, ["product__slug", "title"]),
    (ProductSpecification, ["product__slug", "key"]),
]


def get_trans_fields(model):
    """Return all text/char translation field names (excludes image/file fields)."""
    fields = []
    for f in model._meta.fields:
        if f.name.endswith(LANG_SUFFIXES) and f.get_internal_type() in ("CharField", "TextField"):
            fields.append(f.name)
    return fields


def get_lookup_dict(obj, lookup_fields):
    lookup = {}
    for field in lookup_fields:
        val = obj
        for part in field.split("__"):
            val = getattr(val, part, None) if val is not None else None
        if val is None or val == "":
            return None
        lookup[field] = val
    return lookup


class Command(BaseCommand):
    help = "Export local translations to JSON and import them into live DB with zero external API calls."

    def add_arguments(self, parser):
        parser.add_argument("--export", type=str, help="Path to export translations JSON bundle.")
        parser.add_argument("--import-file", dest="import_file", type=str, help="Path to import translations JSON bundle.")
        parser.add_argument("--dry-run", action="store_true", help="Preview import counts without modifying the database.")
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing non-empty translations on target DB (default: only fill NULL/empty fields).",
        )

    def handle(self, *args, **options):
        export_path = options.get("export")
        import_path = options.get("import_file")
        dry_run = options.get("dry_run", False)
        overwrite = options.get("overwrite", False)

        if not export_path and not import_path:
            raise CommandError("Provide either --export <file.json> or --import-file <file.json>.")

        if export_path:
            self.export_bundle(export_path)
        if import_path:
            self.import_bundle(import_path, dry_run=dry_run, overwrite=overwrite)

    def export_bundle(self, export_path):
        bundle = {}
        total_records = 0

        for model, lookup_fields in MODEL_SPECS:
            model_name = model.__name__
            trans_fields = get_trans_fields(model)
            if not trans_fields:
                continue

            qs = model.objects.all()
            if any("__" in f for f in lookup_fields):
                qs = qs.select_related(*{f.split("__")[0] for f in lookup_fields if "__" in f})

            records = []
            for obj in qs:
                lookup = get_lookup_dict(obj, lookup_fields)
                if not lookup:
                    continue
                translations = {}
                for tf in trans_fields:
                    val = getattr(obj, tf, None)
                    if val is not None and str(val).strip() != "":
                        translations[tf] = val
                if translations:
                    records.append({"lookup": lookup, "translations": translations})

            bundle[model_name] = records
            total_records += len(records)
            self.stdout.write(f"Exported {len(records)} {model_name} records")

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"\nDone! Exported {total_records} total records to {export_path}"))

    def import_bundle(self, import_path, dry_run=False, overwrite=False):
        with open(import_path, "r", encoding="utf-8") as f:
            bundle = json.load(f)

        model_map = {m.__name__: (m, get_trans_fields(m)) for m, _ in MODEL_SPECS}
        total_updated = 0
        total_skipped = 0

        with transaction.atomic():
            for model_name, records in bundle.items():
                if model_name not in model_map:
                    continue
                model, valid_fields = model_map[model_name]
                valid_set = set(valid_fields)
                model_updated = 0

                for rec in records:
                    lookup = rec.get("lookup") or {}
                    raw_trans = rec.get("translations") or {}
                    updates = {k: v for k, v in raw_trans.items() if k in valid_set}
                    if not lookup or not updates:
                        continue

                    matches = list(model.objects.filter(**lookup))
                    if not matches:
                        total_skipped += 1
                        continue

                    for obj in matches:
                        if overwrite:
                            fields_to_apply = updates
                        else:
                            # Only fill NULL / empty fields so existing live translations (e.g. Arabic) are never overwritten
                            fields_to_apply = {
                                k: v
                                for k, v in updates.items()
                                if getattr(obj, k, None) is None or str(getattr(obj, k, "")).strip() == ""
                            }

                        if not fields_to_apply:
                            continue

                        if not dry_run:
                            model.objects.filter(pk=obj.pk).update(**fields_to_apply)
                        model_updated += 1

                total_updated += model_updated
                self.stdout.write(
                    f"{'[DRY-RUN] ' if dry_run else ''}Updated {model_updated} {model_name} row(s)"
                )

            if dry_run:
                transaction.set_rollback(True)

        if not dry_run:
            cache.clear()
            self.stdout.write(self.style.SUCCESS(f"\nImport complete! Updated {total_updated} row(s) with 0 API calls. Cache cleared."))
        else:
            self.stdout.write(self.style.WARNING(f"\nDry-run complete. Would update {total_updated} row(s) ({total_skipped} unmatched)."))

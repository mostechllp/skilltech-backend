import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


def ensure_all_database_columns():
    """
    Safely inspects and adds all necessary Hindi & Arabic columns
    to MySQL/SQLite tables if they do not exist.
    Prevents OperationalError 1054 (Unknown column).
    """
    from django.db import connection

    cols_to_check = [
        ('catalog_product', 'title_hi', 'VARCHAR(255) NULL'),
        ('catalog_product', 'short_description_hi', 'VARCHAR(255) NULL'),
        ('catalog_product', 'description_hi', 'LONGTEXT NULL'),
        ('catalog_product', 'tags_hi', 'LONGTEXT NULL'),
        ('catalog_productbulletfeature', 'title_hi', 'VARCHAR(255) NULL'),
        ('catalog_productbulletfeature', 'text_hi', 'LONGTEXT NULL'),
        ('catalog_productbulletfeature', 'title_ar', 'VARCHAR(255) NULL'),
        ('catalog_productbulletfeature', 'text_ar', 'LONGTEXT NULL'),
        ('catalog_productspecification', 'key_hi', 'VARCHAR(200) NULL'),
        ('catalog_productspecification', 'value_hi', 'VARCHAR(500) NULL'),
        ('catalog_blogpost', 'title_hi', 'VARCHAR(255) NULL'),
        ('catalog_blogpost', 'short_description_hi', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'content_hi', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'author_hi', 'VARCHAR(100) NULL'),
        ('catalog_service', 'name_hi', 'VARCHAR(100) NULL'),
        ('catalog_service', 'description_hi', 'LONGTEXT NULL'),
        ('catalog_servicefaq', 'question_hi', 'VARCHAR(255) NULL'),
        ('catalog_servicefaq', 'answer_hi', 'LONGTEXT NULL'),
        ('catalog_tvsize', 'size_hi', 'VARCHAR(50) NULL'),
        ('catalog_availabletime', 'time_slot_hi', 'VARCHAR(100) NULL'),
        ('catalog_newspost', 'title_hi', 'VARCHAR(255) NULL'),
        ('catalog_newspost', 'content_hi', 'LONGTEXT NULL'),
        ('catalog_category', 'name_hi', 'VARCHAR(100) NULL'),
        ('catalog_subcategory', 'name_hi', 'VARCHAR(100) NULL'),
        ('catalog_maincategory', 'name_hi', 'VARCHAR(100) NULL'),
        ('catalog_feature', 'title_hi', 'VARCHAR(255) NULL'),
        ('catalog_installationtype', 'name_hi', 'VARCHAR(100) NULL'),
        ('catalog_project', 'title_hi', 'VARCHAR(100) NULL'),
        ('catalog_project', 'subtitle_hi', 'VARCHAR(100) NULL'),
        ('catalog_project', 'location_hi', 'VARCHAR(100) NULL'),
        ('catalog_catalogue', 'title_hi', 'VARCHAR(100) NULL'),
        ('catalog_certificate', 'title_hi', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'title_hi', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'subtitle_hi', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'button_text_hi', 'VARCHAR(50) NULL'),

        # Spanish (_es) columns
        ('catalog_product', 'title_es', 'VARCHAR(255) NULL'),
        ('catalog_product', 'short_description_es', 'VARCHAR(255) NULL'),
        ('catalog_product', 'description_es', 'LONGTEXT NULL'),
        ('catalog_product', 'tags_es', 'LONGTEXT NULL'),
        ('catalog_productbulletfeature', 'title_es', 'VARCHAR(255) NULL'),
        ('catalog_productbulletfeature', 'text_es', 'LONGTEXT NULL'),
        ('catalog_productspecification', 'key_es', 'VARCHAR(200) NULL'),
        ('catalog_productspecification', 'value_es', 'VARCHAR(500) NULL'),
        ('catalog_blogpost', 'title_es', 'VARCHAR(255) NULL'),
        ('catalog_blogpost', 'short_description_es', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'content_es', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'author_es', 'VARCHAR(100) NULL'),
        ('catalog_service', 'name_es', 'VARCHAR(100) NULL'),
        ('catalog_service', 'description_es', 'LONGTEXT NULL'),
        ('catalog_servicefaq', 'question_es', 'VARCHAR(255) NULL'),
        ('catalog_servicefaq', 'answer_es', 'LONGTEXT NULL'),
        ('catalog_tvsize', 'size_es', 'VARCHAR(50) NULL'),
        ('catalog_availabletime', 'time_slot_es', 'VARCHAR(100) NULL'),
        ('catalog_newspost', 'title_es', 'VARCHAR(255) NULL'),
        ('catalog_newspost', 'content_es', 'LONGTEXT NULL'),
        ('catalog_category', 'name_es', 'VARCHAR(100) NULL'),
        ('catalog_subcategory', 'name_es', 'VARCHAR(100) NULL'),
        ('catalog_maincategory', 'name_es', 'VARCHAR(100) NULL'),
        ('catalog_feature', 'title_es', 'VARCHAR(255) NULL'),
        ('catalog_installationtype', 'name_es', 'VARCHAR(100) NULL'),
        ('catalog_project', 'title_es', 'VARCHAR(100) NULL'),
        ('catalog_project', 'subtitle_es', 'VARCHAR(100) NULL'),
        ('catalog_project', 'location_es', 'VARCHAR(100) NULL'),
        ('catalog_catalogue', 'title_es', 'VARCHAR(100) NULL'),
        ('catalog_certificate', 'title_es', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'title_es', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'subtitle_es', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'button_text_es', 'VARCHAR(50) NULL'),

        # Portuguese (_pt) columns
        ('catalog_product', 'title_pt', 'VARCHAR(255) NULL'),
        ('catalog_product', 'short_description_pt', 'VARCHAR(255) NULL'),
        ('catalog_product', 'description_pt', 'LONGTEXT NULL'),
        ('catalog_product', 'tags_pt', 'LONGTEXT NULL'),
        ('catalog_productbulletfeature', 'title_pt', 'VARCHAR(255) NULL'),
        ('catalog_productbulletfeature', 'text_pt', 'LONGTEXT NULL'),
        ('catalog_productspecification', 'key_pt', 'VARCHAR(200) NULL'),
        ('catalog_productspecification', 'value_pt', 'VARCHAR(500) NULL'),
        ('catalog_blogpost', 'title_pt', 'VARCHAR(255) NULL'),
        ('catalog_blogpost', 'short_description_pt', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'content_pt', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'author_pt', 'VARCHAR(100) NULL'),
        ('catalog_service', 'name_pt', 'VARCHAR(100) NULL'),
        ('catalog_service', 'description_pt', 'LONGTEXT NULL'),
        ('catalog_servicefaq', 'question_pt', 'VARCHAR(255) NULL'),
        ('catalog_servicefaq', 'answer_pt', 'LONGTEXT NULL'),
        ('catalog_tvsize', 'size_pt', 'VARCHAR(50) NULL'),
        ('catalog_availabletime', 'time_slot_pt', 'VARCHAR(100) NULL'),
        ('catalog_newspost', 'title_pt', 'VARCHAR(255) NULL'),
        ('catalog_newspost', 'content_pt', 'LONGTEXT NULL'),
        ('catalog_category', 'name_pt', 'VARCHAR(100) NULL'),
        ('catalog_subcategory', 'name_pt', 'VARCHAR(100) NULL'),
        ('catalog_maincategory', 'name_pt', 'VARCHAR(100) NULL'),
        ('catalog_feature', 'title_pt', 'VARCHAR(255) NULL'),
        ('catalog_installationtype', 'name_pt', 'VARCHAR(100) NULL'),
        ('catalog_project', 'title_pt', 'VARCHAR(100) NULL'),
        ('catalog_project', 'subtitle_pt', 'VARCHAR(100) NULL'),
        ('catalog_project', 'location_pt', 'VARCHAR(100) NULL'),
        ('catalog_catalogue', 'title_pt', 'VARCHAR(100) NULL'),
        ('catalog_certificate', 'title_pt', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'title_pt', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'subtitle_pt', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'button_text_pt', 'VARCHAR(50) NULL'),

        # French (_fr) columns
        ('catalog_product', 'title_fr', 'VARCHAR(255) NULL'),
        ('catalog_product', 'short_description_fr', 'VARCHAR(255) NULL'),
        ('catalog_product', 'description_fr', 'LONGTEXT NULL'),
        ('catalog_product', 'tags_fr', 'LONGTEXT NULL'),
        ('catalog_productbulletfeature', 'title_fr', 'VARCHAR(255) NULL'),
        ('catalog_productbulletfeature', 'text_fr', 'LONGTEXT NULL'),
        ('catalog_productspecification', 'key_fr', 'VARCHAR(200) NULL'),
        ('catalog_productspecification', 'value_fr', 'VARCHAR(500) NULL'),
        ('catalog_blogpost', 'title_fr', 'VARCHAR(255) NULL'),
        ('catalog_blogpost', 'short_description_fr', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'content_fr', 'LONGTEXT NULL'),
        ('catalog_blogpost', 'author_fr', 'VARCHAR(100) NULL'),
        ('catalog_service', 'name_fr', 'VARCHAR(100) NULL'),
        ('catalog_service', 'description_fr', 'LONGTEXT NULL'),
        ('catalog_servicefaq', 'question_fr', 'VARCHAR(255) NULL'),
        ('catalog_servicefaq', 'answer_fr', 'LONGTEXT NULL'),
        ('catalog_tvsize', 'size_fr', 'VARCHAR(50) NULL'),
        ('catalog_availabletime', 'time_slot_fr', 'VARCHAR(100) NULL'),
        ('catalog_newspost', 'title_fr', 'VARCHAR(255) NULL'),
        ('catalog_newspost', 'content_fr', 'LONGTEXT NULL'),
        ('catalog_category', 'name_fr', 'VARCHAR(100) NULL'),
        ('catalog_subcategory', 'name_fr', 'VARCHAR(100) NULL'),
        ('catalog_maincategory', 'name_fr', 'VARCHAR(100) NULL'),
        ('catalog_feature', 'title_fr', 'VARCHAR(255) NULL'),
        ('catalog_installationtype', 'name_fr', 'VARCHAR(100) NULL'),
        ('catalog_project', 'title_fr', 'VARCHAR(100) NULL'),
        ('catalog_project', 'subtitle_fr', 'VARCHAR(100) NULL'),
        ('catalog_project', 'location_fr', 'VARCHAR(100) NULL'),
        ('catalog_catalogue', 'title_fr', 'VARCHAR(100) NULL'),
        ('catalog_certificate', 'title_fr', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'title_fr', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'subtitle_fr', 'VARCHAR(100) NULL'),
        ('catalog_offer', 'button_text_fr', 'VARCHAR(50) NULL'),
    ]

    import warnings
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*Accessing the database during app initialization.*")
            with connection.cursor() as cursor:
                for tbl, col, col_def in cols_to_check:
                    try:
                        cursor.execute(f"SHOW COLUMNS FROM `{tbl}` LIKE %s", [col])
                        if not cursor.fetchone():
                            cursor.execute(f"ALTER TABLE `{tbl}` ADD COLUMN `{col}` {col_def}")
                            logger.info(f"Added missing column '{col}' to table '{tbl}'")
                    except Exception as col_err:
                        logger.debug(f"Column check notice for {tbl}.{col}: {col_err}")
    except Exception as db_err:
        logger.debug(f"Database connection not ready during ensure_all_database_columns: {db_err}")


def remove_conflicting_frontend_middleware():
    """
    Next.js 16 uses proxy.ts exclusively and throws an error if both
    middleware.ts and proxy.ts exist.
    """
    try:
        from django.conf import settings
        frontend_middleware = os.path.join(settings.BASE_DIR.parent, "skilltech-frontend", "middleware.ts")
        if os.path.exists(frontend_middleware):
            os.remove(frontend_middleware)
            logger.info("Successfully removed duplicate frontend middleware.ts for Next.js 16")
    except Exception as e:
        logger.debug(f"Middleware cleanup check: {e}")


def auto_populate_spanish_content():
    """
    Ensures existing BlogPosts, ServiceFAQs and NewsPosts have Spanish translations populated.
    """
    try:
        from .models import BlogPost, ServiceFAQ, NewsPost
        from .utils import translate_text

        # 1. Blog posts
        for post in BlogPost.objects.filter(content_es__isnull=True) | BlogPost.objects.filter(content_es=""):
            updated_fields = []
            if post.content:
                post.content_es = translate_text(post.content, target_lang="es")
                updated_fields.append("content_es")
            if not post.title_es and post.title:
                post.title_es = translate_text(post.title, target_lang="es")[:255]
                updated_fields.append("title_es")
            if not post.short_description_es and post.short_description:
                post.short_description_es = translate_text(post.short_description, target_lang="es")
                updated_fields.append("short_description_es")
            if not post.author_es and post.author:
                post.author_es = translate_text(post.author, target_lang="es")[:100]
                updated_fields.append("author_es")
            if updated_fields:
                post.save(update_fields=updated_fields)

        # 2. Service FAQs
        for faq in ServiceFAQ.objects.filter(question_es__isnull=True) | ServiceFAQ.objects.filter(question_es=""):
            updated_fields = []
            if faq.question:
                faq.question_es = translate_text(faq.question, target_lang="es")[:255]
                updated_fields.append("question_es")
            if not faq.answer_es and faq.answer:
                faq.answer_es = translate_text(faq.answer, target_lang="es")
                updated_fields.append("answer_es")
            if updated_fields:
                faq.save(update_fields=updated_fields)

        # 3. News posts
        for news in NewsPost.objects.filter(content_es__isnull=True) | NewsPost.objects.filter(content_es=""):
            updated_fields = []
            if news.content:
                news.content_es = translate_text(news.content, target_lang="es")
                updated_fields.append("content_es")
            if not news.title_es and news.title:
                news.title_es = translate_text(news.title, target_lang="es")[:255]
                updated_fields.append("title_es")
            if updated_fields:
                news.save(update_fields=updated_fields)

        # 4. Offers
        from .models import Offer
        for offer in Offer.objects.all():
            updated_fields = []
            if not offer.title_es and offer.title:
                offer.title_es = translate_text(offer.title, target_lang="es")[:100]
                updated_fields.append("title_es")
            if not offer.subtitle_es and offer.subtitle:
                offer.subtitle_es = translate_text(offer.subtitle, target_lang="es")[:100]
                updated_fields.append("subtitle_es")
            if not offer.button_text_es and offer.button_text:
                offer.button_text_es = translate_text(offer.button_text, target_lang="es")[:50]
                updated_fields.append("button_text_es")
            if not offer.title_hi and offer.title:
                offer.title_hi = translate_text(offer.title, target_lang="hi")[:100]
                updated_fields.append("title_hi")
            if not offer.subtitle_hi and offer.subtitle:
                offer.subtitle_hi = translate_text(offer.subtitle, target_lang="hi")[:100]
                updated_fields.append("subtitle_hi")
            if not offer.button_text_hi and offer.button_text:
                offer.button_text_hi = translate_text(offer.button_text, target_lang="hi")[:50]
                updated_fields.append("button_text_hi")
            if updated_fields:
                offer.save(update_fields=updated_fields)

        # 5. Fix any mistranslated LED TV Category
        from .models import Category
        for cat in Category.objects.filter(name__icontains="LED") | Category.objects.filter(slug__in=["tv", "led-tv"]):
            cat_updated = []
            if cat.name_hi and "नेतृत्व" in cat.name_hi:
                cat.name_hi = "एलईडी टीवी"
                cat_updated.append("name_hi")
            if not cat.name_es:
                cat.name_es = "Televisores LED" if "tv" in cat.slug else translate_text(cat.name, target_lang="es")[:100]
                cat_updated.append("name_es")
            if cat_updated:
                cat.save(update_fields=cat_updated)
    except Exception as e:
        logger.debug(f"Spanish auto-populate notice: {e}")


def auto_populate_portuguese_content():
    """
    Ensures existing BlogPosts, ServiceFAQs, NewsPosts, Categories and Offers have Portuguese translations populated.
    """
    try:
        from .models import BlogPost, ServiceFAQ, NewsPost, Offer, Category
        from .utils import translate_text

        # 1. Blog posts
        for post in BlogPost.objects.filter(content_pt__isnull=True) | BlogPost.objects.filter(content_pt=""):
            updated_fields = []
            if post.content:
                post.content_pt = translate_text(post.content, target_lang="pt")
                updated_fields.append("content_pt")
            if not post.title_pt and post.title:
                post.title_pt = translate_text(post.title, target_lang="pt")[:255]
                updated_fields.append("title_pt")
            if not post.short_description_pt and post.short_description:
                post.short_description_pt = translate_text(post.short_description, target_lang="pt")
                updated_fields.append("short_description_pt")
            if not post.author_pt and post.author:
                post.author_pt = translate_text(post.author, target_lang="pt")[:100]
                updated_fields.append("author_pt")
            if updated_fields:
                post.save(update_fields=updated_fields)

        # 2. Service FAQs
        for faq in ServiceFAQ.objects.filter(question_pt__isnull=True) | ServiceFAQ.objects.filter(question_pt=""):
            updated_fields = []
            if faq.question:
                faq.question_pt = translate_text(faq.question, target_lang="pt")[:255]
                updated_fields.append("question_pt")
            if not faq.answer_pt and faq.answer:
                faq.answer_pt = translate_text(faq.answer, target_lang="pt")
                updated_fields.append("answer_pt")
            if updated_fields:
                faq.save(update_fields=updated_fields)

        # 3. News posts
        for news in NewsPost.objects.filter(content_pt__isnull=True) | NewsPost.objects.filter(content_pt=""):
            updated_fields = []
            if news.content:
                news.content_pt = translate_text(news.content, target_lang="pt")
                updated_fields.append("content_pt")
            if not news.title_pt and news.title:
                news.title_pt = translate_text(news.title, target_lang="pt")[:255]
                updated_fields.append("title_pt")
            if updated_fields:
                news.save(update_fields=updated_fields)

        # 4. Offers
        for offer in Offer.objects.all():
            updated_fields = []
            if not offer.title_pt and offer.title:
                offer.title_pt = translate_text(offer.title, target_lang="pt")[:100]
                updated_fields.append("title_pt")
            if not offer.subtitle_pt and offer.subtitle:
                offer.subtitle_pt = translate_text(offer.subtitle, target_lang="pt")[:100]
                updated_fields.append("subtitle_pt")
            if not offer.button_text_pt and offer.button_text:
                offer.button_text_pt = translate_text(offer.button_text, target_lang="pt")[:50]
                updated_fields.append("button_text_pt")
            if updated_fields:
                offer.save(update_fields=updated_fields)

        # 5. Categories
        for cat in Category.objects.filter(name_pt__isnull=True) | Category.objects.filter(name_pt=""):
            if "tv" in cat.slug or "led-tv" in cat.slug:
                cat.name_pt = "Televisores LED"
            else:
                cat.name_pt = translate_text(cat.name, target_lang="pt")[:100]
            cat.save(update_fields=["name_pt"])

        # 6. Main Categories & SubCategories
        from .models import MainCategory, SubCategory
        for mc in MainCategory.objects.filter(name_pt__isnull=True) | MainCategory.objects.filter(name_pt=""):
            mc.name_pt = translate_text(mc.name, target_lang="pt")[:100]
            mc.save(update_fields=["name_pt"])

        for sc in SubCategory.objects.filter(name_pt__isnull=True) | SubCategory.objects.filter(name_pt=""):
            sc.name_pt = translate_text(sc.name, target_lang="pt")[:100]
            sc.save(update_fields=["name_pt"])

        # 7. Products
        from .models import Product
        for prod in Product.objects.filter(title_pt__isnull=True) | Product.objects.filter(title_pt=""):
            updated_fields = []
            if not prod.title_pt and (prod.title or prod.name):
                prod.title_pt = translate_text(prod.title or prod.name, target_lang="pt")[:255]
                updated_fields.append("title_pt")
            if not prod.short_description_pt and prod.short_description:
                prod.short_description_pt = translate_text(prod.short_description, target_lang="pt")
                updated_fields.append("short_description_pt")
            if not prod.description_pt and prod.description:
                prod.description_pt = translate_text(prod.description, target_lang="pt")
                updated_fields.append("description_pt")
            if not prod.tags_pt and prod.tags:
                tag_items = [t.strip() for t in prod.tags.split(',') if t.strip()]
                prod.tags_pt = ", ".join([translate_text(t, target_lang="pt") for t in tag_items])
                updated_fields.append("tags_pt")
            if updated_fields:
                prod.save(update_fields=updated_fields)

        # 8. Features & Bullet Features
        from .models import Feature, ProductBulletFeature
        for feat in Feature.objects.filter(title_pt__isnull=True) | Feature.objects.filter(title_pt=""):
            if feat.title:
                feat.title_pt = translate_text(feat.title, target_lang="pt")[:255]
                feat.save(update_fields=["title_pt"])

        for bf in ProductBulletFeature.objects.filter(title_pt__isnull=True) | ProductBulletFeature.objects.filter(title_pt=""):
            updated_fields = []
            if not bf.title_pt and bf.title:
                bf.title_pt = translate_text(bf.title, target_lang="pt")[:255]
                updated_fields.append("title_pt")
            if not bf.text_pt and bf.text:
                bf.text_pt = translate_text(bf.text, target_lang="pt")
                updated_fields.append("text_pt")
            if updated_fields:
                bf.save(update_fields=updated_fields)

        # 9. Specifications
        from .models import ProductSpecification
        for spec in ProductSpecification.objects.filter(key_pt__isnull=True) | ProductSpecification.objects.filter(key_pt=""):
            updated_fields = []
            if not spec.key_pt and spec.key:
                spec.key_pt = translate_text(spec.key, target_lang="pt")[:255]
                updated_fields.append("key_pt")
            if not spec.value_pt and spec.value:
                spec.value_pt = translate_text(spec.value, target_lang="pt")[:255]
                updated_fields.append("value_pt")
            if updated_fields:
                spec.save(update_fields=updated_fields)

        # 10. Service Installation types, TV sizes, Available times
        from .models import InstallationType, TVSize, AvailableTime
        for it in InstallationType.objects.filter(name_pt__isnull=True) | InstallationType.objects.filter(name_pt=""):
            if it.name:
                it.name_pt = translate_text(it.name, target_lang="pt")[:100]
                it.save(update_fields=["name_pt"])

        for ts in TVSize.objects.filter(size_pt__isnull=True) | TVSize.objects.filter(size_pt=""):
            if ts.size:
                ts.size_pt = translate_text(ts.size, target_lang="pt")[:100]
                ts.save(update_fields=["size_pt"])

        for at in AvailableTime.objects.filter(time_slot_pt__isnull=True) | AvailableTime.objects.filter(time_slot_pt=""):
            if at.time_slot:
                at.time_slot_pt = translate_text(at.time_slot, target_lang="pt")[:100]
                at.save(update_fields=["time_slot_pt"])
    except Exception as e:
        logger.debug(f"Portuguese auto-populate notice: {e}")


class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        import catalog.signals
        remove_conflicting_frontend_middleware()
        ensure_all_database_columns()

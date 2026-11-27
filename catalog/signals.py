import logging
import requests
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    Category, SubCategory, Product, ProductImage, ProductFeature,
    ProductBulletFeature, ProductSpecification, HomepageBanner, Offer,
    Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,
    Project, SEOPage, SiteSettings, Service, ServiceFAQ, BranchLocation,
    GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition,
    Arm, NewsPost, NewsCategory, CountrySetting, Feature, MainCategory
)

logger = logging.getLogger(__name__)

_TRANSLATION_CACHE = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def translate_text(text, target_lang='hi', source_lang='en'):
    if not text or not str(text).strip():
        return ""
    text_str = str(text).strip()

    cache_key = (source_lang, target_lang, text_str)
    if cache_key in _TRANSLATION_CACHE:
        return _TRANSLATION_CACHE[cache_key]

    # 1. Primary Engine: Google Translate GTX endpoint
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text_str
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                translated = "".join(seg[0] for seg in data[0] if seg and len(seg) > 0 and seg[0])
                if translated:
                    _TRANSLATION_CACHE[cache_key] = translated
                    return translated
    except Exception:
        pass

    # 2. Fallback Engine: MyMemory API (if Google rate-limits)
    try:
        mm_url = "https://api.mymemory.translated.net/get"
        mm_params = {
            "q": text_str[:500],
            "langpair": f"{source_lang}|{target_lang}"
        }
        mm_resp = requests.get(mm_url, params=mm_params, headers=HEADERS, timeout=5)
        if mm_resp.status_code == 200:
            mm_data = mm_resp.json()
            translated = mm_data.get("responseData", {}).get("translatedText")
            if translated and "MYMEMORY WARNING" not in str(translated).upper():
                _TRANSLATION_CACHE[cache_key] = translated
                return translated
    except Exception:
        pass

    return ""

@receiver(pre_save, sender=Product)
def auto_translate_product(sender, instance, **kwargs):
    try:
        # Hindi
        if instance.title and not instance.title_hi:
            instance.title_hi = (translate_text(instance.title, 'hi') or "")[:250]
        if instance.short_description and not instance.short_description_hi:
            instance.short_description_hi = (translate_text(instance.short_description, 'hi') or "")[:250]
        if instance.description and not instance.description_hi:
            instance.description_hi = translate_text(instance.description, 'hi')

        # Spanish
        if instance.title and hasattr(instance, 'title_es') and not instance.title_es:
            instance.title_es = (translate_text(instance.title, 'es') or "")[:250]
        if instance.short_description and hasattr(instance, 'short_description_es') and not instance.short_description_es:
            instance.short_description_es = (translate_text(instance.short_description, 'es') or "")[:250]
        if instance.description and hasattr(instance, 'description_es') and not instance.description_es:
            instance.description_es = translate_text(instance.description, 'es')

        # Portuguese
        if instance.title and hasattr(instance, 'title_pt') and not instance.title_pt:
            instance.title_pt = (translate_text(instance.title, 'pt') or "")[:250]
        if instance.short_description and hasattr(instance, 'short_description_pt') and not instance.short_description_pt:
            instance.short_description_pt = (translate_text(instance.short_description, 'pt') or "")[:250]
        if instance.description and hasattr(instance, 'description_pt') and not instance.description_pt:
            instance.description_pt = translate_text(instance.description, 'pt')

        # French
        if instance.title and hasattr(instance, 'title_fr') and not instance.title_fr:
            instance.title_fr = (translate_text(instance.title, 'fr') or "")[:250]
        if instance.short_description and hasattr(instance, 'short_description_fr') and not instance.short_description_fr:
            instance.short_description_fr = (translate_text(instance.short_description, 'fr') or "")[:250]
        if instance.description and hasattr(instance, 'description_fr') and not instance.description_fr:
            instance.description_fr = translate_text(instance.description, 'fr')

        # Arabic (if empty and admin didn't fill it)
        if instance.title and not instance.title_ar:
            instance.title_ar = (translate_text(instance.title, 'ar') or "")[:250]
        if instance.short_description and not instance.short_description_ar:
            instance.short_description_ar = (translate_text(instance.short_description, 'ar') or "")[:250]
        if instance.description and not instance.description_ar:
            instance.description_ar = translate_text(instance.description, 'ar')
    except Exception as e:
        logger.error(f"Error in auto_translate_product: {e}")

@receiver(pre_save, sender=MainCategory)
def auto_translate_maincategory(sender, instance, **kwargs):
    try:
        if instance.name and hasattr(instance, 'name_hi') and not instance.name_hi:
            instance.name_hi = translate_text(instance.name, 'hi')
        if instance.name and hasattr(instance, 'name_ar') and not instance.name_ar:
            instance.name_ar = translate_text(instance.name, 'ar')
        if instance.name and hasattr(instance, 'name_es') and not instance.name_es:
            instance.name_es = translate_text(instance.name, 'es')
        if instance.name and hasattr(instance, 'name_pt') and not instance.name_pt:
            instance.name_pt = translate_text(instance.name, 'pt')
        if instance.name and hasattr(instance, 'name_fr') and not instance.name_fr:
            instance.name_fr = translate_text(instance.name, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_maincategory: {e}")

@receiver(pre_save, sender=Category)
def auto_translate_category(sender, instance, **kwargs):
    try:
        if instance.name and hasattr(instance, 'name_hi') and not instance.name_hi:
            instance.name_hi = translate_text(instance.name, 'hi')
        if instance.name and hasattr(instance, 'name_ar') and not instance.name_ar:
            instance.name_ar = translate_text(instance.name, 'ar')
        if instance.name and hasattr(instance, 'name_es') and not instance.name_es:
            instance.name_es = translate_text(instance.name, 'es')
        if instance.name and hasattr(instance, 'name_pt') and not instance.name_pt:
            instance.name_pt = translate_text(instance.name, 'pt')
        if instance.name and hasattr(instance, 'name_fr') and not instance.name_fr:
            instance.name_fr = translate_text(instance.name, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_category: {e}")

@receiver(pre_save, sender=SubCategory)
def auto_translate_subcategory(sender, instance, **kwargs):
    try:
        if instance.name and hasattr(instance, 'name_hi') and not instance.name_hi:
            instance.name_hi = translate_text(instance.name, 'hi')
        if instance.name and hasattr(instance, 'name_ar') and not instance.name_ar:
            instance.name_ar = translate_text(instance.name, 'ar')
        if instance.name and hasattr(instance, 'name_es') and not instance.name_es:
            instance.name_es = translate_text(instance.name, 'es')
        if instance.name and hasattr(instance, 'name_pt') and not instance.name_pt:
            instance.name_pt = translate_text(instance.name, 'pt')
        if instance.name and hasattr(instance, 'name_fr') and not instance.name_fr:
            instance.name_fr = translate_text(instance.name, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_subcategory: {e}")

@receiver(pre_save, sender=Feature)
def auto_translate_feature(sender, instance, **kwargs):
    try:
        if instance.title and hasattr(instance, 'title_hi') and not instance.title_hi:
            instance.title_hi = translate_text(instance.title, 'hi')
        if instance.title and hasattr(instance, 'title_ar') and not instance.title_ar:
            instance.title_ar = translate_text(instance.title, 'ar')
        if instance.title and hasattr(instance, 'title_es') and not instance.title_es:
            instance.title_es = translate_text(instance.title, 'es')
        if instance.title and hasattr(instance, 'title_pt') and not instance.title_pt:
            instance.title_pt = translate_text(instance.title, 'pt')
        if instance.title and hasattr(instance, 'title_fr') and not instance.title_fr:
            instance.title_fr = translate_text(instance.title, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_feature: {e}")

@receiver(pre_save, sender=ProductBulletFeature)
def auto_translate_bullet_feature(sender, instance, **kwargs):
    try:
        if instance.title and hasattr(instance, 'title_hi') and not instance.title_hi:
            instance.title_hi = translate_text(instance.title, 'hi')
        if instance.title and hasattr(instance, 'title_ar') and not instance.title_ar:
            instance.title_ar = translate_text(instance.title, 'ar')
        if instance.title and hasattr(instance, 'title_es') and not instance.title_es:
            instance.title_es = translate_text(instance.title, 'es')
        if instance.title and hasattr(instance, 'title_pt') and not instance.title_pt:
            instance.title_pt = translate_text(instance.title, 'pt')
        if instance.title and hasattr(instance, 'title_fr') and not instance.title_fr:
            instance.title_fr = translate_text(instance.title, 'fr')
        if instance.text and hasattr(instance, 'text_hi') and not instance.text_hi:
            instance.text_hi = translate_text(instance.text, 'hi')
        if instance.text and hasattr(instance, 'text_ar') and not instance.text_ar:
            instance.text_ar = translate_text(instance.text, 'ar')
        if instance.text and hasattr(instance, 'text_es') and not instance.text_es:
            instance.text_es = translate_text(instance.text, 'es')
        if instance.text and hasattr(instance, 'text_pt') and not instance.text_pt:
            instance.text_pt = translate_text(instance.text, 'pt')
        if instance.text and hasattr(instance, 'text_fr') and not instance.text_fr:
            instance.text_fr = translate_text(instance.text, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_bullet_feature: {e}")

@receiver(pre_save, sender=Catalogue)
def auto_translate_catalogue(sender, instance, **kwargs):
    try:
        if instance.title and hasattr(instance, 'title_hi') and not instance.title_hi:
            instance.title_hi = translate_text(instance.title, 'hi')
        if instance.title and hasattr(instance, 'title_ar') and not instance.title_ar:
            instance.title_ar = translate_text(instance.title, 'ar')
        if instance.title and hasattr(instance, 'title_es') and not instance.title_es:
            instance.title_es = translate_text(instance.title, 'es')
        if instance.title and hasattr(instance, 'title_pt') and not instance.title_pt:
            instance.title_pt = translate_text(instance.title, 'pt')
        if instance.title and hasattr(instance, 'title_fr') and not instance.title_fr:
            instance.title_fr = translate_text(instance.title, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_catalogue: {e}")

@receiver(pre_save, sender=Certificate)
def auto_translate_certificate(sender, instance, **kwargs):
    try:
        if instance.title and hasattr(instance, 'title_hi') and not instance.title_hi:
            instance.title_hi = translate_text(instance.title, 'hi')
        if instance.title and hasattr(instance, 'title_ar') and not instance.title_ar:
            instance.title_ar = translate_text(instance.title, 'ar')
        if instance.title and hasattr(instance, 'title_es') and not instance.title_es:
            instance.title_es = translate_text(instance.title, 'es')
        if instance.title and hasattr(instance, 'title_pt') and not instance.title_pt:
            instance.title_pt = translate_text(instance.title, 'pt')
        if instance.title and hasattr(instance, 'title_fr') and not instance.title_fr:
            instance.title_fr = translate_text(instance.title, 'fr')
    except Exception as e:
        logger.error(f"Error in auto_translate_certificate: {e}")

# List of all models that should trigger cache clearing
CACHE_INVALIDATION_MODELS = [
    Category, SubCategory, Product, ProductImage, ProductFeature,
    ProductBulletFeature, ProductSpecification, HomepageBanner, Offer,
    Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,
    Project, SEOPage, SiteSettings, Service, ServiceFAQ, BranchLocation,
    GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition,
    Arm, NewsPost, NewsCategory, CountrySetting
]

def clear_cache_handler(sender, instance, **kwargs):
    """
    Clears the entire cache.
    """
    logger.info(f"Clearing cache due to change in {sender.__name__} (id={instance.pk})")
    cache.clear()

# Register post_save and post_delete receivers for each model
for model in CACHE_INVALIDATION_MODELS:
    post_save.connect(clear_cache_handler, sender=model)
    post_delete.connect(clear_cache_handler, sender=model)

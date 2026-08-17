import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    Category, SubCategory, Product, ProductImage, ProductFeature,
    ProductBulletFeature, ProductSpecification, HomepageBanner, Offer,
    Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,
    Project, SEOPage, SiteSettings, Service, ServiceFAQ, BranchLocation,
    GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition,
    Arm, NewsPost, NewsCategory
)

logger = logging.getLogger(__name__)

# List of all models that should trigger cache clearing
CACHE_INVALIDATION_MODELS = [
    Category, SubCategory, Product, ProductImage, ProductFeature,
    ProductBulletFeature, ProductSpecification, HomepageBanner, Offer,
    Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,
    Project, SEOPage, SiteSettings, Service, ServiceFAQ, BranchLocation,
    GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition,
    Arm, NewsPost, NewsCategory
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

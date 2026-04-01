from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, HomepageBannerViewSet
from catalog.views import OfferViewSet, ContactEnquiryViewSet, ServiceBookingViewSet, ClientViewSet, CatalogueViewSet, CertificateViewSet, GalleryViewSet, PageBannerViewSet, BlogPostViewSet, ProjectViewSet, SEOPageViewSet, SiteSettingsViewSet, ServiceViewSet, ServiceFAQViewSet, CareerApplicationViewSet, GlobalLocationViewSet, SitemapDataViewSet, StatisticViewSet, ServiceStatisticViewSet, generate_captcha, validate_captcha
from catalog.views import  NewsPostViewset
from catalog.views import CatalogueThumbnailDownloadView,MainCategoryViewSet,ArmsViewSet
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /static/",
        "Disallow: /media/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

router = DefaultRouter()
# ... (rest of router registrations remains same)
router.register(r'maincategories', MainCategoryViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet, basename='product')
# Allow slashes in lookup field
ProductViewSet.lookup_value_regex = r".+"
router.register(r'homepage-banners', HomepageBannerViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'contact', ContactEnquiryViewSet)
router.register(r'service-booking', ServiceBookingViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'catalogues', CatalogueViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'page-banners', PageBannerViewSet)
router.register(r'blogs', BlogPostViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'seo', SEOPageViewSet)
router.register(r'settings', SiteSettingsViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'service-faqs', ServiceFAQViewSet)
router.register(r'career-applications', CareerApplicationViewSet)
router.register(r'global-locations', GlobalLocationViewSet)
router.register(r'statistics', StatisticViewSet)
router.register(r'service-statistics', ServiceStatisticViewSet)
router.register(r'sitemap-data', SitemapDataViewSet, basename='sitemap-data'),
router.register(r'newspost',NewsPostViewset,basename="newspost"),
router.register(r'arms',ArmsViewSet,basename="arms")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/captcha/', generate_captcha, name='captcha'),
    path('api/validate-captcha/', validate_captcha, name='validate_captcha'),
    path('api/', include(router.urls)),
    path('robots.txt', robots_txt),
    path('api/catalogue/<int:pk>/download-thumbnail/',CatalogueThumbnailDownloadView.as_view(),name="catalogue-thumbnail-download")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path("__debug__/", include(debug_toolbar.urls)),
#     ]
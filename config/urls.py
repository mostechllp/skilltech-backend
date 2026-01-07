from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, HomepageBannerViewSet, OfferViewSet, ContactEnquiryViewSet, ServiceBookingViewSet, ClientViewSet, CatalogueViewSet, CertificateViewSet, GalleryViewSet, PageBannerViewSet, BlogPostViewSet, ProjectViewSet, SEOPageViewSet, SiteSettingsViewSet, ServiceViewSet, CareerViewSet, CareerApplicationViewSet, GlobalLocationViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet)
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
router.register(r'careers', CareerViewSet)
router.register(r'career-applications', CareerApplicationViewSet)
router.register(r'global-locations', GlobalLocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, HomepageBannerViewSet, OfferViewSet, ContactEnquiryViewSet, ServiceBookingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'homepage-banners', HomepageBannerViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'contact', ContactEnquiryViewSet)
router.register(r'service-booking', ServiceBookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

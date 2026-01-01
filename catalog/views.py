from rest_framework import viewsets, status, mixins
from .models import Category, SubCategory, Product, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, HomepageBannerSerializer, OfferSerializer, ProductEnquirySerializer, ContactEnquirySerializer, ServiceBookingSerializer, ClientSerializer, CatalogueSerializer, CertificateSerializer, GallerySerializer, PageBannerSerializer, BlogPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = SubCategory.objects.all()
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()
        subcategory_slug = self.request.query_params.get('subcategory_slug')
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        return queryset
    
    @action(detail=True, methods=['post'])
    def enquire(self, request, slug=None):
        product = self.get_object()
        serializer = ProductEnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response({'status': 'Enquiry submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomepageBannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomepageBanner.objects.filter(active=True).order_by('order')
    serializer_class = HomepageBannerSerializer

class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(active=True).order_by('order')
    serializer_class = OfferSerializer

class ContactEnquiryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactEnquiry.objects.all()
    serializer_class = ContactEnquirySerializer

class ServiceBookingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer

class ClientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Client.objects.filter(active=True).order_by('order')

    serializer_class = ClientSerializer



class CatalogueViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Catalogue.objects.filter(active=True).order_by('order')

    serializer_class = CatalogueSerializer



class CertificateViewSet(viewsets.ReadOnlyModelViewSet):



    queryset = Certificate.objects.filter(active=True).order_by('order')



    serializer_class = CertificateSerializer







class GalleryViewSet(viewsets.ReadOnlyModelViewSet):







    queryset = Gallery.objects.all().order_by('-created_at')







    serializer_class = GallerySerializer







    







    def get_queryset(self):







        queryset = Gallery.objects.all().order_by('-created_at')







        category_slug = self.request.query_params.get('category_slug')







        if category_slug:







            queryset = queryset.filter(category__slug=category_slug)







        return queryset















class PageBannerViewSet(viewsets.ReadOnlyModelViewSet):















    queryset = PageBanner.objects.all()















    serializer_class = PageBannerSerializer















    lookup_field = 'page'































class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):















    queryset = BlogPost.objects.filter(active=True).order_by('-created_at')















    serializer_class = BlogPostSerializer















    lookup_field = 'slug'





























from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductFeature, ProductSpecification, ProductImage, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost, Project,SEOPage, SiteSettings, Service, InstallationType, TVSize, AvailableTime, Career, CareerApplication, GlobalLocation

class InstallationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationType
        fields = ['id', 'name']

class TVSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVSize
        fields = ['id', 'size']

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = ['id', 'time_slot']

class ServiceSerializer(serializers.ModelSerializer):
    installation_types = InstallationTypeSerializer(many=True, read_only=True)
    tv_sizes = TVSizeSerializer(many=True, read_only=True)
    available_times = AvailableTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'

class CareerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerApplication
        fields = '__all__'

class GlobalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalLocation
        fields = '__all__'

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['screen_size', 'vesa_compatibility', 'profile_to_wall', 'weight_capacity', 'screen_rotation', 'direction_indicator', 'curved_tv']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['key', 'value']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    category_slug = serializers.CharField(source='subcategory.category.slug', read_only=True)
    category=serializers.CharField(source='subcategory.category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'

class HomepageBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageBanner
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class ProductEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEnquiry
        fields = '__all__'
        read_only_fields = ['product']

class ContactEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactEnquiry
        fields = '__all__'

class ServiceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBooking
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):

    class Meta:

        model = Client

        fields = '__all__'



class CatalogueSerializer(serializers.ModelSerializer):

    class Meta:

        model = Catalogue

        fields = '__all__'



class CertificateSerializer(serializers.ModelSerializer):



    class Meta:



        model = Certificate



        fields = '__all__'







class GallerySerializer(serializers.ModelSerializer):







    category_slug = serializers.CharField(source='category.slug', read_only=True)







    







    class Meta:







        model = Gallery







        fields = '__all__'















class PageBannerSerializer(serializers.ModelSerializer):















    class Meta:















        model = PageBanner















        fields = '__all__'































class BlogPostSerializer(serializers.ModelSerializer):































    tags = serializers.SerializerMethodField()































































    class Meta:































        model = BlogPost































        fields = '__all__'































































    def get_tags(self, obj):































        if not obj.tags:































            return []































        return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]































































class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = '__all__'



class SEOPageSerializer(serializers.ModelSerializer):

    class Meta:

        model = SEOPage

        fields = '__all__'

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

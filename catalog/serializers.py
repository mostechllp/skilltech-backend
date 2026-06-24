from rest_framework import serializers
from .models import Category, Feature, ProductSeo, SubCategory, Product, ProductFeature, ProductBulletFeature, ProductSpecification
from .models import  ProductImage, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client
from .models import  Catalogue, Certificate, Gallery, PageBanner, BlogPost, Project,SEOPage, SiteSettings, Service
from .models import  InstallationType, TVSize, AvailableTime, ServiceFAQ, CareerApplication, GlobalLocation, ServiceStatistic,HomeStatistic,MainCategory, CareerPosition
from .models import NewsCategory,NewsPost,Arm

class CareerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPosition
        fields = '__all__'

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

class ServiceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = ['id', 'question', 'answer', 'order']

class ServiceSerializer(serializers.ModelSerializer):
    installation_types = InstallationTypeSerializer(many=True, read_only=True)
    tv_sizes = TVSizeSerializer(many=True, read_only=True)
    available_times = AvailableTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


class CareerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerApplication
        fields = '__all__'

class GlobalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalLocation
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feature
        fields=['id','title','order']

class ProductFeatureSerializer(serializers.ModelSerializer):
    feature=FeatureSerializer(read_only=True)
    class Meta:
        model = ProductFeature
        fields = ['feature','value','icon']

class ProductBulletFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBulletFeature
        fields = ['id', 'title', 'text', 'order']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['key', 'value']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

class ProductSeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSeo
        fields = ['meta_title', 'meta_description', 'meta_image', 'meta_keywords', 'canonical_url']

class SimilarProductSerializer(serializers.ModelSerializer):
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    category_slug = serializers.CharField(source='subcategory.category.slug', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'title', 'slug','slug_path', 'main_image', 'main_image_alt', 'subcategory_slug', 'category_slug']

class CategorySerializer2(serializers.ModelSerializer):    
    class Meta:
        model = Category
        fields = '__all__'
class SubCategorySerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    products_count = serializers.IntegerField(read_only=True)
    category=CategorySerializer2()
    
    class Meta:
        model = SubCategory
        fields = '__all__'
    
   

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True,source='active_subcategories')
    
    class Meta:
        model = Category
        fields = '__all__'

class MainCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = MainCategory
        fields = ["id", "name", "slug", "order", "categories"]
class ProductListSerializer(serializers.ModelSerializer):
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    category_slug = serializers.CharField(source='subcategory.category.slug', read_only=True)
    category = serializers.CharField(source='subcategory.category.name', read_only=True)
    category_ar = serializers.CharField(source='subcategory.category.name_ar', read_only=True)
    
    class Meta:
        model = Product
        # Explicitly listing fields is safer and faster than '__all__'
        fields = [
            'id', 'name', 'title', 'slug', 'slug_path',
            'main_image', 'main_image_alt', 
            'short_description', 
            'subcategory_slug', 'category_slug', 'category', 'category_ar',
            'show_in_home', 'active', 'order','show_economic'
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True, read_only=True)
    bullet_features = ProductBulletFeatureSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    seo = ProductSeoSerializer(read_only=True)
    similar_products = SimilarProductSerializer(many=True, read_only=True)
    subcategory = SubCategorySerializer()

    class Meta:
        model = Product
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

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStatistic
        fields = '__all__'

class ServiceStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStatistic
        fields = '__all__'

class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsPost
        fields="__all__"

class ArmSerializer(serializers.ModelSerializer):
    class Meta:
        model=Arm
        fields="__all__"
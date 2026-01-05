from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductFeature, ProductSpecification, ProductImage, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost, Project,SEOPage

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['description']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['key', 'value']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    category_slug = serializers.CharField(source='subcategory.category.slug', read_only=True)

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















    class Meta:















        model = BlogPost















        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = '__all__'



class SEOPageSerializer(serializers.ModelSerializer):

    class Meta:

        model = SEOPage

        fields = '__all__'

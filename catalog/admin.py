from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, ProductFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'subcategory', 'slug')
    list_filter = ('subcategory', 'subcategory__category')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureInline, ProductSpecificationInline, ProductImageInline]

@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'active', 'order')
    list_editable = ('active', 'order')

@admin.register(ProductEnquiry)
class ProductEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'company', 'email', 'message', 'subject')
    readonly_fields = ('created_at',)

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'installation_type', 'date', 'time', 'created_at')
    list_filter = ('installation_type', 'date', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('name',)

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'category__name')

@admin.register(PageBanner)
class PageBannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'heading')
    search_fields = ('page', 'heading')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

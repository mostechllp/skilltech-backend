from django.contrib import admin
from .models import Category, Project, SubCategory, Product, ProductImage, ProductFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,SEOPage, SiteSettings, Service, InstallationType, TVSize, AvailableTime, Career, CareerApplication, GlobalLocation

class InstallationTypeInline(admin.TabularInline):
    model = InstallationType
    extra = 1

class TVSizeInline(admin.TabularInline):
    model = TVSize
    extra = 1

class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name', 'description')
    inlines = [InstallationTypeInline, TVSizeInline, AvailableTimeInline]

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('position', 'location', 'experience', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('position', 'location', 'description')
    prepopulated_fields = {'slug': ('position',)}

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'career', 'created_at')
    list_filter = ('career', 'created_at')
    search_fields = ('name', 'email', 'phone', 'cover_letter')
    readonly_fields = ('created_at',)

@admin.register(GlobalLocation)
class GlobalLocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'email', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('country', 'address')
    fields = ('country', 'address', 'email', 'map_iframe', 'map_link', 'active', 'order')

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
    list_display = ('name', 'slug', 'active')
    list_editable = ('active',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'active')
    list_editable = ('active',)
    list_filter = ('category', 'active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'subcategory', 'slug', 'active')
    list_editable = ('active',)
    list_filter = ('subcategory', 'subcategory__category', 'active')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureInline, ProductSpecificationInline, ProductImageInline]

@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')
    fields = ('subtitle', 'title', 'description', 'button_text', 'button_link', 'image', 'active', 'order')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'active', 'order')
    list_editable = ('active', 'order')
    fields=('subtitle','title','image','button_text','button_link','active','order')

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
    list_display = ('page', 'title')
    search_fields = ('page', 'title')
    fields = ('page', 'subtitle', 'title', 'description', 'button_text', 'button_link', 'image')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=('title','subtitle','location','image','order','active')

    

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(SEOPage)
    
class SEOAdmin(admin.ModelAdmin):
    
    list_display = ("page","meta_title","meta_description","meta_image","meta_keywords")
    

    
@admin.register(SiteSettings)
    

    
class SiteSettingsAdmin(admin.ModelAdmin):
    

    
    list_display = ('email', 'phone', 'phone_number2', 'demo')
    

    

    

    
    def has_add_permission(self, request):
    

    

    
        # Limit to only one instance
    
        if self.model.objects.exists():
    
            return False
    
        return super().has_add_permission(request)
    
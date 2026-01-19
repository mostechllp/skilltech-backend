from django.contrib import admin
from .models import Category, Project, SubCategory, Product, ProductImage, ProductFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,SEOPage, SiteSettings, Service, ServiceFAQ, InstallationType, TVSize, AvailableTime, Career, CareerApplication, GlobalLocation, HomeStatistic, ServiceStatistic
from .models import ProductSeo,Feature
from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult,Error

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

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductSeoInline(admin.StackedInline):
    model = ProductSeo

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

class ProductResource(resources.ModelResource):
    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=ForeignKeyWidget(SubCategory, 'name')  # or 'slug'
    )
    class Meta:
        model = Product
        import_id_fields = ['name']
        skip_unchanged = True
        report_skipped = True
        fields=('name','title','slug','subcategory','order','active','description')

    def import_row(self, row, instance_loader, **kwargs):
        name = (row.get("name") or "").strip()

        # ✅ Skip duplicates (don’t update existing)
        if name and Product.objects.filter(name__iexact=name).exists():
            rr = RowResult()
            rr.import_type = RowResult.IMPORT_TYPE_SKIP
            rr.diff = [f"Skipped: Product name '{name}' already exists"]
            return rr

        # ✅ If any error happens in this row, skip it and continue others
        try:
            rr = super().import_row(row, instance_loader, **kwargs)
        except Exception as e:
            rr = RowResult()
            rr.import_type = RowResult.IMPORT_TYPE_SKIP
            rr.diff = [f"Skipped: {type(e).__name__}: {e}"]
            return rr

        # ✅ If import-export reports validation errors in rr.errors, convert to SKIP
        if getattr(rr, "errors", None):
            rr.import_type = RowResult.IMPORT_TYPE_SKIP
            rr.diff = [f"Skipped: {rr.errors[0]}"]
            rr.errors = []  # so it appears under "Skipped" not "Errors"

        return rr
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'title', 'subcategory','order', 'slug', 'active')
    list_editable = ('active','order')
    list_filter = ('subcategory', 'subcategory__category', 'active')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureInline, ProductSpecificationInline, ProductImageInline,ProductSeoInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "similar_products":
            if request.resolver_match and request.resolver_match.kwargs.get('object_id'):
                kwargs["queryset"] = Product.objects.exclude(pk=request.resolver_match.kwargs.get('object_id'))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'active')

@admin.register(HomeStatistic)
class HomeStatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'value')

@admin.register(ServiceStatistic)
class ServiceStatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'value')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)




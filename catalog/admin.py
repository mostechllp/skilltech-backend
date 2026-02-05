from django.contrib import admin
from .models import Category, LogEntryExtra, Project, SubCategory, Product, ProductImage, ProductFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,SEOPage, SiteSettings, Service, ServiceFAQ, InstallationType, TVSize, AvailableTime, Career, CareerApplication, GlobalLocation, HomeStatistic, ServiceStatistic
from .models import ProductSeo,Feature,MainCategory
from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult,Error
from catalog.mixins import AdminIPLogMixin

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
class ServiceAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name', 'description')
    inlines = [InstallationTypeInline, TVSizeInline, AvailableTimeInline]

@admin.register(Career)
class CareerAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('position', 'location', 'experience', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('position', 'location', 'description')
    prepopulated_fields = {'slug': ('position',)}

@admin.register(CareerApplication)
class CareerApplicationAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'career', 'created_at')
    list_filter = ('career', 'created_at')
    search_fields = ('name', 'email', 'phone', 'cover_letter')
    readonly_fields = ('created_at',)

@admin.register(GlobalLocation)
class GlobalLocationAdmin(AdminIPLogMixin, admin.ModelAdmin):
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

@admin.register(MainCategory)
class MainCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'order')
    list_editable = ('active','order')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Category)
class CategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'order')
    list_editable = ('active','order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
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
class ProductAdmin(AdminIPLogMixin, ImportExportModelAdmin):
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
class HomepageBannerAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('link','active', 'order')
    list_editable = ('active', 'order')
    fields = ('link', 'image', 'image_alt','active', 'order')

@admin.register(Offer)
class OfferAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'active', 'order')
    list_editable = ('active', 'order')
    fields=('subtitle','title','image','button_text','button_link','active','order')

@admin.register(ProductEnquiry)
class ProductEnquiryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'company', 'email', 'message', 'subject')
    readonly_fields = ('created_at',)

@admin.register(ServiceBooking)
class ServiceBookingAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'installation_type', 'date', 'time', 'created_at')
    list_filter = ('installation_type', 'date', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Client)
class ClientAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('name',)

@admin.register(Catalogue)
class CatalogueAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title',)

@admin.register(Certificate)
class CertificateAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title',)

@admin.register(Gallery)
class GalleryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'category__name')

@admin.register(PageBanner)
class PageBannerAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('page', 'title')
    search_fields = ('page', 'title')
    fields = ('page', 'subtitle', 'title', 'description', 'button_text', 'button_link', 'image')

@admin.register(Project)
class ProjectAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display=('title','subtitle','location','image','order','active')

    

@admin.register(BlogPost)
class BlogPostAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(SEOPage)
    
class SEOAdmin(AdminIPLogMixin, admin.ModelAdmin):
    
    list_display = ("page","meta_title","meta_description","meta_image","meta_keywords")
    

    
@admin.register(SiteSettings)
    
class SiteSettingsAdmin(AdminIPLogMixin, admin.ModelAdmin):
    

    
    list_display = ('email', 'phone', 'phone_number2', 'demo')
    

    

    

    
    def has_add_permission(self, request):
    

    

    
        # Limit to only one instance
    
        if self.model.objects.exists():
    
            return False
    
        return super().has_add_permission(request)

@admin.register(ServiceFAQ)
class ServiceFAQAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('question', 'active')

@admin.register(HomeStatistic)
class HomeStatisticAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'value')

@admin.register(ServiceStatistic)
class ServiceStatisticAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'value')

@admin.register(Feature)
class FeatureAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)



@admin.register(LogEntryExtra)
class LogEntryExtraAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ("id", "get_action_time", "get_user", "get_action_flag", "ip_address")
    search_fields = ("log_entry__object_repr", "log_entry__change_message", "log_entry__user__username")
    list_filter = ("log_entry__action_flag", "log_entry__content_type", "log_entry__user")
    ordering = ("-log_entry__action_time",)

    readonly_fields = (
        "get_user",
        "get_content_type",
        "get_object_id",
        "get_object_repr",
        "get_action_flag",
        "get_change_message",
        "get_action_time",
        "ip_address",
    )

    fieldsets = (
        (None, {"fields": ("get_user", "get_content_type", "get_object_id", "get_object_repr")}),
        ("Action", {"fields": ("get_action_flag", "get_change_message")}),
        ("Meta", {"fields": ("get_action_time", "ip_address")}),
    )

    def get_user(self, obj):
        return obj.log_entry.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'log_entry__user'

    def get_content_type(self, obj):
        return obj.log_entry.content_type
    get_content_type.short_description = 'Content Type'
    get_content_type.admin_order_field = 'log_entry__content_type'

    def get_object_id(self, obj):
        return obj.log_entry.object_id
    get_object_id.short_description = 'Object ID'

    def get_object_repr(self, obj):
        return obj.log_entry.object_repr
    get_object_repr.short_description = 'Object Repr'
    
    def get_action_flag(self, obj):
        return obj.log_entry.action_flag
    get_action_flag.short_description = 'Action Flag'
    get_action_flag.admin_order_field = 'log_entry__action_flag'

    def get_change_message(self, obj):
        return obj.log_entry.change_message
    get_change_message.short_description = 'Change Message'

    def get_action_time(self, obj):
        return obj.log_entry.action_time
    get_action_time.short_description = 'Action Time'
    get_action_time.admin_order_field = 'log_entry__action_time'
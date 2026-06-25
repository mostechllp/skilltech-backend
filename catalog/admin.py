from django.contrib import admin
from .models import Category, LogEntryExtra, Project, SubCategory, Product, ProductImage, ProductFeature, ProductBulletFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,SEOPage, SiteSettings, Service, ServiceFAQ, InstallationType, TVSize, AvailableTime, CareerApplication, GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition

@admin.register(CareerPosition)
class CareerPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('name',)
from .models import ProductSeo,Feature,MainCategory,NewsCategory,NewsPost,Arm
from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult,Error
from catalog.mixins import AdminIPLogMixin
from django import forms
from .forms import ProductAdminForm

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


@admin.register(CareerApplication)
class CareerApplicationAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'created_at')
    list_filter = ('position', 'created_at')
    search_fields = ('name', 'email', 'phone', 'cover_letter')
    readonly_fields = ('created_at',)

@admin.register(GlobalLocation)
class GlobalLocationAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('country', 'country_ar', 'email', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('country', 'country_ar', 'address', 'address_ar')
    fields = ('country', 'country_ar', 'address', 'address_ar', 'email', 'map_iframe', 'map_link', 'active', 'order')

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature

class ProductBulletFeatureInline(admin.StackedInline):
    model = ProductBulletFeature
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductSeoInline(admin.StackedInline):
    model = ProductSeo

@admin.register(Arm)
class ArmAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'order', 'slug', 'active')
    list_editable = ('order',)
    search_fields = ('name', 'name_ar')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MainCategory)
class MainCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'order')
    list_editable = ('active','order')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Category)
class CategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'slug', 'active', 'order','homepage_order')
    list_editable = ('active','order','homepage_order',)
    search_fields=('name', 'name_ar')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'category', 'slug','order', 'active')
    list_editable = ('active','order')
    search_fields=('name', 'name_ar')
    list_filter = ('category', 'active')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'name_ar', 'slug', 'image', 'active', 'order', 'multi_expand')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_image', 'meta_keywords', 'canonical_url'),
            'classes': ('collapse',),
        }),
    )

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
    form = ProductAdminForm
    # def save_model(self, request, obj, form, change):
    #     category = form.cleaned_data.get("category")

    #     if category and obj.subcategory:
    #         if obj.subcategory.category != category:
    #             # optional: reset or validate
    #             pass

    #     super().save_model(request, obj, form, change)
    fields = [
        # 🔥 Priority fields (top)
        "category","subcategory","arm_fk","name","title",
        # Basic content
        "slug","slug_path","short_description","description",
        # Images
        "main_image","main_image_alt","drawing_image","drawing_image_alt","box_3d_image","box_3d_image_alt","video_url","product_video_url",

        "tags",
        # Files
        "datasheet",
        # Flags
        "show_in_home","show_cbm_calculator","show_economic","active",
        # Relations
        "similar_products",
        # CBM Calculator
        "units_per_carton","carton_length_cm","carton_width_cm","carton_height_cm","gross_weight_per_carton_kg","net_weight_per_carton_kg",
        # Meta
        "order","created_at","updated_at",
    ]

    readonly_fields = ["created_at", "updated_at"]
    list_display = ('name', 'title', 'subcategory','order', 'slug', 'active')
    list_editable = ('active','order')
    list_filter = ('subcategory', 'subcategory__category', 'active')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureInline, ProductBulletFeatureInline, ProductSpecificationInline, ProductImageInline,ProductSeoInline]

    def save_model(self, request, obj, form, change):
        # Generate slug_path only if it's empty
        if not obj.slug_path:
            category_slug = obj.subcategory.category.slug if obj.subcategory else ""
            subcategory_slug = obj.subcategory.slug if obj.subcategory else ""
            product_slug = obj.slug

            # Build slug_path safely
            parts = [category_slug, subcategory_slug, product_slug]
            obj.slug_path = "/".join([p for p in parts if p])

        super().save_model(request, obj, form, change)

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
    list_display = ('title', 'title_ar', 'subtitle', 'subtitle_ar', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar', 'subtitle', 'subtitle_ar')
    fields = (
        'title', 'title_ar',
        'subtitle', 'subtitle_ar',
        'image',
        'button_text', 'button_text_ar',
        'button_link', 'button_link_ar',
        'active', 'order'
    )

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
    list_display = ('title', 'title_ar', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar')

@admin.register(Certificate)
class CertificateAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar')

@admin.register(Gallery)
class GalleryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'title_ar', 'category__name')

@admin.register(PageBanner)
class PageBannerAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('page', 'title')
    search_fields = ('page', 'title')
    fields = ('page', 'subtitle', 'title', 'description', 'button_text', 'button_link', 'image')

@admin.register(Project)
class ProjectAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display=('title', 'title_ar', 'subtitle', 'subtitle_ar', 'location', 'location_ar', 'image', 'order', 'active')
    search_fields=('title', 'title_ar', 'subtitle', 'subtitle_ar', 'location', 'location_ar')
    fields = (
        'title', 'title_ar',
        'subtitle', 'subtitle_ar',
        'location', 'location_ar',
        'image', 'order', 'active'
    )

    

@admin.register(BlogPost)
class BlogPostAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'title_ar', 'content', 'content_ar', 'author', 'author_ar')
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'title_ar',
        'slug',
        'image', 'image_ar',
        'short_description', 'short_description_ar',
        'content', 'content_ar',
        'tags',
        'author', 'author_ar',
        'active'
    )
    
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
    list_display = ('question', 'question_ar', 'active')
    search_fields = ('question', 'question_ar', 'answer', 'answer_ar')

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
    list_display = ('title', 'title_ar', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'title_ar')



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

@admin.register(NewsCategory)
class NewsCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    pass

@admin.register(NewsPost)
class NewsPostAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'category', 'status', 'published_at', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'title_ar', 'content', 'content_ar')

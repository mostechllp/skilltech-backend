from django.contrib import admin
import csv
import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.urls import path
from .models import Category, LogEntryExtra, Project, SubCategory, Product, ProductImage, ProductFeature, ProductBulletFeature, ProductSpecification, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, QuoteRequest, ServiceBooking, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost,SEOPage, SiteSettings, Service, ServiceFAQ, InstallationType, TVSize, AvailableTime, CareerApplication, GlobalLocation, HomeStatistic, ServiceStatistic, CareerPosition, BranchLocation, CountrySetting

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
    fields = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru')
    extra = 1

class TVSizeInline(admin.TabularInline):
    model = TVSize
    fields = ('size', 'size_ar', 'size_hi', 'size_es', 'size_pt', 'size_fr', 'size_ru')
    extra = 1

class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    fields = ('time_slot', 'time_slot_ar', 'time_slot_hi', 'time_slot_es', 'time_slot_pt', 'time_slot_fr', 'time_slot_ru')
    extra = 1

@admin.register(Service)
class ServiceAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'active')
    search_fields = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'description', 'description_ar', 'description_hi', 'description_es', 'description_pt', 'description_fr', 'description_ru')
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

@admin.register(BranchLocation)
class BranchLocationAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'icon', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar', 'address', 'address_ar')
    fields = ('title', 'title_ar', 'icon', 'address', 'address_ar', 'tel1', 'tel2', 'email', 'working_hours', 'working_hours_ar', 'active', 'order')


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature
    fields = ('feature', 'value', 'icon', 'show_on_card')
    extra = 1

class ProductBulletFeatureInline(admin.StackedInline):
    model = ProductBulletFeature
    fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'text', 'text_ar', 'text_hi', 'text_es', 'text_pt', 'text_fr', 'text_ru', 'order')
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    fields = ('key', 'key_ar', 'key_hi', 'key_es', 'key_pt', 'key_fr', 'key_ru', 'value', 'value_ar', 'value_hi', 'value_es', 'value_pt', 'value_fr', 'value_ru')
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
    list_display = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'slug', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Category)
class CategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'slug', 'active', 'order','homepage_order')
    list_editable = ('active','order','homepage_order',)
    search_fields=('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'category', 'slug','order', 'active')
    list_editable = ('active','order')
    search_fields=('name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru')
    list_filter = ('category', 'active')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'name_ar', 'name_hi', 'name_es', 'name_pt', 'name_fr', 'name_ru', 'slug', 'image', 'active', 'order', 'multi_expand')
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
        "category","subcategory","arm_fk","name","title", "title_ar", "title_hi", "title_es", "title_pt", "title_fr", "title_ru",
        # Basic content
        "slug","slug_path","short_description","short_description_ar","short_description_hi","short_description_es","short_description_pt","short_description_fr","short_description_ru","description","description_ar","description_hi","description_es","description_pt","description_fr","description_ru",
        # Images
        "main_image","main_image_alt","drawing_image","drawing_image_alt","box_3d_image","box_3d_image_alt","video_url","product_video_url",

        "tags","tags_ar","tags_hi","tags_es","tags_pt","tags_fr","tags_ru",
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
    search_fields = ('name', 'title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'description', 'description_ar', 'description_hi', 'description_es', 'description_pt', 'description_fr', 'description_ru')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureInline, ProductBulletFeatureInline, ProductSpecificationInline, ProductImageInline,ProductSeoInline]

    def save_model(self, request, obj, form, change):
        # Ensure slug is generated first before computing slug_path
        if not obj.slug:
            from django.utils.text import slugify
            obj.slug = slugify(obj.name)

        category_slug = obj.subcategory.category.slug if (obj.subcategory and obj.subcategory.category) else ""
        subcategory_slug = obj.subcategory.slug if obj.subcategory else ""
        product_slug = obj.slug

        parts = [category_slug, subcategory_slug, product_slug]
        full_slug_path = "/".join([p for p in parts if p])

        # If slug_path is missing or incomplete (missing product slug), generate it
        if not obj.slug_path or obj.slug_path.count('/') < 2:
            obj.slug_path = full_slug_path

        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "similar_products":
            if request.resolver_match and request.resolver_match.kwargs.get('object_id'):
                kwargs["queryset"] = Product.objects.exclude(pk=request.resolver_match.kwargs.get('object_id'))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(HomepageBanner)
class HomepageBannerAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('link', 'active', 'order')
    list_editable = ('active', 'order')
    fields = ('link', 'image', 'image_ar', 'image_alt', 'active', 'order')

@admin.register(Offer)
class OfferAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'subtitle', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'subtitle', 'subtitle_ar')
    fields = (
        'title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru',
        'subtitle', 'subtitle_ar', 'subtitle_hi', 'subtitle_es', 'subtitle_pt', 'subtitle_fr', 'subtitle_ru',
        'image',
        'button_text', 'button_text_ar', 'button_text_hi', 'button_text_es', 'button_text_pt', 'button_text_fr', 'button_text_ru',
        'button_link', 'button_link_ar',
        'active', 'order'
    )

@admin.register(ProductEnquiry)
class ProductEnquiryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('reference_number', 'name', 'email', 'phone', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('reference_number', 'name', 'email', 'message')
    readonly_fields = ('reference_number', 'created_at',)

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'company', 'email', 'message', 'subject')
    readonly_fields = ('created_at',)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('reference_number', 'full_name', 'company', 'email', 'phone', 'attachment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('reference_number', 'full_name', 'company', 'email', 'phone', 'requirements')
    readonly_fields = ('reference_number', 'created_at')

@admin.register(ServiceBooking)
class ServiceBookingAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('reference_number', 'name', 'email', 'phone', 'location', 'installation_type', 'date', 'time', 'created_at')
    list_filter = ('installation_type', 'date', 'created_at')
    search_fields = ('reference_number', 'name', 'email', 'phone', 'location')
    readonly_fields = ('reference_number', 'created_at',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='servicebooking_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        range_type = request.GET.get('range_type', 'this_month')
        filter_by = request.GET.get('filter_by', 'created_date')
        from_date_str = request.GET.get('from_date')
        to_date_str = request.GET.get('to_date')

        today = timezone.localtime(timezone.now()).date()

        try:
            if range_type == 'this_month':
                start_date = today.replace(day=1)
                # Next month's 1st day minus 1 day
                next_month = today.replace(day=28) + datetime.timedelta(days=4)
                end_date = next_month.replace(day=1) - datetime.timedelta(days=1)
            elif range_type == 'last_month':
                first_day_this_month = today.replace(day=1)
                end_date = first_day_this_month - datetime.timedelta(days=1)
                start_date = end_date.replace(day=1)
            elif range_type == 'custom':
                if not from_date_str or not to_date_str:
                    return HttpResponse("Please provide both From and To dates for custom range.", status=400)
                start_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(to_date_str, '%Y-%m-%d').date()
            else:
                return HttpResponse("Invalid range type.", status=400)
        except Exception as e:
            return HttpResponse(f"Error parsing dates: {e}", status=400)

        # Apply filtering
        if filter_by == 'scheduled_date':
            queryset = ServiceBooking.objects.filter(date__range=(start_date, end_date)).order_by('-date')
        else:
            queryset = ServiceBooking.objects.filter(created_at__date__range=(start_date, end_date)).order_by('-created_at')

        # Generate CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="service_bookings_{start_date}_to_{end_date}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Reference Number', 'Name', 'Email', 'Phone', 'Location', 'Installation Type', 'Booking Date', 'Booking Time', 'Created At'])

        for booking in queryset:
            created_at_local = timezone.localtime(booking.created_at)
            writer.writerow([
                booking.reference_number,
                booking.name,
                booking.email,
                booking.phone,
                booking.location,
                booking.installation_type,
                booking.date.strftime('%Y-%m-%d') if booking.date else '',
                booking.time,
                created_at_local.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return response

@admin.register(Client)
class ClientAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('name',)

@admin.register(Catalogue)
class CatalogueAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru')
    fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'thumbnail', 'file', 'order', 'active')

@admin.register(Certificate)
class CertificateAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru')
    fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'thumbnail', 'file', 'order', 'active')

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
    list_display=('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'subtitle', 'location', 'image', 'order', 'active')
    search_fields=('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'subtitle', 'location')
    fields = (
        'title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru',
        'subtitle', 'subtitle_ar', 'subtitle_hi', 'subtitle_es', 'subtitle_pt', 'subtitle_fr', 'subtitle_ru',
        'location', 'location_ar', 'location_hi', 'location_es', 'location_pt', 'location_fr', 'location_ru',
        'image', 'order', 'active'
    )

@admin.register(BlogPost)
class BlogPostAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru',
        'slug',
        'image', 'image_ar',
        'short_description', 'short_description_ar', 'short_description_hi', 'short_description_es', 'short_description_pt', 'short_description_fr', 'short_description_ru',
        'content', 'content_ar', 'content_hi', 'content_es', 'content_pt', 'content_fr', 'content_ru',
        'tags',
        'author', 'author_ar', 'author_hi', 'author_es', 'author_pt', 'author_fr', 'author_ru',
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
    list_display = ('question', 'question_ar', 'question_hi', 'question_es', 'question_pt', 'question_fr', 'question_ru', 'active')
    search_fields = ('question', 'question_ar', 'question_hi', 'question_es', 'question_pt', 'question_fr', 'question_ru', 'answer', 'answer_ar', 'answer_hi', 'answer_es', 'answer_pt', 'answer_fr', 'answer_ru')
    fields = ('question', 'question_ar', 'question_hi', 'question_es', 'question_pt', 'question_fr', 'question_ru', 'answer', 'answer_ar', 'answer_hi', 'answer_es', 'answer_pt', 'answer_fr', 'answer_ru', 'order', 'active')

@admin.register(HomeStatistic)
class HomeStatisticAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('label', 'label_ar', 'value', 'value_ar', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'label_ar', 'value', 'value_ar')

@admin.register(ServiceStatistic)
class ServiceStatisticAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('label', 'label_ar', 'value', 'value_ar', 'suffix', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('label', 'label_ar', 'value', 'value_ar')

@admin.register(Feature)
class FeatureAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru')
    fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'order')



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
    list_display = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'category', 'status', 'published_at', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'title_ar', 'title_hi', 'title_es', 'title_pt', 'title_fr', 'title_ru', 'content', 'content_ar', 'content_hi', 'content_es', 'content_pt', 'content_fr')



# =====================================================================
# Visitor Analytics Admin Dashboard
# =====================================================================
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from .models import VisitorLog


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'ip_address', 'country_badge', 'device_badge', 'path_display', 'referrer_display')
    list_filter = ('device_type', 'is_bot', 'country')
    search_fields = ('ip_address', 'path', 'country', 'referrer', 'user_agent')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 50
    actions = ['export_selected_as_csv']

    def export_selected_as_csv(self, request, queryset):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="visitor_reports_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date & Time', 'IP Address', 'Country', 'Country Code', 'Device Type', 'Is Bot', 'Visited Path', 'Referrer'])

        for log in queryset:
            writer.writerow([
                log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                log.ip_address,
                log.country,
                log.country_code or '',
                log.device_type,
                'Yes' if log.is_bot else 'No',
                log.path,
                log.referrer or ''
            ])
        return response
    export_selected_as_csv.short_description = "📥 Export selected to CSV (Excel)"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def country_badge(self, obj):
        flag = f" ({obj.country_code})" if obj.country_code else ""
        return f"{obj.country}{flag}"
    country_badge.short_description = 'Country'
    country_badge.admin_order_field = 'country'

    def device_badge(self, obj):
        colors = {
            'desktop': '#062e5c',
            'mobile': '#0ea5e9',
            'tablet': '#8b5cf6',
            'bot': '#ef4444',
        }
        color = colors.get(obj.device_type, '#6b7280')
        return format_html(
            '<span style="background: {}; color: #fff; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;">{}</span>',
            color,
            obj.device_type
        )
    device_badge.short_description = 'Device'
    device_badge.admin_order_field = 'device_type'

    def path_display(self, obj):
        return format_html('<code style="color: #062e5c; font-weight: 500;">{}</code>', obj.path[:60])
    path_display.short_description = 'Path'
    path_display.admin_order_field = 'path'

    def referrer_display(self, obj):
        if not obj.referrer:
            return '-'
        ref = obj.referrer
        short_ref = ref[:40] + ('...' if len(ref) > 40 else '')
        return format_html('<span title="{}">{}</span>', ref, short_ref)
    referrer_display.short_description = 'Referrer'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-report/', self.admin_site.admin_view(self.trigger_weekly_report), name='visitorlog-send-report'),
            path('preview-report/', self.admin_site.admin_view(self.preview_report_html), name='visitorlog-preview-report'),
            path('download-csv/', self.admin_site.admin_view(self.download_csv_report), name='visitorlog-download-csv'),
        ]
        return custom_urls + urls

    def preview_report_html(self, request):
        from catalog.management.commands.send_weekly_report import generate_weekly_report_data, build_email_html
        data = generate_weekly_report_data()
        html_content = build_email_html(data)
        return HttpResponse(html_content, content_type='text/html')

    def download_csv_report(self, request):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="all_visitor_reports_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date & Time', 'IP Address', 'Country', 'Country Code', 'Device Type', 'Is Bot', 'Visited Path', 'Referrer'])

        logs = VisitorLog.objects.filter(is_bot=False).order_by('-created_at')[:10000]
        for log in logs:
            writer.writerow([
                log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                log.ip_address,
                log.country,
                log.country_code or '',
                log.device_type,
                'Yes' if log.is_bot else 'No',
                log.path,
                log.referrer or ''
            ])
        return response

    def trigger_weekly_report(self, request):
        from catalog.management.commands.send_weekly_report import send_weekly_report_email
        from catalog.models import SiteSettings

        site_settings = SiteSettings.objects.first()
        if not site_settings or not site_settings.email_host or not site_settings.email_host_user:
            self.message_user(
                request,
                "SMTP configuration missing: Please fill in 'Email host', 'Email host user', and 'Email host password' under Catalog > Site Settings first.",
                messages.WARNING
            )
            return redirect('admin:catalog_visitorlog_changelist')

        try:
            recipient = send_weekly_report_email()
            self.message_user(request, f"Weekly visitor report successfully sent to {recipient}!", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Failed to send email: {e}", messages.ERROR)

        return redirect('admin:catalog_visitorlog_changelist')



@admin.register(CountrySetting)
class CountrySettingAdmin(AdminIPLogMixin, admin.ModelAdmin):
    list_display = ('country_name', 'country_code', 'phone', 'mobile', 'email', 'company_name', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('country_name', 'country_name_ar', 'country_code', 'email', 'phone', 'company_name')
    list_filter = ('active',)
    fieldsets = (
        ("Country Identification", {
            "fields": (("country_code", "country_name", "country_name_ar"), ("active", "order")),
            "description": "Select the GCC country code and enter English/Arabic country names.",
        }),
        ("Company & Copyright Details", {
            "fields": ("company_name", "copyright_text"),
            "description": "Displayed in the footer copyright notice and official company representation.",
        }),
        ("Contact Details", {
            "fields": (("phone", "mobile"), ("email", "whatsapp")),
            "description": "Displayed in the top header, footer, and floating WhatsApp button when this country is selected.",
        }),
        ("Office Address", {
            "fields": (("address_heading", "address_heading_ar"), "address", "address_ar"),
            "description": "Physical branch/office address shown in the footer and contact sections.",
        }),
    )

    def has_add_permission(self, request):
        """Prevent adding duplicate or non-GCC countries."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent accidental deletion of GCC countries."""
        return False

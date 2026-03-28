from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.admin.models import LogEntry
from django.utils import timezone


class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    order = models.DecimalField(max_digits=5, decimal_places=3, default=0.000, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
class Category(models.Model):
    main_category = models.ForeignKey(
        MainCategory,
        related_name="categories",
        on_delete=models.CASCADE,
        null=True,        # ✅ TEMP
        blank=True,       # ✅ TEMP
        db_index=True
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Recommended size: 400x400px (1:1 aspect ratio). Transparent PNG preferred.")
    show_in_home=models.BooleanField(default=False, db_index=True)
    show_in_explore_home=models.BooleanField(default=False, db_index=True)
    show_in_footer=models.BooleanField(default=False, db_index=True)
    # ✅ for Cables & Wires / Gaming
    flatten_in_menu = models.BooleanField(default=False, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    order=models.DecimalField(max_digits=5,decimal_places=3,default=0.000, db_index=True)

    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_image = models.ImageField(upload_to='categories/seo/', blank=True, null=True, help_text="Recommended size: 2400x1260px (Social media sharing).")
    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")
    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL for this category page")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True, help_text="Recommended size: 400x400px (1:1 aspect ratio).")
    active = models.BooleanField(default=True, db_index=True)
    order=models.DecimalField(max_digits=5,decimal_places=3,default=0.000, db_index=True)
    multi_expand=models.BooleanField(default=False)

    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_image = models.ImageField(upload_to='subcategories/seo/', blank=True, null=True, help_text="Recommended size: 2400x1260px (Social media sharing).")
    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")
    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL for this subcategory page")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category.name} - {self.name}'

    class Meta:
        verbose_name_plural = 'Sub Categories'

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Model Name, e.g., SH 380R',db_index=True)
    title = models.CharField(max_length=255, help_text='Full Title, e.g., 360 Rotate Wall Mount...',db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    slug_path = models.CharField(max_length=500)
    
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(help_text='Full product description')
    
    main_image = models.ImageField(upload_to='products/main/',max_length=500, help_text="Recommended size: 1600x1600px (1:1 aspect ratio). Transparent PNG preferred for listing consistency.")
    main_image_alt = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for SEO")
    drawing_image = models.ImageField(upload_to='products/drawings/',max_length=500, blank=True, null=True, help_text="Recommended size: 1200x800px or similar (Landscape/Technical drawing).")
    drawing_image_alt = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for SEO")
    
    box_3d_image = models.ImageField(upload_to='products/3dboxes/', max_length=500, blank=True, null=True, help_text="Recommended size: 1200x800px or similar.")
    box_3d_image_alt = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for SEO")
    
    video_url = models.URLField(blank=True, null=True, help_text='Installation Video URL')
    product_video_url = models.URLField(blank=True, null=True, help_text='Product Video URL')
    
    tags = models.TextField(blank=True, help_text='Comma separated tags, e.g. Tag1, Tag2')

    # New fields
    datasheet = models.FileField(upload_to='products/datasheets/',max_length=500, blank=True, null=True)
    show_in_home = models.BooleanField(default=False,db_index=True)
    similar_products = models.ManyToManyField('self', blank=True, related_name='similar_to')
    show_cbm_calculator = models.BooleanField(default=False)
    show_economic=models.BooleanField(default=False)    
    
    # CBM Calculator Fields
    units_per_carton = models.IntegerField(blank=True, null=True, help_text='Units per Carton')
    carton_length_cm = models.FloatField(blank=True, null=True, help_text='Carton Length in cm')
    carton_width_cm = models.FloatField(blank=True, null=True, help_text='Carton Width in cm')
    carton_height_cm = models.FloatField(blank=True, null=True, help_text='Carton Height in cm')
    gross_weight_per_carton_kg = models.FloatField(blank=True, null=True, help_text='Gross Weight per Carton in Kg')
    net_weight_per_carton_kg = models.FloatField(blank=True, null=True, help_text='Net Weight per Carton in Kg')

    ARM_CHOICES = [
        ('single', 'Single Arm'),
        ('double', 'Double Arm'),
        ('triple', 'Triple Arm'),
        ('four', 'Quad Arm'),
        ('dual','Dual Extension Arm'),
        ('six', 'Full Motion Multi Arm'),
    ]
    arm = models.CharField(max_length=10, choices=ARM_CHOICES, blank=True, null=True, db_index=True)

    active = models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order=models.DecimalField(max_digits=5,decimal_places=3,default=0.000,db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        indexes = [
            # CRITICAL OPTIMIZATION
            # Used in: SubCategorySerializer.get_products_count
            # Line: obj.products.filter(active=True).count()
            # Why: This lets the DB count active products for a subcategory instantly.
            models.Index(fields=['subcategory', 'active']),
        ]

class Feature(models.Model):
    title=models.CharField(max_length=100)
    order=models.DecimalField(max_digits=5,decimal_places=3,default=0.000)
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    feature=models.ForeignKey(Feature,related_name='product_features',on_delete=models.SET_NULL,blank=True,null=True)
    value=models.CharField(max_length=255) 
    icon=models.ImageField(upload_to='products/features/',blank=True,null=True,help_text="Icon for the feature. Recommended size: 400x400px (1:1 aspect ratio).")

    def __str__(self):
        return f'Features for {self.product.name}'

class ProductBulletFeature(models.Model):
    product = models.ForeignKey(Product, related_name='bullet_features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Bold part of the feature (e.g. 360° Screen Rotation)")
    text = models.TextField(help_text="Main description of the feature")
    order = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Bullet feature for {self.product.name}"

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.key}: {self.value}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/',max_length=500, help_text="Recommended size: 1600x1600px (1:1 aspect ratio).")
    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for SEO")
    order=models.DecimalField(max_digits=5,decimal_places=3,default=0.000)
    
    def __str__(self):
        return f'Image for {self.product.name}'
    
    class Meta:
        ordering = ['order']

class ProductSeo(models.Model):
    product = models.OneToOneField(Product, related_name='seo', on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_image = models.ImageField(upload_to='products/seo/', blank=True, null=True, help_text="Recommended size: 2400x1260px (Social media sharing).")
    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")
    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL for this product page")

    def __str__(self):
        return f'SEO for {self.product.name}'

class HomepageBanner(models.Model):
    link = models.CharField(max_length=200, default='/')
    image = models.ImageField(upload_to='banners/', help_text="Recommended size: 2000x2000px (1:1 aspect ratio) for square desktop rendering. Ensure focal point is centered.")
    image_alt = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for SEO")
    active = models.BooleanField(default=True)
    order = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)
    class Meta:
        ordering = ['order']


class Offer(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, help_text='e.g. New Arrival, Trending, Hot Pick')
    image = models.ImageField(upload_to='offers/', help_text="Size depends on position. Big: 1200x1200px, Small: 800x600px, Wide: 1600x600px.")
    button_text = models.CharField(max_length=50, default='Explore')
    button_link = models.CharField(max_length=200, default='/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ProductEnquiry(models.Model):
    product = models.ForeignKey(Product, related_name='enquiries', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Enquiry from {self.name} for {self.product.name}'

class ContactEnquiry(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Contact Enquiries'

    def __str__(self):
        return f'Contact from {self.name} - {self.company}'

class ServiceBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    installation_type = models.CharField(max_length=100)
    tv_size = models.CharField(max_length=50)
    bracket = models.BooleanField(default=False)
    date = models.DateField()
    time = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Service Booking from {self.name} on {self.date}'

class Client(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='clients/', help_text="Recommended size: 400x200px (Landscape). Transparent PNG preferred.")

    order = models.IntegerField(default=0, db_index=True)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.name



class Catalogue(models.Model):

    title = models.CharField(max_length=100)

    thumbnail = models.ImageField(upload_to='catalogues/thumbnails/', help_text="Recommended size: 600x800px (Portrait/Cover).")

    file = models.FileField(upload_to='catalogues/files/')

    order = models.IntegerField(default=0, db_index=True)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.title



class Certificate(models.Model):



    title = models.CharField(max_length=100)



    thumbnail = models.ImageField(upload_to='certificates/thumbnails/', help_text="Recommended size: 800x600px (Landscape).")



    file = models.FileField(upload_to='certificates/files/')



    order = models.IntegerField(default=0, db_index=True)



    active = models.BooleanField(default=True)







    class Meta:



        ordering = ['order']







    def __str__(self):



        return self.title







class Gallery(models.Model):
    category = models.ForeignKey(Category, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/', help_text="Recommended size: 1600x1200px (Landscape).")
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return f'Gallery image for {self.category.name}'

class PageBanner(models.Model):
    PAGE_CHOICES = [
        ('gallery', 'Gallery'),
        ('career', 'Career'),
        ('blog', 'Blog'),
    ]
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True, default='Explore')
    button_link = models.CharField(max_length=200, blank=True, default='/')
    image = models.ImageField(upload_to='page_banners/', help_text="Recommended size: 3200x1200px (Wide landscape).")
    
    def __str__(self):
        return f'Banner for {self.get_page_display()}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog/', help_text="Recommended size: 1600x1000px (Landscape).")
    content = models.TextField()
    short_description = models.TextField(blank=True, help_text="Summary displayed on the list page")
    tags = models.TextField(blank=True, help_text="Comma separated tags, e.g. Tech, News, Update")
    author = models.CharField(max_length=100, default="Admin")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Project(models.Model):

    title = models.CharField(max_length=100)

    subtitle = models.CharField(max_length=100, blank=True)

    location = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='projects/', help_text="Recommended size: 1200x800px (Landscape).")

    order = models.IntegerField(default=0, db_index=True)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.title



class SEOPage(models.Model):

    PAGE_CHOICES = [

        ('home', 'Home'),

        ('about', 'About Us'),

        ('services', 'Services'),

        ('support', 'Support'),

        ('gallery', 'Gallery'),

        ('career', 'Career'),

        ('blog', 'Blog'),

        ('contact', 'Contact'),

        ('news', 'News & Media'),

    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)

    meta_title = models.CharField(max_length=200, blank=True)

    meta_description = models.TextField(blank=True)

    meta_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text="Recommended size: 2400x1260px (Social media sharing).")

    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")

    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL for this page")


    def __str__(self):

        return self.get_page_display()


class SiteSettings(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True, verbose_name="X (Twitter)")
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    service_whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="WhatsApp number for service page")
    
    address_heading = models.CharField(max_length=100, blank=True, null=True, default="Our Office")
    address = models.TextField(blank=True, null=True, help_text="Enter address with line breaks")
    google_map_link = models.URLField(blank=True, null=True, help_text="Google Maps Location URL")

    demo = models.BooleanField(default=False, help_text="If checked, adds 'noindex' to meta tags")

    email_host = models.CharField(max_length=255)
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)
    admin_email = models.TextField(blank=True, null=True, help_text="Email address(es) to receive contact form submissions. Separate multiple emails with a comma (e.g. admin@example.com, support@example.com)")
    
    enable_captcha = models.BooleanField(default=True, help_text="Enable/Disable captcha verification for all forms")

    class Meta:
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Site Settings"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class InstallationType(models.Model):
    service = models.ForeignKey(Service, related_name='installation_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TVSize(models.Model):
    service = models.ForeignKey(Service, related_name='tv_sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size

class AvailableTime(models.Model):
    service = models.ForeignKey(Service, related_name='available_times', on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=100)

    def __str__(self):
        return self.time_slot

class ServiceFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service FAQ'
        verbose_name_plural = 'Service FAQs'

    def __str__(self):
        return f"{self.question}"



# class Career(models.Model):
#     position = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True, blank=True)
#     experience = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     description = models.TextField()
#     active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.position)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.position

class CareerApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='career_cvs/')
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"



class GlobalLocation(models.Model):
    country = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    map_iframe = models.TextField(help_text='Paste the full iframe code from Google Maps (Share -> Embed a map)')
    map_link = models.URLField(help_text='Google Maps Link (for Get Directions button)')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.country

class HomeStatistic(models.Model):
    value = models.IntegerField(help_text="Numeric value for the counter (e.g. 100 for 100K)")
    label = models.CharField(max_length=100, help_text="Label below the number (e.g. Projects)")
    suffix = models.CharField(max_length=20, blank=True, help_text="Suffix after number (e.g. K+, +)")
    icon = models.ImageField(upload_to='statistics/', blank=True, null=True, help_text="Optional icon")
    order = models.IntegerField(default=0, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} - {self.label}"

class ServiceStatistic(models.Model):
    value = models.IntegerField(help_text="Numeric value for the counter (e.g. 100 for 100K)")
    label = models.CharField(max_length=100, help_text="Label below the number (e.g. Projects)")
    suffix = models.CharField(max_length=20, blank=True, help_text="Suffix after number (e.g. K+, +)")
    icon = models.ImageField(upload_to='service_statistics/', blank=True, null=True, help_text="Optional icon")
    order = models.IntegerField(default=0, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} - {self.label}"

class LogEntryExtra(models.Model):
    log_entry = models.OneToOneField(LogEntry, on_delete=models.CASCADE, related_name="extra")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.log_entry_id} - {self.ip_address}"

    class Meta:
        verbose_name = "Log Entry"
        verbose_name_plural = "Log Entries"
    
class NewsCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)  # "Corporate News"
    slug = models.SlugField(max_length=140, unique=True,blank=True)  # "corporate-news"
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug=slugify(self.name)
            slug = base_slug
            counter = 1

            while NewsCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"

            self.slug = slug

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

class NewsPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    category = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    # For cards
    cover_image = models.ImageField(upload_to="news/", blank=True, null=True)

    # Main content (simple version)
    content = models.TextField()  # later you can replace with RichTextField / EditorJS\
    video_url=models.URLField(blank=True,null=True)

    # Publishing
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Control latest updates ordering (optional)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto slug
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while NewsPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug

        # Auto set published_at when publishing
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()


        super().save(*args, **kwargs)
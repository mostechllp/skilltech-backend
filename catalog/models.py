from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Recommended size: 400x400px (1:1 aspect ratio). Transparent PNG preferred.")
    show_in_home=models.BooleanField(default=False)
    show_in_explore_home=models.BooleanField(default=False)
    show_in_footer=models.BooleanField(default=False)
    active = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)

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
    name = models.CharField(max_length=100, help_text='Model Name, e.g., SH 380R')
    title = models.CharField(max_length=255, help_text='Full Title, e.g., 360 Rotate Wall Mount...')
    slug = models.SlugField(unique=True, blank=True)
    
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(help_text='Full product description')
    
    main_image = models.ImageField(upload_to='products/main/', help_text="Recommended size: 1600x1600px (1:1 aspect ratio). Transparent PNG preferred for listing consistency.")
    drawing_image = models.ImageField(upload_to='products/drawings/', blank=True, null=True, help_text="Recommended size: 1200x800px or similar (Landscape/Technical drawing).")
    
    video_url = models.URLField(blank=True, null=True, help_text='Installation Video URL')
    product_video_url = models.URLField(blank=True, null=True, help_text='Product Video URL')
    
    tags = models.TextField(blank=True, help_text='Comma separated tags, e.g. Tag1, Tag2')

    # New fields
    datasheet = models.FileField(upload_to='products/datasheets/', blank=True, null=True)
    show_in_home = models.BooleanField(default=False)
    show_cbm_calculator = models.BooleanField(default=False)
    
    # CBM Calculator Fields
    units_per_carton = models.IntegerField(blank=True, null=True, help_text='Units per Carton')
    carton_length_cm = models.FloatField(blank=True, null=True, help_text='Carton Length in cm')
    carton_width_cm = models.FloatField(blank=True, null=True, help_text='Carton Width in cm')
    carton_height_cm = models.FloatField(blank=True, null=True, help_text='Carton Height in cm')
    gross_weight_per_carton_kg = models.FloatField(blank=True, null=True, help_text='Gross Weight per Carton in Kg')
    net_weight_per_carton_kg = models.FloatField(blank=True, null=True, help_text='Net Weight per Carton in Kg')

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    screen_size = models.CharField(max_length=100, blank=True, null=True)
    vesa_compatibility = models.CharField(max_length=100, blank=True, null=True)
    profile_to_wall = models.CharField(max_length=100, blank=True, null=True)
    weight_capacity = models.CharField(max_length=100, blank=True, null=True)
    screen_rotation = models.CharField(max_length=100, blank=True, null=True)
    direction_indicator = models.CharField(max_length=100, blank=True, null=True)
    curved_tv = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Features for {self.product.name}'

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.key}: {self.value}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', help_text="Recommended size: 1600x1600px (1:1 aspect ratio).")
    
    def __str__(self):
        return f'Image for {self.product.name}'

class HomepageBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, default='Explore')
    button_link = models.CharField(max_length=200, default='/')
    image = models.ImageField(upload_to='banners/', help_text="Recommended size: 2000x2000px (1:1 aspect ratio) for square desktop rendering. Ensure focal point is centered.")
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Offer(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, help_text='e.g. New Arrival, Trending, Hot Pick')
    image = models.ImageField(upload_to='offers/', help_text="Size depends on position. Big: 1200x1200px, Small: 800x600px, Wide: 1600x600px.")
    button_text = models.CharField(max_length=50, default='Explore')
    button_link = models.CharField(max_length=200, default='/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

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

    order = models.IntegerField(default=0)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.name



class Catalogue(models.Model):

    title = models.CharField(max_length=100)

    thumbnail = models.ImageField(upload_to='catalogues/thumbnails/', help_text="Recommended size: 600x800px (Portrait/Cover).")

    file = models.FileField(upload_to='catalogues/files/')

    order = models.IntegerField(default=0)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.title



class Certificate(models.Model):



    title = models.CharField(max_length=100)



    thumbnail = models.ImageField(upload_to='certificates/thumbnails/', help_text="Recommended size: 800x600px (Landscape).")



    file = models.FileField(upload_to='certificates/files/')



    order = models.IntegerField(default=0)



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

    order = models.IntegerField(default=0)

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

    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)

    meta_title = models.CharField(max_length=200, blank=True)

    meta_description = models.TextField(blank=True)

    meta_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text="Recommended size: 2400x1260px (Social media sharing).")

    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")



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



class Career(models.Model):
    position = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.position)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position

class CareerApplication(models.Model):
    career = models.ForeignKey(Career, related_name='applications', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='career_cvs/')
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.career.position}"



class GlobalLocation(models.Model):
    country = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    map_iframe = models.TextField(help_text='Paste the full iframe code from Google Maps (Share -> Embed a map)')
    map_link = models.URLField(help_text='Google Maps Link (for Get Directions button)')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.country


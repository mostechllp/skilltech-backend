from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    show_in_home=models.BooleanField(default=False)
    show_in_explore_home=models.BooleanField(default=False)
    show_in_footer=models.BooleanField(default=False)

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
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True)

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
    
    main_image = models.ImageField(upload_to='products/main/')
    drawing_image = models.ImageField(upload_to='products/drawings/', blank=True, null=True)
    
    video_url = models.URLField(blank=True, null=True, help_text='Installation Video URL')
    product_video_url = models.URLField(blank=True, null=True, help_text='Product Video URL')
    
    tags = models.JSONField(default=list, blank=True, help_text='List of tags')

    # New fields
    datasheet = models.FileField(upload_to='products/datasheets/', blank=True, null=True)
    show_in_home = models.BooleanField(default=False)
    
    # CBM Calculator Fields
    units_per_carton = models.IntegerField(default=1, help_text='Units per Carton')
    carton_length_cm = models.FloatField(default=0, help_text='Carton Length in cm')
    carton_width_cm = models.FloatField(default=0, help_text='Carton Width in cm')
    carton_height_cm = models.FloatField(default=0, help_text='Carton Height in cm')
    gross_weight_per_carton_kg = models.FloatField(default=0, help_text='Gross Weight per Carton in Kg')
    net_weight_per_carton_kg = models.FloatField(default=0, help_text='Net Weight per Carton in Kg')

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
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.key}: {self.value}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    
    def __str__(self):
        return f'Image for {self.product.name}'

class HomepageBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, default='Explore')
    button_link = models.CharField(max_length=200, default='/')
    image = models.ImageField(upload_to='banners/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Offer(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, help_text='e.g. New Arrival, Trending, Hot Pick')
    image = models.ImageField(upload_to='offers/')
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
    INSTALLATION_TYPES = [
        ('normal', 'Normal Installation'),
        ('motorized', 'Motorized Bracket Installation'),
        ('wall_mount', 'Wall Mounting'),
        ('concealed', 'Concealed Wiring Setup'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    installation_type = models.CharField(max_length=50, choices=INSTALLATION_TYPES)
    tv_size = models.CharField(max_length=50)
    bracket = models.BooleanField(default=False)
    date = models.DateField()
    time = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Service Booking from {self.name} on {self.date}'

class Client(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='clients/')

    order = models.IntegerField(default=0)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.name



class Catalogue(models.Model):

    title = models.CharField(max_length=100)

    thumbnail = models.ImageField(upload_to='catalogues/thumbnails/')

    file = models.FileField(upload_to='catalogues/files/')

    order = models.IntegerField(default=0)

    active = models.BooleanField(default=True)



    class Meta:

        ordering = ['order']



    def __str__(self):

        return self.title



class Certificate(models.Model):



    title = models.CharField(max_length=100)



    thumbnail = models.ImageField(upload_to='certificates/thumbnails/')



    file = models.FileField(upload_to='certificates/files/')



    order = models.IntegerField(default=0)



    active = models.BooleanField(default=True)







    class Meta:



        ordering = ['order']







    def __str__(self):



        return self.title







class Gallery(models.Model):
    category = models.ForeignKey(Category, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
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
    heading = models.CharField(max_length=100)
    subheading = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='page_banners/')
    
    def __str__(self):
        return f'Banner for {self.get_page_display()}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    short_description = models.TextField(blank=True, help_text="Summary displayed on the list page")
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

    image = models.ImageField(upload_to='projects/')

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

    meta_image = models.ImageField(upload_to='seo/', blank=True, null=True)

    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords")



    def __str__(self):

        return self.get_page_display()

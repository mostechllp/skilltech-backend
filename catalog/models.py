from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

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
    description = models.TextField(blank=True, null=True)

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
    
    video_url = models.URLField(blank=True, null=True)
    
    features = models.JSONField(default=list, blank=True, help_text='List of features')
    specifications = models.JSONField(default=dict, blank=True, help_text='Key-Value pairs for specs')
    tags = models.JSONField(default=list, blank=True, help_text='List of tags')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    
    def __str__(self):
        return f'Image for {self.product.name}'

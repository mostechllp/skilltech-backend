from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
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
    inlines = [ProductImageInline]

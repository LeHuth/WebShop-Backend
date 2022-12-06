from django.contrib import admin
from .models import Product, Stock, Category, ProductImage


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Category)

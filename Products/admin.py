from django.contrib import admin
from .models import Product, Stock, Category, ProductImage, Review, Vote


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    readonly_fields = ('user','title','rating','text','created')


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ReviewInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Vote)

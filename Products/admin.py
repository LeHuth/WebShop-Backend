from django.contrib import admin
from .models import Product, Stock, Category, ProductImage, Review, Vote, Manufacturer, ProductPdf, Report


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0


class ProductPdfInline(admin.StackedInline):
    model = ProductPdf
    extra = 0


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    readonly_fields = ('member', 'title', 'rating', 'text', 'created')


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPdfInline, ReviewInline]
    filter_horizontal = ['variants']


class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReportInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Vote)
admin.site.register(Manufacturer)
admin.site.register(Report)

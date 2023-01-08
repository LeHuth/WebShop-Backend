from django.contrib import admin
from .models import Product, Stock, Category, ProductImage, Review, Vote, Manufacturer, ProductPdf, Report


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0

    def has_view_or_change_permission(self, request, obj=None):
        return True


class ProductPdfInline(admin.StackedInline):
    model = ProductPdf
    extra = 0


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)

    def has_view_or_change_permission(self, request, obj=None):
        return True


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    readonly_fields = ('member', 'title', 'rating', 'text', 'created')


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPdfInline, ReviewInline]
    filter_horizontal = ['variants']


class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReportInline]


class ReportAdmin(admin.ModelAdmin):
    model = Report


class ReportCustomerService(ReportAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return True


class ProductsCustomerService(ProductAdmin):

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_staff

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        self.readonly_fields = ('rating',)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Vote)
admin.site.register(Manufacturer)
admin.site.register(Report)

from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Member, MemberImage, MemberAddress


# Register your models here.

class MemberImageInline(admin.StackedInline):
    model = MemberImage
    extra = 0


class MemberAddressInline(admin.StackedInline):
    model = MemberAddress
    extra = 0
    readonly_fields = ('street', 'number', 'postalcode', 'city', 'country')


class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberImageInline, MemberAddressInline]


class MemberCustomerService(MemberAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return True

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        #self.readonly_fields = ('username',)
        self.exclude = ('password', 'groups',)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


#admin.site = admin_site = MemberAdminSite(name='memberadmin')
admin.site.register(Member, MemberAdmin)

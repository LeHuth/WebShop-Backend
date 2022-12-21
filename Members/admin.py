from django.contrib import admin
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


admin.site.register(Member, MemberAdmin)

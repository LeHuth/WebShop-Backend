from django.contrib.admin import AdminSite
from Members.admin import Member, MemberCustomerService
from Products.admin import Product, ProductsCustomerService, ReportCustomerService, Report


class CustomerServiceSite(AdminSite):
    site_header = 'Customer Service Portal'

    def has_permission(self, request):
        print(request.user.is_staff)
        return request.user.is_staff


customer_service_site = CustomerServiceSite(name='customer service')

customer_service_site.register(Member, MemberCustomerService)
customer_service_site.register(Product, ProductsCustomerService)
customer_service_site.register(Report, ReportCustomerService)

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Customer, PotentialCustomer

# Admin site başlığını değiştir
admin.site.site_header = 'Adverier CRM'
admin.site.site_title = 'Adverier CRM'
admin.site.index_title = 'Adverier CRM Yönetim Paneli'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'phone', 'email', 'address')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(PotentialCustomer)
class PotentialCustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email', 'address')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

from django.contrib import admin
from apps.accounts.models import CustomUser, Address, Opt


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(Opt)

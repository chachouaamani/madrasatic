from django.contrib import admin

# Register your models here.
from users.models import Users, Service,Role
from django.contrib.auth.admin import UserAdmin

admin.site.register(Role)


class CustomUserAdmin(UserAdmin):
    model=Users
    list_display = ('username', 'first_name', 'last_name', 'email', 'password', 'role', 'is_active')
    list_filter = ('role', 'last_name')
    search_fields = ('username', 'role')
    actions = ('desactivate_account', 'activate_account')
    fieldsets = (
        (None, {'fields': ('username','password','email', 'first_name', 'last_name','role','image')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Personal',{'fields':('is_staff','is_superuser','date_joined','last_login')}),
    )

    def desactivate_account(self, request, queryset):
        queryset.update(is_active=False)

    def activate_account(self, request, queryset):
        queryset.update(is_active=True)


admin.site.register(Users, CustomUserAdmin)

admin.site.site_header = 'Madrasa_tic'
admin.site.site_title = 'Madrasa_tic'

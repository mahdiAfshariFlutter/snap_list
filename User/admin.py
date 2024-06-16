from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from User.models import User, OtpCode


class MyUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']


class OtpCodeAdmin(admin.ModelAdmin):
    model = OtpCode
    list_display = ['id', 'email', 'code']


admin.site.register(User, MyUserAdmin)
admin.site.register(OtpCode, OtpCodeAdmin)

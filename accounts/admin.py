from .models import User, Profile
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'is_verified')


admin.site.register(User, UserAdmin)
admin.site.register(Profile)

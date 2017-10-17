from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'slug']
admin.site.register(UserProfile, UserProfileAdmin)
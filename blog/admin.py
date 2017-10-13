from django.contrib import admin

from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'created_time', 'modified_time', 'published', 'category']
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Tag, TagAdmin)

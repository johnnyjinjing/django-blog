from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Comment

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['author', 'post', 'body'[:20], 'created_time', 'parent']
# admin.site.register(Comment, CommentAdmin)

class CommentMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 16
    list_display = ['body'[:20], 'author', 'post', 'created_time', 'parent']

admin.site.register(Comment, CommentMPTTModelAdmin)
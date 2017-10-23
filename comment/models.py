from django.db import models
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    """ Comment
    """
    author = models.ForeignKey(User)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post')
    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['created_time']

    class Meta:
        ordering=['tree_id','lft']

    def __unicode__(self):
        return self.body[:20]
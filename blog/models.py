from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    """ Catagory of post
    name: name of the category, unique
    slug: slug, unque
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    """ Tag of post
    name: name of the tag, unique
    """

    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    """ Post
    author: author of the post, FK: User
    title: title of the post, unique
    body: body of the post
    created_time: time the post created
    modified_time: time the post created
    published: is the post published or in draft
    category: category of the post, FK: Category
    category: tags of the post, Many-To-Many: Tag, can be blank
    slug: slug, unique
    """

    author = models.ForeignKey(User)
    title = models.CharField(max_length=100, unique=True, default=None)
    body = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-created_time', 'title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title



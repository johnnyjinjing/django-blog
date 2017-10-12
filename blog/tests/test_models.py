from django.test import TestCase
from django.db import IntegrityError

from django.contrib.auth.models import User
from ..models import Category, Tag, Post

class CategoryModelTests(TestCase):
    """ test Category model
    """
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='test category')

    def test_category_name_max_length(self):
        """ the max length of category name is 100
        """
        cat = Category.objects.get(name='test category')
        max_length = cat._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_slug(self):
        """ test if slug name is correct
        """
        cat = Category.objects.get(name='test category')
        self.assertEqual(cat.slug, "test-category")

    def test_insert_same_category_name(self):
        """ insert category with same name is not allowed
        """
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='test category')

    def test_insert_same_slug(self):
        """ insert categoty with same slug is not allowed
        """
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='test-category')


class TagModelTests(TestCase):
    """ test Tag model
    """
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='test_tag')

    def test_tag_name_max_length(self):
        """ the max length of tag name is 100
        """
        tag = Tag.objects.get(name='test_tag')
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_insert_same_tag_name(self):
        """ insert tag with same name is not allowed
        """
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='test_tag')

class PostModelTests(TestCase):
    """ test Post model
    """
    @classmethod
    def setUpTestData(cls):
        # create a User
        cls.user = User.objects.create_user(username='test',
            email='test@test.com', password='testtest')
        cls.category = Category.objects.create(name='test category')
        Post.objects.create(author=cls.user, title='test_title',
            body='something here', category=cls.category)

    def test_author_required(self):
        """ author of post is requried
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(title='test_title_2',
            body='something here', category=self.category)

    def test_title_required(self):
        """ title of post is requried
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(author=self.user,
            body='something here', category=self.category)

    def test_title_unique(self):
        """ title of post is unique
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(author=self.user, title='test_title',
            body='something here', category=self.category)

    def test_body_blank(self):
        """ body of post can be blank
        """
        try:
            Post.objects.create(author=self.user, title='test_title_2',
            body='', category=self.category)
        except:
            self.fail()

    def test_published_default(self):
        """ published is defaulted to False
        """
        post = Post.objects.get(id=1)
        self.assertFalse(post.published)

    def test_category_required(self):
        """ category of post is required
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(author=self.user, title='test_title_2',
            body='something here')

    def test_multiple_tags(self):
        """ post can have more than 1 tags
        """

        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        post = Post.objects.create(author=self.user, title='test_title_2',
            body='something here', category=self.category)
        post.tags.add(tag1)
        post.tags.add(tag2)

        post = Post.objects.get(title='test_title_2')

        self.assertEqual(post.tags.all()[0].name, "tag1")
        self.assertEqual(post.tags.all()[1].name, "tag2")

    def test_slug(self):
        """ test if slug name is correct
        """
        post = Post.objects.get(id=1)
        self.assertEqual(post.slug, "test_title")

    def test_slug_unique(self):
        """ slug of Post is unique
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(title='test title',
            body='something here', category=self.category)

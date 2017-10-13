from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import Category, Tag, Post

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # user
        cls.user = User.objects.create_user(username='test',
            email='test@test.com', password='testtest')

        # category
        cls.category = Category.objects.create(name='test category')

        # tags
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")

        # posts
        post1 = Post.objects.create(author=cls.user, title='test_title',
            body='something here', category=cls.category, published=True)
        post2 = Post.objects.create(author=cls.user, title='test_title_2',
            body='something else here', category=cls.category, published=True)
        post2.tags.add(tag1)
        post3 = Post.objects.create(author=cls.user, title='test_title_3',
            body='much more stuff...', category=cls.category, published=True)
        post3.tags.add(tag1)
        post3.tags.add(tag2)
        post4 = Post.objects.create(author=cls.user, title='test_title_4',
            body='much more stuff...', category=cls.category)
        post4.tags.add(tag1)
        post4.tags.add(tag2)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('blog:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('blog:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/index.html')

    def test_lists_all_published_posts(self):
        resp = self.client.get(reverse('blog:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['post_list']), 3)
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from ..models import Category, Post, Tag


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.cate = Category.objects.create(name="测试")

    def test_str_representation(self):
        self.assertEqual(self.cate.__str__(), self.cate.name)


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="测试")

    def test_str_representation(self):
        self.assertEqual(self.tag.__str__(), self.tag.name)


class PostModelTestCase(TestCase):
    def setUp(self):
        # 断开 haystack 的 signal，测试生成的文章无需生成索引
        # apps.get_app_config('haystack').signal_processor.teardown()
        user = User.objects.create_superuser(
            username='admin', 
            email='admin@hellogithub.com', 
            password='admin')
        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = '新的测试内容'
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 54)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)


class BlogDataTestCase(TestCase):
    def setUp(self):
        # apps.get_app_config('haystack').signal_processor.teardown()

        # User
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@hellogithub.com',
            password='admin'
        )

        # 分类
        self.cate1 = Category.objects.create(name='测试分类一')
        self.cate2 = Category.objects.create(name='测试分类二')

        # 标签
        self.tag1 = Tag.objects.create(name='测试标签一')
        self.tag2 = Tag.objects.create(name='测试标签二')

        # 文章
        self.post1 = Post.objects.create(
            title='测试标题一',
            body='测试内容一',
            category=self.cate1,
            author=self.user,
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='测试标题二',
            body='测试内容二',
            category=self.cate2,
            author=self.user,
            created_time=timezone.now() - timedelta(days=100)
        )



class AdminTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('admin:blog_post_add')

    def test_set_author_after_publishing_the_post(self):
        data = {
            'title': '测试标题',
            'body': '测试内容',
            'category': self.cate1.pk,
        }
        self.client.login(username=self.user.username, password='admin')
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.all().latest('created_time')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, data.get('title'))
        self.assertEqual(post.category, self.cate1)

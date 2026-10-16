from django.test import TestCase
from rest_framework.test import APIClient

from account.models import User
from post.models import Post


class PostCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test', email='test@example.com', password='secret', is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def create_post(self, data):
        return self.client.post('/api/post/create/', data, format='multipart')

    def test_create_private_post(self):
        response = self.create_post({'body': 'private', 'is_private': 'true'})

        self.assertTrue(response.json()['is_private'])
        self.assertTrue(Post.objects.get(body='private').is_private)

    def test_create_public_post(self):
        response = self.create_post({'body': 'public', 'is_private': 'false'})

        self.assertFalse(response.json()['is_private'])
        self.assertFalse(Post.objects.get(body='public').is_private)

    def test_create_post_defaults_to_public(self):
        response = self.create_post({'body': 'default'})

        self.assertFalse(response.json()['is_private'])


class PrivatePostVisibilityTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            name='Author', email='author@example.com', password='secret', is_active=True)
        self.other = User.objects.create_user(
            name='Other', email='other@example.com', password='secret', is_active=True)
        self.private_post = Post.objects.create(
            body='secret #hidden', created_by=self.author, is_private=True)
        self.public_post = Post.objects.create(
            body='hello #hidden', created_by=self.author)

    def client_for(self, user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    def visible_bodies(self, user):
        client = self.client_for(user)
        profile = client.get(f'/api/post/profile/{self.author.id}/').json()['results']['posts']
        search = client.post('/api/search/', {'query': 'secret'}).json()['posts']
        trend = client.get('/api/post/', {'trend': 'hidden'}).json()['results']
        return {
            'profile': [post['body'] for post in profile],
            'search': [post['body'] for post in search],
            'trend': [post['body'] for post in trend],
        }

    def test_other_user_cannot_see_private_post_in_lists(self):
        for source, bodies in self.visible_bodies(self.other).items():
            self.assertNotIn('secret #hidden', bodies, source)
        self.assertIn('hello #hidden', self.visible_bodies(self.other)['profile'])

    def test_friend_cannot_see_private_post_in_feed(self):
        self.author.friends.add(self.other)

        feed = self.client_for(self.other).get('/api/post/').json()['results']

        self.assertEqual([post['body'] for post in feed], ['hello #hidden'])

    def test_other_user_cannot_access_private_post(self):
        client = self.client_for(self.other)
        post_url = f'/api/post/{self.private_post.id}'

        self.assertEqual(client.get(f'{post_url}/detail/').status_code, 404)
        self.assertEqual(client.post(f'{post_url}/like/').status_code, 404)
        self.assertEqual(client.post(f'{post_url}/comment/', {'comment': 'hi'}).status_code, 404)
        self.assertEqual(client.post(f'{post_url}/report/', {'reportText': 'spam'}).status_code, 404)

        self.private_post.refresh_from_db()
        self.assertEqual(self.private_post.likes_count, 0)
        self.assertEqual(self.private_post.comments_count, 0)

    def test_author_can_see_own_private_post(self):
        for source, bodies in self.visible_bodies(self.author).items():
            self.assertIn('secret #hidden', bodies, source)

        feed = self.client_for(self.author).get('/api/post/').json()['results']
        self.assertIn('secret #hidden', [post['body'] for post in feed])

        detail = self.client_for(self.author).get(f'/api/post/{self.private_post.id}/detail/')
        self.assertEqual(detail.status_code, 200)


class ReportPostTests(TestCase):
    def test_report_public_post(self):
        author = User.objects.create_user(
            name='Author', email='author@example.com', password='secret', is_active=True)
        reporter = User.objects.create_user(
            name='Reporter', email='reporter@example.com', password='secret', is_active=True)
        post = Post.objects.create(body='hello', created_by=author)
        client = APIClient()
        client.force_authenticate(reporter)

        response = client.post(f'/api/post/{post.id}/report/', {'reportText': 'spam'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.reports.get().report, 'spam')


class TrendFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test', email='test@example.com', password='secret', is_active=True)
        Post.objects.create(body='I like #python', created_by=self.user)
        Post.objects.create(body='I like #pythonista', created_by=self.user)
        Post.objects.create(body='I like #Python too', created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def trend_bodies(self, trend):
        response = self.client.get('/api/post/', {'trend': trend})
        self.assertEqual(response.status_code, 200)
        return sorted(post['body'] for post in response.json()['results'])

    def test_trend_matches_whole_hashtag_only(self):
        self.assertEqual(self.trend_bodies('python'), ['I like #Python too', 'I like #python'])

    def test_trend_with_regex_characters(self):
        for trend in ['(', 'pyth.*', '(a+)+$']:
            self.assertEqual(self.trend_bodies(trend), [], trend)


class DeleteCommentTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            name='Author', email='author@example.com', password='secret', is_active=True)
        self.commenter = User.objects.create_user(
            name='Commenter', email='commenter@example.com', password='secret', is_active=True)
        self.other = User.objects.create_user(
            name='Other', email='other@example.com', password='secret', is_active=True)
        self.post = Post.objects.create(body='post', created_by=self.author)
        self.other_post = Post.objects.create(body='other post', created_by=self.other)
        self.post.add_comment(self.commenter, 'comment')
        self.other_post.add_comment(self.commenter, 'other comment')
        self.comment = self.post.comments.get()
        self.other_comment = self.other_post.comments.get()

    def delete_comment(self, user, post, comment):
        client = APIClient()
        client.force_authenticate(user)
        return client.delete(f'/api/post/{post.id}/comment/{comment.id}/')

    def assert_comments_count(self, post, count):
        post.refresh_from_db()
        self.assertEqual(post.comments.count(), count)
        self.assertEqual(post.comments_count, count)

    def test_comment_author_can_delete_comment(self):
        response = self.delete_comment(self.commenter, self.post, self.comment)

        self.assertEqual(response.status_code, 200)
        self.assert_comments_count(self.post, 0)

    def test_post_author_can_delete_comment(self):
        response = self.delete_comment(self.author, self.post, self.comment)

        self.assertEqual(response.status_code, 200)
        self.assert_comments_count(self.post, 0)

    def test_other_user_cannot_delete_comment(self):
        response = self.delete_comment(self.other, self.post, self.comment)

        self.assertEqual(response.status_code, 404)
        self.assert_comments_count(self.post, 1)

    def test_cannot_delete_comment_through_other_post(self):
        response = self.delete_comment(self.commenter, self.post, self.other_comment)

        self.assertEqual(response.status_code, 404)
        self.assert_comments_count(self.post, 1)
        self.assert_comments_count(self.other_post, 1)

    def test_post_author_cannot_delete_comment_on_other_post(self):
        response = self.delete_comment(self.author, self.post, self.other_comment)

        self.assertEqual(response.status_code, 404)
        self.assert_comments_count(self.other_post, 1)


class InvalidPostRequestTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            name='Author', email='author@example.com', password='secret', is_active=True)
        self.other = User.objects.create_user(
            name='Other', email='other@example.com', password='secret', is_active=True)
        self.post = Post.objects.create(body='hello', created_by=self.author)
        self.client = APIClient()
        self.client.force_authenticate(self.other)

    def test_empty_comment(self):
        for data in [{}, {'comment': ''}, {'comment': '   '}]:
            response = self.client.post(f'/api/post/{self.post.id}/comment/', data)
            self.assertEqual(response.status_code, 400, data)

        self.post.refresh_from_db()
        self.assertEqual(self.post.comments_count, 0)
        self.assertFalse(self.post.notifications.exists())

    def test_empty_report(self):
        for data in [{}, {'reportText': '   '}]:
            response = self.client.post(f'/api/post/{self.post.id}/report/', data)
            self.assertEqual(response.status_code, 400, data)

        self.assertFalse(self.post.reports.exists())

    def test_delete_other_users_post(self):
        response = self.client.delete(f'/api/post/{self.post.id}/')

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

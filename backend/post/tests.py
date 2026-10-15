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

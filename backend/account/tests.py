from django.test import TestCase
from rest_framework.test import APIClient

from account.models import User
from post.models import Post


class UserEmailPrivacyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret', is_active=True)
        self.other = User.objects.create_user(
            name='Bob', email='bob@example.com', password='secret', is_active=True)
        self.post = Post.objects.create(body='hello', created_by=self.other)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_other_users_email_is_hidden(self):
        search = self.client.post('/api/search/', {'query': 'Bob'}).json()
        profile = self.client.get(f'/api/post/profile/{self.other.id}/').json()['results']
        friends = self.client.get(f'/api/friends/{self.other.id}/').json()

        users = [
            search['users'][0],
            profile['user'],
            profile['posts'][0]['created_by'],
            friends['user'],
        ]
        for user in users:
            self.assertNotIn('email', user)

    def test_own_email_is_returned(self):
        me = self.client.get('/api/me/').json()
        self.assertEqual(me['email'], 'alice@example.com')

        response = self.client.post('/api/editprofile/', {
            'name': 'Alice New', 'email': 'alice@example.com'}, format='multipart').json()
        self.assertEqual(response['updated_user']['email'], 'alice@example.com')
        self.assertEqual(response['updated_user']['name'], 'Alice New')

from django.test import TestCase
from rest_framework.test import APIClient

from account.models import FriendshipRequest, User
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


class FriendshipTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret', is_active=True)
        self.bob = User.objects.create_user(
            name='Bob', email='bob@example.com', password='secret', is_active=True)

    def client_for(self, user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    def send_request(self, sender, receiver):
        return self.client_for(sender).post(f'/api/friends/{receiver.id}/request/')

    def handle(self, user, friend, request_id, status):
        return self.client_for(user).post(
            f'/api/friends/{friend.id}/request/{request_id}/', {'status': status})

    def make_friends(self):
        request_id = self.send_request(self.alice, self.bob).json()['id']
        self.handle(self.bob, self.alice, request_id, 'accepted')
        return request_id

    def assert_friends_count(self, alice_count, bob_count):
        self.alice.refresh_from_db()
        self.bob.refresh_from_db()
        self.assertEqual(self.alice.friends_count, alice_count)
        self.assertEqual(self.bob.friends_count, bob_count)

    def test_accept_request(self):
        self.make_friends()

        self.assertTrue(self.alice.friends.filter(id=self.bob.id).exists())
        self.assert_friends_count(1, 1)

    def test_accept_request_twice(self):
        request_id = self.make_friends()

        response = self.handle(self.bob, self.alice, request_id, 'accepted')

        self.assertEqual(response.status_code, 404)
        self.assert_friends_count(1, 1)

    def test_accept_rejected_request(self):
        request_id = self.send_request(self.alice, self.bob).json()['id']
        self.handle(self.bob, self.alice, request_id, 'rejected')

        response = self.handle(self.bob, self.alice, request_id, 'accepted')

        self.assertEqual(response.status_code, 404)
        self.assert_friends_count(0, 0)

    def test_invalid_status(self):
        request_id = self.send_request(self.alice, self.bob).json()['id']

        response = self.handle(self.bob, self.alice, request_id, 'whatever')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FriendshipRequest.objects.get(id=request_id).status, 'sent')

    def test_sender_cannot_accept_own_request(self):
        request_id = self.send_request(self.alice, self.bob).json()['id']

        response = self.handle(self.alice, self.bob, request_id, 'accepted')

        self.assertEqual(response.status_code, 404)
        self.assert_friends_count(0, 0)

    def test_sender_can_cancel_request(self):
        request_id = self.send_request(self.alice, self.bob).json()['id']

        response = self.handle(self.alice, self.bob, request_id, 'canceled')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendshipRequest.objects.get(id=request_id).status, 'canceled')

    def test_cannot_send_request_to_yourself(self):
        response = self.send_request(self.alice, self.alice)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(FriendshipRequest.objects.exists())

    def test_cannot_send_request_to_friend(self):
        self.make_friends()

        response = self.send_request(self.bob, self.alice)

        self.assertEqual(response.status_code, 400)

    def test_remove_friend(self):
        self.make_friends()

        response = self.client_for(self.alice).delete(f'/api/friends/{self.bob.id}/request/')

        self.assertEqual(response.json()['message'], 'friendship removed')
        self.assertFalse(self.alice.friends.filter(id=self.bob.id).exists())
        self.assert_friends_count(0, 0)

    def test_remove_non_friend(self):
        response = self.client_for(self.alice).delete(f'/api/friends/{self.bob.id}/request/')

        self.assertEqual(response.status_code, 400)
        self.assert_friends_count(0, 0)

    def test_unknown_user(self):
        unknown_id = '00000000-0000-0000-0000-000000000000'
        client = self.client_for(self.alice)

        self.assertEqual(client.post(f'/api/friends/{unknown_id}/request/').status_code, 404)
        self.assertEqual(client.get(f'/api/friends/{unknown_id}/').status_code, 404)


class ActivateEmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret')

    def activate(self, params):
        return self.client.get('/activateemail/', params)

    def test_activate_user(self):
        response = self.activate({'email': self.user.email, 'id': self.user.id})

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_invalid_parameters(self):
        invalid_params = [
            {},
            {'email': self.user.email},
            {'id': self.user.id},
            {'email': 'wrong@example.com', 'id': self.user.id},
            {'email': self.user.email, 'id': 'not-a-uuid'},
        ]
        for params in invalid_params:
            self.assertEqual(self.activate(params).status_code, 400, params)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

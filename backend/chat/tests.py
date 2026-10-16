from django.test import TestCase
from rest_framework.test import APIClient

from account.models import User
from chat.models import ConversationMessage


class MessageTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret', is_active=True)
        self.bob = User.objects.create_user(
            name='Bob', email='bob@example.com', password='secret', is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(self.alice)
        self.client.post(f'/api/chat/{self.bob.id}/')

    def send(self, data):
        return self.client.post(f'/api/chat/{self.bob.id}/messages/', data)

    def test_send_message(self):
        response = self.send({'message': ' hello '})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message']['message'], 'hello')

    def test_send_empty_message(self):
        for data in [{}, {'message': ''}, {'message': '   '}]:
            self.assertEqual(self.send(data).status_code, 400, data)
        self.assertFalse(ConversationMessage.objects.exists())

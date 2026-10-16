from django.test import TestCase
from rest_framework.test import APIClient

from account.models import User
from notification.models import Notification


class ReadNotificationTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret', is_active=True)
        self.bob = User.objects.create_user(
            name='Bob', email='bob@example.com', password='secret', is_active=True)
        self.notification = Notification.objects.create_notification(
            created_for=self.alice, created_by=self.bob,
            type_of_notification=Notification.NEWFRIENDREQUEST)

    def read(self, user, notification_id):
        client = APIClient()
        client.force_authenticate(user)
        return client.get(f'/api/notification/read/{notification_id}/')

    def test_read_own_notification(self):
        self.assertEqual(self.read(self.alice, self.notification.id).status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_read_other_users_notification(self):
        self.assertEqual(self.read(self.bob, self.notification.id).status_code, 404)
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.is_read)

    def test_read_unknown_notification(self):
        unknown_id = '00000000-0000-0000-0000-000000000000'
        self.assertEqual(self.read(self.alice, unknown_id).status_code, 404)

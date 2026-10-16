from django.test import TestCase
from rest_framework.test import APIClient

from account.models import User


class SearchTests(TestCase):
    def test_search_without_query(self):
        user = User.objects.create_user(
            name='Alice', email='alice@example.com', password='secret', is_active=True)
        client = APIClient()
        client.force_authenticate(user)

        for data in [{}, {'query': '   '}]:
            response = client.post('/api/search/', data)
            self.assertEqual(response.status_code, 200, data)
            self.assertEqual(response.json(), {'users': [], 'posts': []})

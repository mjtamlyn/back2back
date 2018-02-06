from django.test import TestCase
from django.urls import reverse


class IndexTest(TestCase):

    def test_basics(self):
        url = reverse('index')
        response = self.client.get(url)

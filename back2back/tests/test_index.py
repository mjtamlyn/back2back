from django.core.urlresolvers import reverse
from django.test import TestCase


class IndexTest(TestCase):

    def test_basics(self):
        url = reverse('index')
        response = self.client.get(url)

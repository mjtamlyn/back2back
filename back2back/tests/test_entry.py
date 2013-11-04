from django.test import TestCase

from back2back.models import Entry
from back2back.structure import GentsRecurve


class TestCreatingEntry(TestCase):
    def test_simple(self):
        category = GentsRecurve()
        category.create_entry('Larry Godfrey')
        self.assertEqual(Entry.objects.count(), 1)
        self.assertIsInstance(Entry.objects.get().get_category(), GentsRecurve)

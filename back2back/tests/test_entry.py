import unittest

from django.test import TestCase

from back2back.models import Entry
from back2back.structure import GentsRecurve


class TestCreatingEntry(TestCase):
    def test_simple(self):
        category = GentsRecurve()
        category.create_entry('Larry Godfrey')
        self.assertEqual(Entry.objects.count(), 1)
        self.assertIsInstance(Entry.objects.get().get_category(), GentsRecurve)

    def test_with_agb_number(self):
        category = GentsRecurve()
        category.create_entry('Marc Tamlyn', '1039623')
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(Entry.objects.get().agb_number, '1039623')

    @unittest.skip
    def test_limit(self):
        category = GentsRecurve()
        for i in range(category.max_entries):
            category.create_entry('Archer %s' % i)


class TestEntryView(TestCase):
    pass

from collections import OrderedDict

from .models import Entry


class BaseCategory(object):
    max_entries = 24

    def __str__(self):
        return self.name

    def get_entries(self):
        return Entry.objects.filter(category=self.slug).order_by('seeding', 'name')

    def create_entry(self, name, agb_number='', seeding=None):
        Entry.objects.create(category=self.slug, name=name, agb_number=agb_number, seeding=seeding)


class GentsRecurve(BaseCategory):
    name = 'Gents Recurve'
    slug = 'gents-recurve'


class LadiesRecurve(BaseCategory):
    name = 'Ladies Recurve'
    slug = 'ladies-recurve'


class GentsCompound(BaseCategory):
    name = 'Gents Compound'
    slug = 'gents-compound'


class LadiesCompound(BaseCategory):
    name = 'Ladies Compound'
    slug = 'ladies-compound'


CATEGORIES = [GentsRecurve(), LadiesRecurve(), GentsCompound(), LadiesCompound()]
CATEGORIES_BY_SLUG = OrderedDict((category.slug, category) for category in CATEGORIES)

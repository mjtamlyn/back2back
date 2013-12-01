from collections import OrderedDict

from .models import Entry


class BaseCategory(object):
    max_entries = 30

    def __str__(self):
        return self.name

    def get_entries(self):
        return Entry.objects.filter(category=self.slug).order_by('seeding', 'name')

    def create_entry(self, name, agb_number='', seeding=None):
        Entry.objects.create(category=self.slug, name=name, agb_number=agb_number, seeding=seeding)

    def get_first_round_groups(self, entries=None):
        num_groups = int(self.max_entries / 6)
        if entries is None:
            entries = self.get_entries()
        return [Group(category=self, number=i, entries=entries) for i in range(num_groups)]


class GentsRecurve(BaseCategory):
    name = 'Gents Recurve'
    slug = 'gents-recurve'


class LadiesRecurve(BaseCategory):
    name = 'Ladies Recurve'
    slug = 'ladies-recurve'
    max_entries = 18


class GentsCompound(BaseCategory):
    name = 'Gents Compound'
    slug = 'gents-compound'


class LadiesCompound(BaseCategory):
    name = 'Ladies Compound'
    slug = 'ladies-compound'
    max_entries = 18



class Group(object):
    def __init__(self, category, number, entries):
        self.category = category
        self.number = number
        self.all_entries = entries

    def __str__(self):
        return 'Group {}'.format(self.label)

    @property
    def label(self):
        return 'ABCDE'[self.number]

    def entries(self):
        return [e for e in self.all_entries if e.first_group_number == self.number]

    def load_entries(self):
        return self.category.get_entries().filter(first_group_number=self.number)

    def add_entry(self, entry):
        entry.first_group_number = self.number
        entry.save()
        self.index_entries()

    def remove_entry(self, entry):
        entry.first_group_number = None
        entry.save()
        self.index_entries()

    def index_entries(self):
        entries = self.load_entries()
        for i, entry in enumerate(entries):
            entry.first_group_index = i
            entry.save()

    def matches(self):
        entries = self.entries()
        arrangement = [
            [[0, 5], [1, 2], [3, 4]],
            [[0, 4], [1, 3], [2, 5]],
            [[0, 3], [1, 5], [2, 4]],
            [[0, 2], [1, 4], [3, 5]],
            [[0, 1], [2, 3], [4, 5]],
        ]
        return [{
            'index': i,
            'matches': [{
                'archer_1': entries[match[0]] if len(entries) > match[0] else 'BYE',
                'archer_2': entries[match[1]] if len(entries) > match[1] else 'BYE',
                'index': j,
            } for j, match in enumerate(row)],
        } for i, row in enumerate(arrangement)]


CATEGORIES = [GentsRecurve(), LadiesRecurve(), GentsCompound(), LadiesCompound()]
CATEGORIES_BY_SLUG = OrderedDict((category.slug, category) for category in CATEGORIES)

from collections import OrderedDict

from .models import Entry, Score


BYE = 'BYE'


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
        scores = Score.objects.filter(entry__in=entries, stage='first-round')
        scores_by_entry = {}
        for score in scores:
            if score.entry not in scores_by_entry:
                scores_by_entry[score.entry] = {}
            scores_by_entry[score.entry][score.time] = score
        arrangement = [
            [[0, 5], [1, 2], [3, 4]],
            [[0, 4], [1, 3], [2, 5]],
            [[0, 3], [1, 5], [2, 4]],
            [[0, 2], [1, 4], [3, 5]],
            [[0, 1], [2, 3], [4, 5]],
        ]
        return [{
            'index': i,
            'matches': [self.get_match(archer_1, archer_2, entries=entries, scores=scores_by_entry, time=i, match_number=j) for j, (archer_1, archer_2) in enumerate(row)],
        } for i, row in enumerate(arrangement)]

    def get_match(self, archer_1, archer_2, entries, scores, time, match_number):
        if len(entries) > archer_1:
            archer_1 = entries[archer_1]
            if archer_1 in scores:
                score_1 = scores[archer_1].get(time)
            else:
                score_1 = ''
        else:
            archer_1 = BYE
            score_1 = ''
        if len(entries) > archer_2:
            archer_2 = entries[archer_2]
            if archer_2 in scores:
                score_2 = scores[archer_2].get(time)
            else:
                score_2 = ''
        else:
            archer_2 = BYE
            score_2 = ''
        return {
            'archer_1': archer_1,
            'archer_2': archer_2,
            'score_1': score_1,
            'score_2': score_2,
            'index': match_number,
            'time': time,
        }

    def get_score(self, entry, opponent, time):
        if entry == BYE:
            return None
        try:
            score = Score.objects.get(entry=entry, time=time, stage='first-round')
        except Score.DoesNotExist:
            score = Score(entry=entry, time=time, stage='first-round')
        score.opponent = None if opponent == BYE else opponent
        return score

    def get_result(self, match, data):
        if match['archer_1'] == 'BYE':
            return {'archer_2': 2}
        if match['archer_2'] == 'BYE':
            return {'archer_1': 2}
        if data['archer_1'] > data['archer_2']:
            return {'archer_1': 2, 'archer_2': 0}
        if data['archer_1'] == data['archer_2']:
            return {'archer_1': 1, 'archer_2': 1}
        if data['archer_1'] < data['archer_2']:
            return {'archer_1': 0, 'archer_2': 2}

    def record_result(self, match, data):
        score_1 = self.get_score(match['archer_1'], match['archer_2'], match['time'])
        score_2 = self.get_score(match['archer_2'], match['archer_1'], match['time'])
        result = self.get_result(match, data)
        if score_1 is not None:
            score_1.score = data['archer_1']
            score_1.points = result['archer_1']
            score_1.save()
        if score_2 is not None:
            score_2.score = data['archer_2']
            score_2.points = result['archer_2']
            score_2.save()

CATEGORIES = [GentsRecurve(), LadiesRecurve(), GentsCompound(), LadiesCompound()]
CATEGORIES_BY_SLUG = OrderedDict((category.slug, category) for category in CATEGORIES)

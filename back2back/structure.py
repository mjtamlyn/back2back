from collections import OrderedDict

from django.db.models import Sum

from .forms import MatchForm
from .models import Entry, Score


BYE = 'BYE'


class BaseCategory(object):
    max_entries = 30
    first_round_high_scores = 2
    second_round_layout = [
        0, 1, 1, 0, 1, # Winners
        1, 0, 0, 1, 0, # Runners up
        1, 0, # High scores
    ]

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
        return [Group(category=self, stage='first-round', number=i, entries=entries) for i in range(num_groups)]

    def get_first_round_qualifiers(self, entries):
        direct_qs = filter(lambda e: (e.first_group_placing is not None and e.first_group_placing <= 2), entries)
        direct_qs = sorted(direct_qs, key=lambda e: (e.first_group_placing, e.first_group_number))
        for q in direct_qs:
            q.qualified = 'Q'
        entries = filter(lambda e: (e.first_group_placing is not None and e.first_group_placing > 2), entries)
        entries = sorted(entries, key=lambda e: e.first_group_score, reverse=True)
        num_q = self.first_round_high_scores
        qualified = []
        counter = 0
        while len(qualified) < num_q and counter < len(entries):
            start_value = entries[counter].first_group_score
            second_counter = counter
            while second_counter < len(entries) and entries[second_counter].first_group_score == start_value:
                second_counter += 1
            new_qs = entries[counter:second_counter]
            counter += len(new_qs)
            qualified += new_qs
            label = 'q' if len(qualified) <= num_q else 'tie ({})'.format(len(new_qs))
            for q in new_qs:
                q.qualified = label
        return direct_qs + qualified

    def get_second_round_groups(self, qualifiers=None, entries=None):
        if qualifiers is not None:
            groups = [
                Group(category=self, stage='second-round', number=0, entries=[]),
                Group(category=self, stage='second-round', number=1, entries=[]),
            ]
            layout = self.second_round_layout
            for i, entry in enumerate(qualifiers):
                if entry.qualified in ['Q', 'q']:
                    group_number = layout[i]
                    entry.second_group_number = group_number
                    groups[group_number].all_entries.append(entry)
            return groups
        if entries is None:
            entries = self.get_entries()
        return [
            Group(category=self, stage='second-round', number=0, entries=entries),
            Group(category=self, stage='second-round', number=1, entries=entries),
        ]

    def set_second_round_groups(self, qualifiers):
        groups = self.get_second_round_groups(qualifiers)
        for i, group in enumerate(groups):
            for j, entry in enumerate(group.entries()):
                entry.second_group_number = i
                entry.second_group_index = j
                entry.save()
                


class GentsRecurve(BaseCategory):
    name = 'Gents Recurve'
    slug = 'gents-recurve'


class LadiesRecurve(BaseCategory):
    name = 'Ladies Recurve'
    slug = 'ladies-recurve'
    max_entries = 18
    first_round_high_scores = 6
    second_round_layout = [
        0, 1, 1, # Winners
        1, 0, 0, # Runners up
        1, 0, 0, 1, 1, 0, # High scores
    ]


class GentsCompound(BaseCategory):
    name = 'Gents Compound'
    slug = 'gents-compound'


class LadiesCompound(BaseCategory):
    name = 'Ladies Compound'
    slug = 'ladies-compound'
    max_entries = 18
    first_round_high_scores = 6
    second_round_layout = [
        0, 1, 1, # Winners
        1, 0, 0, # Runners up
        1, 0, 0, 1, 1, 0, # High scores
    ]


class Group(object):
    def __init__(self, category, stage, number, entries):
        self.category = category
        self.stage = stage
        self.number = number
        self.all_entries = entries

    def __str__(self):
        return 'Group {}'.format(self.label)

    @property
    def label(self):
        if self.stage == 'first-round':
            return 'ABCDE'[self.number]
        return 'FG'[self.number]

    def entries(self):
        if self.stage == 'first-round':
            return [e for e in self.all_entries if e.first_group_number == self.number]
        else:
            return [e for e in self.all_entries if e.second_group_number == self.number]

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
        scores = Score.objects.filter(entry__in=entries, stage=self.stage)
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
        match = {
            'archer_1': archer_1,
            'archer_2': archer_2,
            'score_1': score_1,
            'score_2': score_2,
            'index': match_number,
            'time': time,
        }
        match['form'] = MatchForm(group=self, match=match)
        return match

    def get_score(self, entry, opponent, time):
        if entry == BYE:
            return None
        try:
            score = Score.objects.get(entry=entry, time=time, stage=self.stage)
        except Score.DoesNotExist:
            score = Score(entry=entry, time=time, stage=self.stage)
        score.opponent = None if opponent == BYE else opponent
        return score

    def get_result(self, match, data):
        if data['archer_1'] is None:
            return None
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

    def denorm_group_data(self):
        for entry in self.entries():
            totals = Score.objects.filter(stage=self.stage, entry=entry).aggregate(points=Sum('points'), score=Sum('score'))
            if self.stage == 'first-round':
                entry.first_group_points = totals['points'] or 0
                entry.first_group_score = totals['score'] or 0
            else:
                entry.second_group_points = totals['points'] or 0
                entry.second_group_score = totals['score'] or 0
            entry.save()
        entries = self.leaderboard(scores=True)
        for i, entry in enumerate(entries, 1):
            if self.stage == 'first-round':
                entry.first_group_placing = i
            else:
                entry.second_group_placing = i
            entry.save()

    def record_result(self, match, data):
        score_1 = self.get_score(match['archer_1'], match['archer_2'], match['time'])
        score_2 = self.get_score(match['archer_2'], match['archer_1'], match['time'])
        result = self.get_result(match, data)
        if result is None:
            if score_1 is not None and score_1.pk:
                score_1.delete()
            if score_2 is not None and score_2.pk:
                score_2.delete()
        else:
            if score_1 is not None:
                score_1.score = data['archer_1']
                score_1.points = result['archer_1']
                score_1.save()
            if score_2 is not None:
                score_2.score = data['archer_2']
                score_2.points = result['archer_2']
                score_2.save()
        self.denorm_group_data()

    def leaderboard(self, scores=False):
        """If you don't pass scores=True this will use the denormed placing field."""
        entries = self.entries()
        if self.stage == 'first-round':
            if scores:
                return sorted(entries, key=lambda e: (e.first_group_points, e.first_group_score), reverse=True)
            else:
                return sorted(entries, key=lambda e: (e.first_group_placing or 10))
        else:
            if scores:
                return sorted(entries, key=lambda e: (e.second_group_points, e.second_group_score), reverse=True)
            else:
                return sorted(entries, key=lambda e: (e.second_group_placing or 10))


CATEGORIES = [GentsRecurve(), LadiesRecurve(), GentsCompound(), LadiesCompound()]
CATEGORIES_BY_SLUG = OrderedDict((category.slug, category) for category in CATEGORIES)

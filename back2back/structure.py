from collections import OrderedDict

from django.db.models import Sum

from .forms import MatchForm, FinalMatchForm
from .models import Entry, Score


BYE = 'BYE'


class BaseCategory(object):
    max_entries = 30
    first_round_groups = 5
    second_round_groups = 3
    second_round_layout = [
        0, 2,  # Winner, runner up for each group
        1, 0,
        2, 1,
        2, 0,
        1, 2,
        0, 1, 2, 0, 0, 1, 1, 2,  # High scores
    ]

    def __str__(self):
        return self.name

    def get_entries(self):
        return Entry.objects.filter(category=self.slug).order_by('name')

    def create_entry(self, name, agb_number=''):
        Entry.objects.create(category=self.slug, name=name, agb_number=agb_number)

    def get_first_round_groups(self, entries=None):
        num_groups = self.first_round_groups
        if entries is None:
            entries = self.get_entries()
        return [Group(category=self, stage='first-round', number=i, entries=entries, start_target=i * 3 + self.first_round_target) for i in range(num_groups)]

    def get_top_entries(self, entries, number, key, label):
        entries = sorted(entries, key=key, reverse=True)
        result = []
        start = 0
        while len(result) < number and start < len(entries):
            scan = start
            start_value = key(entries[start])
            while scan < len(entries) and key(entries[scan]) == start_value:
                scan += 1
            to_add = entries[start:scan]
            result += to_add
            start += len(to_add)
            actual_label = label if len(result) <= number else '{} (tie {})'.format(label, len(to_add))
            for e in to_add:
                e.qualified = actual_label
        return result

    def get_first_round_qualifiers(self, entries):
        groups = self.get_first_round_groups(entries=entries)
        direct_qs = []
        for group in groups:
            group_entries = group.leaderboard()
            top_ranked = self.get_top_entries(group_entries, number=2, key=lambda e: (e.first_group_points, e.first_group_score), label='Q')
            direct_qs += top_ranked
        entries = filter(lambda e: not hasattr(e, 'qualified'), entries)
        entries = sorted(entries, key=lambda e: e.first_group_score, reverse=True)
        left_to_qualify = self.second_round_groups * 6 - len(direct_qs)
        other_qs = self.get_top_entries(entries, number=left_to_qualify, key=lambda e: e.first_group_score, label='q')
        return direct_qs + other_qs

    def get_second_round_groups(self, qualifiers=None, entries=None):
        if qualifiers is not None:
            groups = [
                Group(category=self, stage='second-round', number=0, entries=[], start_target=self.second_round_target),
                Group(category=self, stage='second-round', number=1, entries=[], start_target=self.second_round_target + 4),
                Group(category=self, stage='second-round', number=2, entries=[], start_target=self.second_round_target + 8),
            ]
            layout = self.second_round_layout
            for i, entry in enumerate(qualifiers):
                if entry.qualified:
                    try:
                        group_number = layout[i]
                    except IndexError:
                        break
                    entry.second_group_number = group_number
                    groups[group_number].all_entries.append(entry)
            return groups
        if entries is None:
            entries = self.get_entries()
        return [
            Group(category=self, stage='second-round', number=0, entries=entries, start_target=self.second_round_target),
            Group(category=self, stage='second-round', number=1, entries=entries, start_target=self.second_round_target + 4),
            Group(category=self, stage='second-round', number=2, entries=entries, start_target=self.second_round_target + 8),
        ]

    def set_second_round_groups(self, qualifiers):
        groups = self.get_second_round_groups(qualifiers)
        for i, group in enumerate(groups):
            for j, entry in enumerate(group.entries()):
                entry.second_group_number = i
                entry.second_group_index = j
                entry.save()

    def get_second_round_qualifiers(self, entries):
        groups = self.get_second_round_groups(entries=entries)
        direct_qs = []
        for group in groups:
            group_entries = group.leaderboard()
            top_ranked = self.get_top_entries(group_entries, number=2, key=lambda e: (e.second_group_points, e.second_group_score), label='Q')
            direct_qs += top_ranked
        entries = filter(lambda e: not hasattr(e, 'qualified'), entries)
        entries = sorted(entries, key=lambda e: (e.second_group_score, e.second_group_points), reverse=True)
        left_to_qualify = 6 - len(direct_qs)
        other_qs = self.get_top_entries(entries, number=left_to_qualify, key=lambda e: e.second_group_score, label='q')
        all_qs = direct_qs + other_qs
        all_qs = sorted(all_qs, key=lambda e: (-(e.second_group_placing or 0), e.second_group_score, e.second_group_points))
        return all_qs

    def set_finals_seeds(self, qualifiers):
        for i, qualifier in enumerate(qualifiers):
            qualifier.final_round_seed = i + 1
            qualifier.save()

    def finals_matches(self, qualifiers):
        seeded_qualifiers = sorted((q for q in qualifiers if q.final_round_seed), key=lambda e: (
            e.final_round_seed,
        ))
        if not seeded_qualifiers:
            return []
        return [self.get_finals_match(seeded_qualifiers, i) for i in range(5)]

    def get_finals_match(self, qualifiers, number):
        match_names = ['Match 1', 'Match 2', 'Match 3', 'Semi-final', 'Final']
        match = {
            'index': number,
            'name': match_names[number],
        }
        if number == 0:
            match['archer_1'] = qualifiers[0]
        else:
            prev_score_attr = 'final_match_%s_score' % number
            prev_archer = sorted(qualifiers, key=lambda e: getattr(e, prev_score_attr) or 0, reverse=True)[0]
            if getattr(prev_archer, prev_score_attr) is not None:
                match['archer_1'] = prev_archer
            else:
                match['archer_1'] = None
        match['archer_2'] = qualifiers[number + 1]
        score_attr = 'final_match_%s_score' % (number + 1)
        if match['archer_1']:
            match['score_1'] = getattr(match['archer_1'], score_attr)
        else:
            match['score_1'] = None
        match['score_2'] = getattr(match['archer_2'], score_attr)
        if match['archer_1'] is not None:
            match['form'] = FinalMatchForm(category=self, match=match)
        return match

    def record_final_result(self, match, data):
        attr = 'final_match_%s_score' % (match['index'] + 1)
        setattr(match['archer_1'], attr, data['archer_1'])
        setattr(match['archer_2'], attr, data['archer_2'])
        match['archer_1'].save()
        match['archer_2'].save()


class GentsRecurve(BaseCategory):
    name = 'Gents Recurve'
    slug = 'gents-recurve'
    first_round_target = 1
    second_round_target = 19


class LadiesRecurve(BaseCategory):
    name = 'Ladies Recurve'
    slug = 'ladies-recurve'
    first_round_target = 16
    second_round_target = 5


class GentsCompound(BaseCategory):
    name = 'Gents Compound'
    slug = 'gents-compound'
    first_round_target = 1
    second_round_target = 19


class LadiesCompound(BaseCategory):
    name = 'Ladies Compound'
    slug = 'ladies-compound'
    first_round_target = 16
    second_round_target = 5


class Group(object):
    def __init__(self, category, stage, number, entries, start_target):
        self.category = category
        self.stage = stage
        self.number = number
        self.all_entries = entries
        self.start_target = start_target

    def __str__(self):
        return 'Group {}'.format(self.label)

    @property
    def label(self):
        if self.stage == 'first-round':
            return '1' + 'ABCDEFGH'[self.number]
        elif self.stage == 'second-round':
            return '2' + 'ABCD'[self.number]
        elif self.stage == 'third-round':
            return '3' + 'AB'[self.number]
        raise ValueError('Unknown round %s' % self.stage)

    def entries(self):
        if self.stage == 'first-round':
            return [e for e in self.all_entries if e.first_group_number == self.number]
        elif self.stage == 'second-round':
            return [e for e in self.all_entries if e.second_group_number == self.number]
        elif self.stage == 'third-round':
            return [e for e in self.all_entries if e.third_group_number == self.number]
        raise ValueError('Unknown round %s' % self.stage)

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
        if self.stage == 'first-round':
            entries = sorted(entries, key=lambda e: e.first_group_index)
        elif self.stage == 'second-round':
            entries = sorted(entries, key=lambda e: e.second_group_index)
        elif self.stage == 'third-round':
            entries = sorted(entries, key=lambda e: e.third_group_index)
        else:
            raise ValueError('Unknown round %s' % self.stage)
        scores = Score.objects.filter(entry__in=entries, stage=self.stage)
        scores_by_entry = {}
        for score in scores:
            if score.entry not in scores_by_entry:
                scores_by_entry[score.entry] = {}
            scores_by_entry[score.entry][score.time] = score
        arrangement = [
            [[0, 2], [3, 4], [5, 1]],
            [[3, 1], [4, 0], [2, 5]],
            [[5, 4], [1, 2], [0, 3]],
            [[1, 0], [5, 3], [4, 2]],
            [[2, 3], [0, 5], [1, 4]],
        ]
        return [{
            'index': i,
            'matches': [self.get_match(archer_1, archer_2, entries=entries, scores=scores_by_entry, time=i, match_number=j) for j, (archer_1, archer_2) in enumerate(row)],
        } for i, row in enumerate(arrangement)]

    def entries_by_index(self):
        if self.stage == 'first-round':
            return sorted(self.entries(), key=lambda e: e.first_group_index)
        elif self.stage == 'second-round':
            return sorted(self.entries(), key=lambda e: e.second_group_index)
        elif self.stage == 'third-round':
            return sorted(self.entries(), key=lambda e: e.third_group_index)
        raise ValueError('Unknown round %s' % self.stage)

    def entries_with_matches(self):
        """Used for results tables."""
        matches = self.matches()
        entries = self.entries_by_index()
        results = []
        for entry in entries:
            results.append({'entry': entry, 'matches': [None, None, None, None, None, None]})
        for time in matches:
            for match in time['matches']:
                if match['archer_1'] == BYE or match['archer_2'] == BYE:
                    continue
                if self.stage == 'first-round':
                    index_1 = match['archer_1'].first_group_index
                    index_2 = match['archer_2'].first_group_index
                elif self.stage == 'second-round':
                    index_1 = match['archer_1'].second_group_index
                    index_2 = match['archer_2'].second_group_index
                elif self.stage == 'third-round':
                    index_1 = match['archer_1'].third_group_index
                    index_2 = match['archer_2'].third_group_index
                else:
                    raise ValueError('Unknown round %s' % self.stage)
                results[index_1]['matches'][index_2] = '{} - {}'.format(match['score_1'].score, match['score_2'].score)
                results[index_2]['matches'][index_1] = '{} - {}'.format(match['score_2'].score, match['score_1'].score)
        return results

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
            'target': match_number + self.start_target,
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
            elif self.stage == 'second-round':
                entry.second_group_points = totals['points'] or 0
                entry.second_group_score = totals['score'] or 0
            elif self.stage == 'third-round':
                entry.third_group_points = totals['points'] or 0
                entry.third_group_score = totals['score'] or 0
            else:
                raise ValueError('Unknown round %s' % self.stage)
            entry.save()
        entries = self.leaderboard(scores=True)
        for i, entry in enumerate(entries, 1):
            if self.stage == 'first-round':
                entry.first_group_placing = i
            elif self.stage == 'second-round':
                entry.second_group_placing = i
            elif self.stage == 'third-round':
                entry.third_group_placing = i
            else:
                raise ValueError('Unknown round %s' % self.stage)
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
        return result

    def leaderboard(self, scores=False):
        """If you don't pass scores=True this will use the denormed placing field."""
        entries = self.entries()
        if self.stage == 'first-round':
            if scores:
                return sorted(entries, key=lambda e: (e.first_group_points, e.first_group_score), reverse=True)
            else:
                return sorted(entries, key=lambda e: (e.first_group_placing or 10))
        elif self.stage == 'second-round':
            if scores:
                return sorted(entries, key=lambda e: (e.second_group_points, e.second_group_score), reverse=True)
            else:
                return sorted(entries, key=lambda e: (e.second_group_placing or 10))
        elif self.stage == 'third-round':
            if scores:
                return sorted(entries, key=lambda e: (e.third_group_points, e.third_group_score), reverse=True)
            else:
                return sorted(entries, key=lambda e: (e.third_group_placing or 10))
        raise ValueError('Unknown round %s' % self.stage)


CATEGORIES = [GentsRecurve(), LadiesRecurve(), GentsCompound(), LadiesCompound()]
CATEGORIES_BY_SLUG = OrderedDict((category.slug, category) for category in CATEGORIES)

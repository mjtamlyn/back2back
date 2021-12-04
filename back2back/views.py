import json
import subprocess

from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import View, TemplateView, FormView, DeleteView
from django.urls import reverse

from braces.views import StaffuserRequiredMixin, UserPassesTestMixin

from .forms import EntryForm, LoginForm, MatchForm, FinalMatchForm, VerifyForm
from .models import Entry
from .structure import CATEGORIES, CATEGORIES_BY_SLUG


class TexPDFView(TemplateView):
    response_class = HttpResponse
    content_type = 'application/pdf'

    def render_tex(self, tex):
        with open('/tmp/tmp.tex', 'w') as f:
            f.write(tex)
        subprocess.call(['pdflatex', '-output-directory=/tmp/', '/tmp/tmp.tex'])
        with open('/tmp/tmp.pdf', 'rb') as f:
            content = f.read()
        return content

    def render_to_response(self, context, **response_kwargs):
        tex = render_to_string(self.get_template_names(), context)
        content = self.render_tex(tex)
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(content, **response_kwargs)


class PublicIndex(TemplateView):
    template_name = 'public_index.html'


class Login(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('index')
        return reverse('athlete-index')


class Logout(LogoutView):
    def get_next_page(self):
        return reverse('public-index')


class ScorersIndex(StaffuserRequiredMixin, TemplateView):
    template_name = 'index.html'


class EntryList(StaffuserRequiredMixin, TemplateView):
    template_name = 'entry_list.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        return {
            'category': category,
            'entries': category.get_entries(),
        }


class EntryAdd(StaffuserRequiredMixin, FormView):
    form_class = EntryForm
    template_name = 'entry_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.category = kwargs['category'] = CATEGORIES_BY_SLUG[self.kwargs['category']]
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(category=self.kwargs['category'], **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('entry-list', kwargs={'category': self.kwargs['category']})


class EntryEdit(EntryAdd):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Entry.objects.get(pk=self.kwargs['entry'])
        return kwargs


class EntryDelete(StaffuserRequiredMixin, DeleteView):
    template_name = 'entry_delete.html'
    pk_url_kwarg = 'entry'
    model = Entry

    def get_success_url(self):
        return reverse('entry-list', kwargs={'category': self.kwargs['category']})


class FirstRoundSetGroups(StaffuserRequiredMixin, TemplateView):
    template_name = 'first_round_set_groups.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        return {
            'category': category,
            'groups': groups,
            'unprocessed': [e for e in entries if e.first_group_number is None],
        }


class FirstRoundGroupAdd(StaffuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        entry = Entry.objects.get(pk=self.request.POST['entry'])
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_first_round_groups()
        group = groups[int(self.request.POST['group'])]
        group.add_entry(entry)
        return HttpResponseRedirect(reverse('first-round-set-groups', kwargs={'category': self.kwargs['category']}))


class FirstRoundGroupRemove(StaffuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        entry = Entry.objects.get(pk=self.request.POST['entry'])
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_first_round_groups()
        group = groups[entry.first_group_number]
        group.remove_entry(entry)
        return HttpResponseRedirect(reverse('first-round-set-groups', kwargs={'category': self.kwargs['category']}))


class FirstRoundMatches(StaffuserRequiredMixin, TemplateView):
    template_name = 'first_round_matches.html'

    def rearrange_matches(self, groups):
        """Rearrange the matches so they're ordered by time not group."""
        times = [[], [], [], [], []]
        for group in groups:
            for matches in group.matches():
                times[matches['index']].append({'group': group, 'matches': matches['matches']})
        return times

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_first_round_groups()
        matches = self.rearrange_matches(groups)
        return {
            'round': 'First',
            'match_url_name': 'first-round-match-record',
            'verify_url_name': 'first-round-match-verify',
            'category': category,
            'groups': groups,
            'matches': matches,
        }


class FirstRoundMatchRecord(UserPassesTestMixin, FormView):
    template_name = 'first_round_match_record.html'
    form_class = MatchForm
    success_url_name = 'first-round-matches'

    def test_func(self, user):
        self.category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = self.get_groups()
        self.group = groups[int(self.kwargs['group'])]
        self.match = self.group.matches()[int(self.kwargs['time'])]['matches'][int(self.kwargs['match'])]
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        try:
            user.entry
        except Entry.DoesNotExist:
            return False
        if user.entry in [self.match['archer_1'], self.match['archer_2']]:
            return True
        return False

    def get_groups(self):
        return self.category.get_first_round_groups()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'group': self.group,
            'match': self.match,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'category': self.category,
            'group': self.group,
            'match': self.match,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        result = form.save()
        if self.request.is_ajax():
            return HttpResponse(json.dumps(result))
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponseBadRequest(form.errors.as_json())
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse(self.success_url_name, kwargs={'category': self.kwargs['category']}) + '#match-' + self.kwargs['time']


class FirstRoundMatchVerify(FirstRoundMatchRecord):
    form_class = VerifyForm

    def test_func(self, user):
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        return False

    def get_form_kwargs(self):
        self.category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = self.get_groups()
        self.group = groups[int(self.kwargs['group'])]
        self.matches = self.group.matches()[int(self.kwargs['time'])]['matches']
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({
            'group': self.group,
            'matches': self.matches,
        })
        return kwargs


class FirstRoundLeaderboard(StaffuserRequiredMixin, TemplateView):
    template_name = 'first_round_leaderboard.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        category.get_first_round_qualifiers(entries=entries)
        return {
            'round': 'First',
            'category': category,
            'groups': groups,
        }


class FirstRoundLeaderboardExportRecurve(TemplateView):
    template_name = 'leaderboard_export.html'

    def get_context_data(self, **kwargs):
        leaderboards = []
        for category in CATEGORIES[:2]:
            entries = category.get_entries()
            groups = category.get_first_round_groups(entries=entries)
            category.get_first_round_qualifiers(entries=entries)
            leaderboards.append({'category': category, 'groups': groups})
        return {
            'round': 'First',
            'leaderboards': leaderboards,
        }


class FirstRoundLeaderboardExportCompound(FirstRoundLeaderboardExportRecurve):

    def get_context_data(self, **kwargs):
        leaderboards = []
        for category in CATEGORIES[2:]:
            entries = category.get_entries()
            groups = category.get_first_round_groups(entries=entries)
            category.get_first_round_qualifiers(entries=entries)
            leaderboards.append({'category': category, 'groups': groups})
        return {
            'round': 'First',
            'leaderboards': leaderboards,
        }


class FirstRoundScoresheets(StaffuserRequiredMixin, TexPDFView):
    template_name = 'scoresheets.tex'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class FirstRoundJudges(StaffuserRequiredMixin, TexPDFView):
    template_name = 'judges.tex'

    def rearrange_matches(self, groups):
        """Rearrange the matches so they're ordered by time not group."""
        times = [[], [], [], [], []]
        for group in groups:
            for matches in group.matches():
                times[matches['index']].append({'group': group, 'matches': matches['matches']})
        return times

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        return {
            'category': category,
            'matches': self.rearrange_matches(groups),
        }


class PublicFirstRound(TemplateView):
    template_name = 'public_first_round.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        category.get_first_round_qualifiers(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class SecondRoundSetGroups(StaffuserRequiredMixin, TemplateView):
    template_name = 'second_round_set_groups.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_first_round_qualifiers(entries=entries)
        groups = category.get_second_round_groups(qualifiers)
        return {
            'category': category,
            'groups': groups,
        }

    def post(self, request, *args, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_first_round_qualifiers(entries=entries)
        category.set_second_round_groups(qualifiers)
        return HttpResponseRedirect(reverse('index'))


class SecondRoundMatches(FirstRoundMatches):
    template_name = 'first_round_matches.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_second_round_groups()
        matches = self.rearrange_matches(groups)
        return {
            'round': 'Second',
            'match_url_name': 'second-round-match-record',
            'category': category,
            'groups': groups,
            'matches': matches,
        }


class SecondRoundMatchRecord(FirstRoundMatchRecord):
    success_url_name = 'second-round-matches'

    def get_groups(self):
        return self.category.get_second_round_groups()


class SecondRoundLeaderboard(StaffuserRequiredMixin, TemplateView):
    template_name = 'second_round_leaderboard.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_second_round_groups(entries=entries)
        category.get_second_round_qualifiers(entries=entries)
        return {
            'round': 'Second',
            'category': category,
            'groups': groups,
        }


class SecondRoundLeaderboardExportRecurve(FirstRoundLeaderboardExportRecurve):

    def get_context_data(self, **kwargs):
        leaderboards = []
        for category in CATEGORIES[:2]:
            entries = category.get_entries()
            groups = category.get_second_round_groups(entries=entries)
            category.get_second_round_qualifiers(entries=entries)
            leaderboards.append({'category': category, 'groups': groups})
        return {
            'round': 'Second',
            'leaderboards': leaderboards,
        }


class SecondRoundLeaderboardExportCompound(FirstRoundLeaderboardExportRecurve):

    def get_context_data(self, **kwargs):
        leaderboards = []
        for category in CATEGORIES[2:]:
            entries = category.get_entries()
            groups = category.get_second_round_groups(entries=entries)
            category.get_second_round_qualifiers(entries=entries)
            leaderboards.append({'category': category, 'groups': groups})
        return {
            'round': 'Second',
            'leaderboards': leaderboards,
        }


class SecondRoundScoresheets(StaffuserRequiredMixin, TexPDFView):
    template_name = 'scoresheets.tex'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_second_round_groups(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class SecondRoundJudges(StaffuserRequiredMixin, TexPDFView):
    template_name = 'judges.tex'

    def rearrange_matches(self, groups):
        """Rearrange the matches so they're ordered by time not group."""
        times = [[], [], [], [], []]
        for group in groups:
            for matches in group.matches():
                times[matches['index']].append({'group': group, 'matches': matches['matches']})
        return times

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_second_round_groups(entries=entries)
        return {
            'category': category,
            'matches': self.rearrange_matches(groups),
        }


class PublicSecondRound(TemplateView):
    template_name = 'public_second_round.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_second_round_groups(entries=entries)
        category.get_second_round_qualifiers(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class ThirdRoundSetGroups(StaffuserRequiredMixin, TemplateView):
    template_name = 'third_round_set_groups.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_second_round_qualifiers(entries=entries)
        groups = category.get_third_round_groups(qualifiers)
        return {
            'category': category,
            'groups': groups,
        }

    def post(self, request, *args, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_second_round_qualifiers(entries=entries)
        category.set_third_round_groups(qualifiers)
        return HttpResponseRedirect(reverse('index'))


class ThirdRoundMatches(FirstRoundMatches):
    template_name = 'first_round_matches.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_third_round_groups()
        matches = self.rearrange_matches(groups)
        return {
            'round': 'Third',
            'match_url_name': 'third-round-match-record',
            'category': category,
            'groups': groups,
            'matches': matches,
        }


class ThirdRoundMatchRecord(FirstRoundMatchRecord):
    success_url_name = 'third-round-matches'

    def get_groups(self):
        return self.category.get_third_round_groups()


class ThirdRoundLeaderboard(StaffuserRequiredMixin, TemplateView):
    template_name = 'third_round_leaderboard.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_third_round_groups(entries=entries)
        category.get_third_round_qualifiers(entries=entries)
        return {
            'round': 'Third',
            'category': category,
            'groups': groups,
        }


class ThirdRoundLeaderboardExport(FirstRoundLeaderboardExportRecurve):

    def get_context_data(self, **kwargs):
        leaderboards = []
        for category in CATEGORIES:
            entries = category.get_entries()
            groups = category.get_third_round_groups(entries=entries)
            category.get_third_round_qualifiers(entries=entries)
            leaderboards.append({'category': category, 'groups': groups})
        return {
            'round': 'Third',
            'leaderboards': leaderboards,
        }


class ThirdRoundScoresheets(StaffuserRequiredMixin, TexPDFView):
    template_name = 'scoresheets.tex'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_third_round_groups(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class ThirdRoundJudges(StaffuserRequiredMixin, TexPDFView):
    template_name = 'judges.tex'

    def rearrange_matches(self, groups):
        """Rearrange the matches so they're ordered by time not group."""
        times = [[], [], [], [], []]
        for group in groups:
            for matches in group.matches():
                times[matches['index']].append({'group': group, 'matches': matches['matches']})
        return times

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_third_round_groups(entries=entries)
        return {
            'category': category,
            'matches': self.rearrange_matches(groups),
        }


class PublicThirdRound(TemplateView):
    template_name = 'public_third_round.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_third_round_groups(entries=entries)
        category.get_third_round_qualifiers(entries=entries)
        return {
            'category': category,
            'groups': groups,
        }


class FinalsSetSeeds(StaffuserRequiredMixin, TemplateView):
    template_name = 'finals_set_seeds.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_second_round_qualifiers(entries=entries)
        return {
            'category': category,
            'qualifiers': reversed(qualifiers),
        }

    def post(self, request, *args, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_second_round_qualifiers(entries=entries)
        category.set_finals_seeds(qualifiers)
        return HttpResponseRedirect(reverse('index'))


class Finals(StaffuserRequiredMixin, TemplateView):
    template_name = 'finals.html'

    def get_context_data(self, **kwargs):
        rounds = ['Match 1', 'Match 2', 'Match 3', 'Semi-final', 'Final']
        finalists = []
        for category in CATEGORIES:
            entries = category.get_entries()
            qualifiers = category.get_second_round_qualifiers(entries=entries)
            matches = category.finals_matches(qualifiers)
            finalists.append({
                'category': category,
                'matches': matches,
            })
        return {
            'rounds': rounds,
            'finalists': finalists,
        }


class PublicFinals(TemplateView):
    template_name = 'public_finals.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        qualifiers = category.get_second_round_qualifiers(entries=entries)
        matches = category.finals_matches(qualifiers)
        return {
            'category': category,
            'matches': matches,
        }


class FinalsMatchRecord(StaffuserRequiredMixin, FormView):
    template_name = 'finals_match_record.html'
    form_class = FinalMatchForm

    def get_groups(self):
        return self.category.get_first_round_groups()

    def get_form_kwargs(self):
        self.category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = self.category.get_entries()
        qualifiers = self.category.get_second_round_qualifiers(entries=entries)
        matches = self.category.finals_matches(qualifiers)
        self.match = matches[int(self.kwargs['match'])]
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'category': self.category,
            'match': self.match,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'category': self.category,
            'match': self.match,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('finals')


class FinalsScoresheets(StaffuserRequiredMixin, TexPDFView):
    template_name = 'finals_scoresheets.tex'

    def get_context_data(self, **kwargs):
        return {
            'categories': CATEGORIES,
            'rounds': ['Match 1', 'Match 2', 'Match 3', 'Semi-final', 'Final'],
        }


class ResultsPDF(StaffuserRequiredMixin, TexPDFView):
    template_name = 'results.tex'

    def get_context_data(self, **kwargs):
        results = []
        for category in CATEGORIES:
            entries = category.get_entries()
            first_groups = category.get_first_round_groups(entries=entries)
            category.get_first_round_qualifiers(entries=entries)
            # hack - deliberately reload entries here
            entries = category.get_entries()
            second_groups = category.get_second_round_groups(entries=entries)
            qualifiers = category.get_second_round_qualifiers(entries=entries)
            # hack - deliberately reload entries here again
            entries = category.get_entries()
            results.append({
                'category': category,
                'first_groups': first_groups,
                'second_groups': second_groups,
                'finals': category.finals_matches(qualifiers)
            })
        return {'results': results}


class AthleteIndex(UserPassesTestMixin, TemplateView):
    template_name = 'athlete_index.html'

    def test_func(self, user):
        if user.is_anonymous:
            return False
        try:
            user.entry
        except Entry.DoesNotExist:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.request.user.entry
        category = entry.get_category()
        entries = category.get_entries()
        category.get_first_round_qualifiers(entries=entries)
        first_round_group = category.get_first_round_group_for_entry(entry, entries=entries)
        if first_round_group:
            first_round_matches = first_round_group.matches_for_entry(entry)
        else:
            first_round_matches = None

        second_entries = category.get_entries()
        category.get_second_round_qualifiers(entries=second_entries)
        second_round_group = category.get_second_round_group_for_entry(entry, entries=second_entries)
        if second_round_group:
            second_round_matches = second_round_group.matches_for_entry(entry)
        else:
            second_round_matches = None
        context.update(**{
            'entry': entry,
            'category': category,
            'first_round_group': first_round_group,
            'first_round_matches': first_round_matches,
            'second_round_group': second_round_group,
            'second_round_matches': second_round_matches,
        })
        return context

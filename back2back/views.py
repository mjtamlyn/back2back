from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, FormView, DeleteView

from .forms import EntryForm, MatchForm
from .models import Entry
from .structure import CATEGORIES, CATEGORIES_BY_SLUG


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'categories': CATEGORIES}


class EntryList(TemplateView):
    template_name = 'entry_list.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        return {
            'category': category,
            'entries': category.get_entries(),
        }


class EntryAdd(FormView):
    form_class = EntryForm
    template_name = 'entry_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.category = kwargs['category'] = CATEGORIES_BY_SLUG[self.kwargs['category']]
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(category=self.category, **kwargs)

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


class EntryDelete(DeleteView):
    template_name = 'entry_delete.html'
    pk_url_kwarg = 'entry'
    model = Entry

    def get_success_url(self):
        return reverse('entry-list', kwargs={'category': self.kwargs['category']})


class FirstRoundSetGroups(TemplateView):
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


class FirstRoundGroupAdd(View):
    def post(self, request, *args, **kwargs):
        entry = Entry.objects.get(pk=self.request.POST['entry'])
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_first_round_groups()
        group = groups[int(self.request.POST['group'])]
        group.add_entry(entry)
        return HttpResponseRedirect(reverse('first-round-set-groups', kwargs={'category': self.kwargs['category']}))


class FirstRoundGroupRemove(View):
    def post(self, request, *args, **kwargs):
        entry = Entry.objects.get(pk=self.request.POST['entry'])
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = category.get_first_round_groups()
        group = groups[entry.first_group_number]
        group.remove_entry(entry)
        return HttpResponseRedirect(reverse('first-round-set-groups', kwargs={'category': self.kwargs['category']}))


class FirstRoundMatches(TemplateView):
    template_name = 'first_round_matches.html'

    def get_context_data(self, **kwargs):
        category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        entries = category.get_entries()
        groups = category.get_first_round_groups(entries=entries)
        return {
            'category': category,
            'groups': groups,
            'unprocessed': [e for e in entries if e.first_group_number is None],
        }


class FirstRoundMatchRecord(FormView):
    template_name = 'first_round_match_record.html'
    form_class = MatchForm

    def get_form_kwargs(self):
        self.category = CATEGORIES_BY_SLUG[self.kwargs['category']]
        groups = self.category.get_first_round_groups()
        self.group = groups[int(self.kwargs['group'])]
        self.match = self.group.matches()[int(self.kwargs['time'])]['matches'][int(self.kwargs['match'])]
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
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('first-round-matches', kwargs={'category': self.kwargs['category']})

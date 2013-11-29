from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, FormView, DeleteView

from .forms import EntryForm
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
        groups = category.get_first_round_groups()
        return {
            'category': category,
            'groups': groups,
        }

from django.views.generic import TemplateView, ListView

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

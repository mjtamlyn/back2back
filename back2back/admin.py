from django.contrib import admin

from .models import Entry, Score


class EntryAdmin(admin.ModelAdmin):
    list_filter = ('category',)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Score)

from django.db import models


CATEGORY_CHOICES = (
    ('gents-recurve', 'Gents Recurve'),
    ('ladies-recurve', 'Ladies Recurve'),
    ('gents-compound', 'Gents Compound'),
    ('ladies-compound', 'Ladies Compound'),
)


class Entry(models.Model):
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    agb_number = models.CharField(max_length=20, blank=True, default='', verbose_name='AGB number')

    class Meta:
        verbose_name_plural = 'entries'

    def get_category(self):
        from . import structure
        classes = {
            'gents-recurve': structure.GentsRecurve,
            'ladies-recurve': structure.LadiesRecurve,
            'gents-compound': structure.GentsCompound,
            'ladies-compound': structure.LadiesCompound,
        }
        return classes[self.category]()

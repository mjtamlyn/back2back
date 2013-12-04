from django.db import models


CATEGORY_CHOICES = (
    ('gents-recurve', 'Gents Recurve'),
    ('ladies-recurve', 'Ladies Recurve'),
    ('gents-compound', 'Gents Compound'),
    ('ladies-compound', 'Ladies Compound'),
)

STAGE_CHOICES = (
    ('first-round', 'First Round'),
    ('second-round', 'Second Round'),
)


class Entry(models.Model):
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    agb_number = models.CharField(max_length=20, blank=True, default='', verbose_name='AGB number')
    seeding = models.PositiveIntegerField(blank=True, null=True)
    first_group_number = models.PositiveIntegerField(blank=True, null=True)
    first_group_index = models.PositiveIntegerField(blank=True, null=True, help_text='indexed 0-5 to do the match layout')
    first_group_placing = models.PositiveIntegerField(blank=True, null=True)
    first_group_points = models.PositiveIntegerField(default=0)
    first_group_score = models.PositiveIntegerField(default=0)
    second_group_number = models.PositiveIntegerField(blank=True, null=True)
    second_group_index = models.PositiveIntegerField(blank=True, null=True, help_text='indexed 0-5 to do the match layout')
    second_group_placing = models.PositiveIntegerField(blank=True, null=True)
    second_group_points = models.PositiveIntegerField(default=0)
    second_group_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'entries'

    def get_category(self):
        from .structure import CATEGORIES_BY_SLUG
        return CATEGORIES_BY_SLUG[self.category]


class Score(models.Model):
    entry = models.ForeignKey(Entry)
    stage = models.CharField(max_length=255, choices=STAGE_CHOICES)
    time = models.PositiveIntegerField()
    opponent = models.ForeignKey(Entry, blank=True, null=True, related_name='opponent_score_set')
    score = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    def is_win(self):
        return self.points == 2

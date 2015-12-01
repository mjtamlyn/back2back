import csv
from optparse import make_option

from django.core.management import BaseCommand

from back2back.models import Entry


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-i', '--input',
            action='store',
            dest='input_file',
            default=None,
        ),
        make_option(
            '--reset',
            action='store_true',
            dest='reset',
            default=False,
        ),
    )

    def handle(self, *args, **options):
        if options['reset']:
            Entry.objects.all().delete()
        input_file = options['input_file']
        with open(input_file) as f:
            reader = csv.reader(f)
            for row in reader:
                Entry.objects.create(category=row[0], name=row[1], first_group_number=row[2])

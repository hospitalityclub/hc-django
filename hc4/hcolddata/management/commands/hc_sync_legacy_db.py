from django.core.management.base import BaseCommand
from django.conf import settings

from hccore import models as new
from hcolddata import models as old


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '-o', '--overwrite', 
            action = 'store_true',
            dest = 'overwrite', 
            help = 'always overwrite data from old DB for existing entries in the new DB',
        )

        parser.add_argument(
            '--countries',
            action = 'store_true',
            dest = 'sync_countries',
            help = 'synchronize countries',
        )

        parser.add_argument(
            '--regions',
            action = 'store_true',
            dest = 'sync_regions',
            help = 'synchronize regions',
        )

        parser.add_argument(
            '--cities',
            action = 'store_true',
            dest = 'sync_cities',
            help = 'synchronize cities',
        )

    def handle(self, *args, **options):
        if options['sync_countries']:
            self.sync_countries(options['overwrite'])

    def sync_countries(self, overwrite=False):
        self.stdout.write(self.style.MIGRATE_HEADING('Synchronizing Countries'))
        nc = new.Country.objects.all()
        oc = old.Countries.objects.all()
        self.stdout.write(' Countries in the new database: {}'.format(str(nc.count())))
        self.stdout.write(' Countries in the old database: {}'.format(str(oc.count())))
        
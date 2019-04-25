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
            '-c, --countries',
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
        # fc is the found countries list. This list will be the indication of "in sync" countries
        fc = {}
        # nfnc/nfoc are  not found new/old countries lists.
        nfnc = []
        nfoc = []
        # mcm is a manual oc.flag to nc.code2 match
        mcm = {
            'bx': 'BN', 'ck': 'CC', 'ez': 'CZ', 'iv': 'CI', 'fm': 'FM', 're': 'RE', 'rs': 'RU', 'us': 'US',
            'vt': 'VA', 'vm': 'VN', 'cg': 'CD', 'cf': 'CG', 'tt': 'TL', 'pt': 'PS', 'sv': 'SJ', 'pc': 'PN',
            'fs': 'TF', 'fk': 'FK', 
        }

        for o in oc:
            for n in nc:
                if o.name == n.name:
                    # self.stdout.write('  Found {}'.format(o.name))
                    fc.update({n.id: o.id})
                    break
            else:
                if o.flag in mcm:
                    try:
                        n = nc.get(code2=mcm[o.flag])
                    except:
                        self.stderr.write('  {} not found in new DB'.format(o.name))
                    else:
                        fc.update({n.id: o.id})
                else:
                    nfoc.append(o)
        for n in nc:
            if n.id not in fc:
                nfnc.append(n)
        self.stdout.write('  Countries matched: {}'.format(str(len(fc))))
        self.stdout.write('  Countries not matched in new DB: {}'.format(str(len(nfnc))))
        for nfn in nfnc:
            self.stdout.write('    {}, {}: {}'.format(str(nfn.id), str(nfn.code2), str(nfn.name)))
        self.stdout.write('  Countries not matched in old DB: {}'.format(str(len(nfoc))))
        for nfo in nfoc:
            self.stdout.write('    {}, {}: {}'.format(str(nfo.id), str(nfo.flag), str(nfo.name)))


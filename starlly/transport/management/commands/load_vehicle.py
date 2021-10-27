from django.core.management.base import BaseCommand, CommandError
from dateutil.parser import parse
import csv
from transport.models import Vehicle

class Command(BaseCommand):
    help = " load Vehicle data"

    def add_arguments(self, parser):
        parser.add_argument('param', type=str)

    def handle(self, *args, **options):
        try:
            param = options.get('param')
            output = []
            with open(param, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                output = [item for item in reader]
                for i in output:
                    i['licenseStart'] = parse(i['licenseStart'])
                    i['licenseEnd'] = parse(i['licenseEnd'])
                    Vehicle(**i).save()
        except:
            raise CommandError("Something went wrong with loading Vehicle data")
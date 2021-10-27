from django.core.management.base import BaseCommand, CommandError
from dateutil.parser import parse
import csv
from transport.models import Vehicle, PermitTracker

class Command(BaseCommand):
    help = " load PermitTracker data"

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
                    try:
                        i['VehicleNumber'] = Vehicle.objects.get(vehicleNumber=i['VehicleNumber'])
                    except:
                        i['VehicleNumber'] = None
                    i['PermitStart'] = parse(i['PermitStart'])
                    i['PermitValidTill'] = parse(i['PermitValidTill'])
                    PermitTracker(**i).save()
        except:
            raise CommandError("Something went wrong with loading PermitTracker data")
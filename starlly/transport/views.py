from csv import DictWriter
from datetime import datetime, timedelta
from collections import OrderedDict
from django.db.models import Avg, Count, Min, Sum, Q, Prefetch
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status, mixins, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from .serializers import *
from .models import *

# Create your views here.
class VehicleViewset(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    """ Vehicle Viewset for Vehicle CRUD """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]    
    pagination_class = CustomPagination
    search_fields = ['vehicleNumber','licenseStatus', 'vehicleGroup','vehicleType','installationtype']

    def get_queryset(self):
        queryset = super().get_queryset()
        startdate = self.request.GET.get('startdate', '2020-01-01')
        enddate = self.request.GET.get('enddate','2021-12-31')
        vehicleGroup = self.request.GET.get('vehicleGroup', None) # DMG, Stockyard
        vehicleType = self.request.GET.get('vehicleType', None) # Tipper, Tractor, Lorry
        installationtype = self.request.GET.get('installationtype', None) # New Installation, Migration
        if vehicleGroup:
            queryset = queryset.filter(vehicleGroup=vehicleGroup)
        if vehicleType:
            queryset = queryset.filter(vehicleType=vehicleType)
        if installationtype:
            queryset = queryset.filter(vehicleGroup=installationtype)
        queryset = queryset.filter(licenseStart__gte = startdate, licenseEnd__lte=enddate)
        return queryset
    
    @action(detail=False, methods=['get'])
    def permits_taken(self, request, pk=None):
        """ Action for vehicles and their permits """
        queryset = super().get_queryset()
        startdate = request.GET.get('startdate', '2020-01-01')
        enddate = request.GET.get('enddate','2021-12-31')
        queryset = queryset.prefetch_related(
            Prefetch('permit_vehicles', queryset=PermitTracker.objects.filter(PermitStart__gte=startdate,
                PermitValidTill__lte = enddate),
                to_attr='filtered_permit_vehicles'))
        paginator = VehiclePermitPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = VehiclePermitsSerializer(queryset, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class PermitTrackerViewset(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    """ Viewset for Permit Tracker Model """
    queryset = PermitTracker.objects.all()
    serializer_class = PermitTrackerSerializer
    filter_backends = [filters.SearchFilter]    
    search_fields = ['PermitNumber', 'Destination']

    @action(detail=False, methods=['get'])
    def generate_data(self, request, pk=None):
        """ Get the info via csv """
        queryset = super().get_queryset()
        vehicles = Vehicle.objects.all()
        startdate = request.GET.get('startdate', '2020-01-01')
        enddate = request.GET.get('enddate','2022-01-01')
        dates = [startdate, enddate]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        dates_header= list(OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((end - start).days)).keys())
        dates= OrderedDict(((start + timedelta(_)).strftime(r"%m-%Y"), None) for _ in range((end - start).days)).keys()
        dates_header.insert(0,'col_name')

        quantity_transported = [{dates_header[0]: 'Permits where quantitiy >= 10'}]
        vehicles_registered = [{dates_header[0]: 'Vehicles registered'}]
        new_installations = [{dates_header[0]: 'New Installation'}]
        migrations = [{dates_header[0]: 'Migration'}]
        renewals = [{dates_header[0]: 'Renewal with existing hardware'}]

        permit_6 = [{dates_header[0]: 'Permit duration < 6 hours'}]
        permit_6_10 = [{dates_header[0]: 'Permit duration <6-10 hours'}]
        permit_10 = [{dates_header[0]: 'Permit duration >10 hours'}]
        locations = []
        data = []
        for dIndex, date in enumerate(dates):
            month, year = date.split("-")
            #Permits where quantitiy >= 10
            queryset_transported = queryset.filter(PermitStart__month = month, PermitStart__year=year, 
                        PermitValidTill__month = month, PermitValidTill__year=year, 
                        Qty__gte=10)
            quantity_transported[0].update({dates_header[dIndex+1] : queryset_transported.count()})

            #Vehicles registered
            vehicles_reg = vehicles.filter(registrationDate__month = month, registrationDate__year = year)
            vehicles_registered[0].update({dates_header[dIndex+1] : vehicles_reg.count()})

            #installations
            installations = Vehicle.objects.all().annotate(
                new_installations=Count(
                    'installationtype',
                    filter=Q(installationtype="New Installation", registrationDate__month = month, registrationDate__year = year)),
                migration=Count(
                    'installationtype',
                    filter=Q(installationtype="Migration", registrationDate__month = month, registrationDate__year = year)),
                renewal=Count(
                    'installationtype',
                    filter=Q(installationtype="Renewal with existing hardware",registrationDate__month = month, registrationDate__year = year)),
                    ).aggregate(sum_new=Sum('new_installations'),
                    sum_migration=Sum('migration'),
                    sum_renewal=Sum('renewal')
                    )
            new_installations[0].update({dates_header[dIndex+1] : installations.get('sum_new',0)})
            migrations[0].update({dates_header[dIndex+1] : installations.get('sum_migration',0)})
            renewals[0].update({dates_header[dIndex+1] : installations.get('sum_renewal',0)})

            #loading location
            loading_location = result = PermitTracker.objects.values('LoadingLocation').annotate(
                        counts=Count(
                        'LoadingLocation',
                        filter=Q(created__month = month, created__year = year)))

            for loc in loading_location:
                loca = [{dates_header[0]: loc['LoadingLocation']}]
                flag = True
                for la in locations:
                    if la[0]['col_name']==loc['LoadingLocation']:
                        la[0].update({dates_header[dIndex+1]:loc['counts'] })
                        flag=False
                if flag:
                    locations.append(loca)

            #permit duration
            hours_6 =0
            hours_6_10 =0
            hours_10 =0
            query = super().get_queryset()
            permits = query.filter(PermitStart__month = month, PermitStart__year = year,
                    PermitValidTill__month = month, PermitValidTill__year = year)
            for permit in permits:
                diff = permit.PermitValidTill - permit.PermitStart
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600

                if hours<6:
                    hours_6= hours_6+1
                elif hours>6 and hours<10:
                    hours_6_10 = hours_6_10+1
                else:
                    hours_10 = hours_10+1

            permit_6[0].update({dates_header[dIndex+1] : hours_6})
            permit_6_10[0].update({dates_header[dIndex+1] : hours_6_10})
            permit_10[0].update({dates_header[dIndex+1] : hours_10})

        data.append(quantity_transported)
        data.append(vehicles_registered)
        data.append(new_installations)
        data.append(migrations)
        data.append(renewals)
        data.append(locations)
        data.append(permit_6)
        data.append(permit_6_10)
        data.append(permit_10)

        final=[]
        count=0
        for content in data:
            for instance in content:
                if isinstance(instance,list):
                    for element in instance:
                        final.append(element)
                else:
                    final.append(instance)
            count+=1
        with open('data.csv','w') as outfile:
            writer = DictWriter(outfile, tuple(final[0].keys()))
            writer.writeheader()
            writer.writerows(final)
        response = FileResponse(
            open('data.csv', 'rb'), as_attachment=True,
            filename='data.csv')
        return response        


    @action(detail=True, methods=['get'])
    def vehicle(self, request, pk=None):
        """ Retrieving Vehicle for the particular permit """
        queryset = super().get_queryset()
        permit = queryset.get(pk=pk)
        queryset = Vehicle.objects.filter(id=permit.VehicleNumber.id)
        serializer = VehicleSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)


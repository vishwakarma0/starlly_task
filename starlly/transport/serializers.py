from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.db.models import Q, Count, F, Max, Min
from rest_framework import serializers, pagination
from rest_framework.response import Response
from .models import *

class VehicleSerializer(serializers.ModelSerializer):
    """ Serializer for Vehicle Model """
    class Meta:
        model = Vehicle
        fields = (
            'id','vehicleNumber','vehicleStatus','vehicleGroup', 'totalPermits','ownerPhone',
            'licenseStart', 'licenseEnd','licenseStatus','capacity','vehicleType','gpsIMEI',
            'telecomProvider','simNo','registrationDate','installationtype','registrationBy')
       

class PermitTrackerSerializer(serializers.ModelSerializer):
    """ Serializer for Permit Tracker Model """
    class Meta:
        model = PermitTracker
        fields = (
            'id','PermitNumber','ILMS_number','VehicleNumber', 'PermitStart','PermitValidTill',
            'LoadingLocation', 'Destination','Qty','Alerts')


class  CustomPagination(pagination.PageNumberPagination):
    """ Pagination for VehiclePermits """
    page_size = 10
    page_size_query_param = 'page_limit'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class  VehiclePermitPagination(pagination.PageNumberPagination):
    """ Pagination for VehiclePermits """
    page_size = 2
    page_size_query_param = 'page_limit'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class VehiclePermitsSerializer(serializers.ModelSerializer):
    """ Serializer for Vehicle and their permits """
    permit_vehicles = PermitTrackerSerializer(read_only=True, many=True, allow_null=True, source='filtered_permit_vehicles')
    permits_count = serializers.SerializerMethodField(read_only=True)

    def get_permits_count(self, obj):
        request_obj = self.context['request']
        startdate = request_obj.query_params.get('startdate', '2020-01-01')
        enddate = str(request_obj.GET.get('enddate','2022-01-01'))
        status = request_obj.GET.get('status', 'PermitStart') # PermitStart, PermitValidTill
        if startdate and enddate:
            try:
                if status=="PermitStart":
                    obj = obj.permit_vehicles.filter(PermitStart__range = [startdate, enddate])
                else:
                    obj = obj.permit_vehicles.filter(PermitValidTill__range=[startdate, enddate])
            except:
                obj = obj
        try:
            return obj.count()
        except: 
            return 0

    class Meta:
        model = Vehicle
        fields = (
            'id','vehicleNumber','vehicleStatus','vehicleGroup', 'totalPermits','ownerPhone',
            'licenseStart', 'licenseEnd','licenseStatus','capacity','vehicleType','gpsIMEI',
            'telecomProvider','simNo','registrationDate','installationtype','registrationBy',
            'permits_count','permit_vehicles')
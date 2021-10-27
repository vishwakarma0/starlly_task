from django.shortcuts import render
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, permissions, filters
from .serializers import *
from .models import *

# Create your views here.
@api_view(['GET'])
def samp(request):
    return Response({"view":"Sample view!!!"})


class UserViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """ User viewset for CRUD """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]    
    search_fields = ['email', 'first_name', 'last_name']
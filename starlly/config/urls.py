"""starlly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('account/', include('account.urls')),
    path('transport/', include('transport.urls')),
]

###  urls
# account/users/  Users CRUD
# auth/token/login/ - Token based login
# auth/token/logout/ - Logout
# transport/vehicles/ Vehicles CRUD
# transport/permits/  Permit Tracker CRUD
# transport/vehicles/?search=value searh/filter
# transport/vehicles/?vehicleGroup=DMG&vehicleType=Lorry&installationtype=Migration nested filter
# transport/permits/generate_csv  Download CSgenerate_data

##loading data via management
# python manage.py load_vehicle vehicle_file.csvfile
# python manage.py load_permit permits_file.csvfile

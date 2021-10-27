from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import *


# Register your models here.
class ViewAdmin(ImportExportModelAdmin):
    readonly_fields=('id','created','modified')
    pass

admin.site.register(Vehicle,ViewAdmin)
admin.site.register(PermitTracker, ViewAdmin)



from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import RohUnit

@admin.register(RohUnit)
class RohUnitAdmin(ImportExportModelAdmin):
    pass
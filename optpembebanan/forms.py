from django import forms
from django.db import models
import datetime
from setparam.models import ParameterOptPembebanan, UnitBoiler

def get_unit_with_spoptb(*args):
    pblist = ParameterOptPembebanan.objects.all().values('unit')
    return pblist

def get_unit(*args):
    unit = UnitBoiler.objects.all().values_list('id','namapltu').distinct()
    return unit

class PembebananForm(forms.Form):
    roh = forms.IntegerField(max_value=100000)
    harga_bb = forms.FloatField(max_value=100)

class RekomendasiKalorForm(forms.Form):
    unit = forms.ModelChoiceField(queryset= UnitBoiler.objects.filter(id__in=get_unit_with_spoptb()))
    file = forms.FileField(label='Upload dokumen ROH')

class SearchRKForm(forms.Form):
    unit = forms.ModelChoiceField(queryset= UnitBoiler.objects.all())






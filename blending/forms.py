from django import forms
from django.db import models
import datetime
from .models import Notes, BlendOnUnit

from setparam.models import UnitBoiler,ParameterBlending
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class SearchBlendingHistoryByUnitForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())


def get_unit(*args):
    pblist = ParameterBlending.objects.all().values('unit')


    return pblist

class PrepareBlandForm(forms.ModelForm):
    class Meta:
        model = BlendOnUnit
        fields = ['unit','tanggal','waktu',]
        widgets = {
            'tanggal': DateTimePickerInput(format='%d/%m/%Y')
        }

class BlendingForm(forms.Form):
    unit = forms.ModelChoiceField(queryset= UnitBoiler.objects.filter(id__in=get_unit() ))
    rohunit = forms.IntegerField()
    tanggal = forms.DateField()
    waktu = forms.TimeField()
    targetkalor = forms.IntegerField()
    persenbiomassa = forms.FloatField()

class BlendOnUnitFrom(forms.ModelForm):
    class Meta:
        model = BlendOnUnit
        #fields = ['unit','tanggal','waktu','kalori','persenbio','roh',]
        exclude=['biomass', 'coalyard', 'tongkang', 'persenbio', 'persentongkang', 'persencoalyard', 'kalori', 'roh']
        #exclude = ['biomass', 'coalyard', 'tongkang','persentongkang', 'persencoalyard']

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        exclude = ["user"]

    labels = {

        'pesan': 'Isi Pesan',
    }
    widgets = {

        'pesan': forms.TextInput(attrs={'class': 'form-control', }),

    }







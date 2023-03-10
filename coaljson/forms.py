from django import forms
from django.core.exceptions import ValidationError
from  django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Coal, CoalJSON, CoalSpec, CoalStockUnit, CoalForBlend
from setparam.models import UnitBoiler
import  json
import datetime
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))

class SetURLAddressForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())
    coalyardurl = forms.CharField(max_length=100)
    tongkangurl = forms.CharField(max_length=100)
    labels = {
        'unit': 'Nama Unit',
        'coalyardurl': 'URL stok di coalyard',
        'tongkangurl': 'URL stok di tongkang',

    }

class CoalForm(forms.ModelForm):
    class Meta:
        model = Coal
        fields = '__all__'


class CoalDataJSONForm(forms.ModelForm):
    class Meta:
        model = CoalJSON
        fields = '__all__'


class MyJSONField(forms.Textarea):

    def clean(self):
        all_key = ["sumberpasokan","Pemasok", "Kategori", "Kalori", "TM", "TS", "ASH", "IDTReducing", \
                   "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                   "HTmax", "JenisAbu", "SI", "Slagging", "C", "H", "N", "O", "statusalat"]

        data = self.clean_data.data
        jsondata = json.loads(data)
        data_key = []
        for key in jsondata.keys():
            data_key.append(key)
        diff_key = list(set(all_key) - set(data_key))
        if len(diff_key) > 0:
            strdata = ' '.join( [item for item in diff_key])
            raise ValueError(f'data {strdata} tidak tersedia')
        return self.clean_data


class CoalSpecForm(forms.ModelForm):
    class Meta:
        model = CoalSpec
        fields = '__all__'
    #tambah satu lagi yaitu unit
    def clean(self):
        all_key = ["sumberpasokan","Pemasok", "Kategori", "Kalori", "TM", "TS", "ASH", "IDTReducing", \
                   "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                   "HTmax", "JenisAbu", "SI", "Slagging", "C", "H", "N", "O", "statusalat"]
        data = self.cleaned_data ['coalspecdata']
        jsondata = json.loads(data)
        data_key = []
        for key in jsondata.keys():
            data_key.append(key)
        diff_key = list(set(all_key) - set(data_key))
        if len(diff_key) > 0:
            strdata = ' '.join([item for item in diff_key])
            #strdata = ' '.join([item for item in data_key])
            raise forms.ValidationError(f'data {strdata} tidak tersedia')

class CoalStockUnitForm(forms.ModelForm):
    class Meta:
        model = CoalStockUnit
        fields = ['unit','tanggal','coalstock']

    labels = {
        'unit': 'Nama Unit',
        'tanggal': 'Tanggal Stock',
        'coalstock': 'Spesifikasi Batubara',
    }
    widgets = {
        'unit': forms.TextInput(attrs={'class': 'form-control', }),
        'coalstock': forms.TextInput(attrs={'class': 'form-control', }),

    }

class SearchStockByUnitForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())

KATEGORI_STOK=(
        ('T','Tongkang'),
        ('C','Coal Yard'),
)
KATEGORI_BB=(
        ('BB','Batubara'),
        ('BIO','Biomass'),
)

class CoalStockSimpleForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())
    tanggal = forms.DateField()
    sumberpasokan = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Pemasok = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    #kategori_stock = forms.ChoiceField(choices=KATEGORI_STOK)
    #kategori_bhn_baku = forms.ChoiceField(choices=KATEGORI_BB)
    Kalori = forms.IntegerField()
    TM = forms.FloatField()
    TS = forms.FloatField()
    ASH = forms.FloatField()
    labels = {
        'unit': 'Nama Unit',
        'tanggal': 'Tanggal Stock',
        'sumberpasokan': 'Sumber Pasokan',
        'TM': 'Total Moisture',
        'TS': 'Total Sulfure',

    }
    #'kategori_bhn_baku': 'Kategori Bahanbaku',
    #'kategori_stock': 'Kategori Stock',
    widgets = {
        'unit': forms.TextInput(attrs={'class': 'form-control', }),
        'tanggal': forms.TextInput(attrs={'class': 'form-control', }),
        'sumberpasokan': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        'Pemasok': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        'TM': forms.TextInput(attrs={'class': 'form-control', }),
        'TS': forms.TextInput(attrs={'class': 'form-control', }),
    }

class CoalStockManualSettingForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())
    tanggal = forms.SplitDateTimeField()

    labels = {
        'unit': 'Nama Unit',
        'tanggal': 'Tanggal Stock',

    }

class CoalForBlendForm(forms.Form):
    class Meta:
        model = CoalForBlend
        fields = ['unit','tanggal','waktu']

    labels = {
        'unit': 'Nama Unit',
        'tanggal': 'Tanggal Stock',

    }
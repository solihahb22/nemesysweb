from django import forms
from django.core.exceptions import ValidationError
from .models import UnitBoiler, ParameterBlending,ParameterOptPembebanan,HargaPerkiraanBB
import json

class UploadROHFromFileForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())
    file = forms.FileField(label='Upload dokumen ROH')


KATEGORI_PARAM = (
        ('OPTB', 'Optimasi Pembebanan'),
        ('BLEND', 'Optimasi Blending'),
    )

class UploadParamFromFileForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=UnitBoiler.objects.all())
    kategori_param = forms.ChoiceField(choices=KATEGORI_PARAM)
    file = forms.FileField(label='Upload dokumen ')

class HargaPerkiraanBBForm(forms.ModelForm):
    class Meta:
        model = HargaPerkiraanBB
        exclude = ('hargaperkiraan',)
        labels ={
            'bulan': 'Bulan',
            'tahun': 'Tahun',
            'hbaperton' : 'Harga Acuan BB ($ USD) ',
            'kursrupiah': 'Kurs Dolar terhadap Rupiah',
            'Kalori': 'Kalori Rata-Rata',
            'Tm': 'Total Moisture',
            'Ts': 'Total Sulfure',
            'Ash': 'ASH'
        }



class UnitBoilerForm(forms.ModelForm):
    class Meta:
        model = UnitBoiler
        fields = '__all__' #cara yang tidak secure
        labels = {
            'namapltu': 'Nama PLTU',
            'namaunit': 'Nama Unit',
            'url_tongkang': 'Endpoint Data Tongkang',
            'url_coalyard': 'Endpoint Data Coalyard',
        }
        widgets = {

            'namapltu': forms.TextInput(attrs={'class': 'form-control',
                                         }),
            'namaunit': forms.TextInput(attrs={'class': 'form-control',
                                         }),
            'url_tongkang': forms.TextInput(attrs={'class': 'form-control',
                                         }),
            'url_coalyard': forms.TextInput(attrs={'class': 'form-control',
                                         }),

        }

    def clean(self):
        url_tongkang = self.cleaned_data.get('url_tongkang')
        url_coalyard = self.cleaned_data.get('url_coalyard')

        if url_tongkang == url_coalyard:
            self._errors['url_tongkang']= self.error_class(['cek ulang url tongkang dan coalyard'])
            self._errors['url_coalyard'] = self.error_class(['cek ulang url tongkang dan coalyard'])

        return self.cleaned_data

class ParameterOptPembebananForm(forms.ModelForm):
    class Meta:
        model = ParameterOptPembebanan
        fields = '__all__'
        labels = {
            'unit': 'Unit Boiler',
            'daya_max': 'Daya Maksimum',
            'daya_min': 'Daya Minimum',
            'koef_a_opt_beban': 'Koefisien a',
            'koef_b_opt_beban': 'Koefisien b',
            'koef_c_opt_beban':'Koefisien c',
            'koef_d_rek_kalor': 'Koefisien d',
            'koef_e_rek_kalor': 'Koefisien e',
            'koef_f_rek_kalor': 'Koefisien f',
        }
        widgets = {
            'daya_max': forms.TextInput(attrs={'class': 'form-control', }),
            'daya_min': forms.TextInput(attrs={'class': 'form-control',  }),
            'koef_a_opt_beban': forms.TextInput(attrs={'class': 'form-control','placeholder':'koefisien a' }),
            'koef_b_opt_beban': forms.TextInput(attrs={'class': 'form-control','placeholder':'koefisien b' }),
            'koef_c_opt_beban': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'koefisien c'}),
            'koef_d_rek_kalor': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'koefisien d' }),
            'koef_e_rek_kalor': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'koefisien e' }),
            'koef_f_rek_kalor': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'koefisien f' }),

        }



class ParameterBlendingForm(forms.ModelForm):
    class Meta:
        model = ParameterBlending
        fields = '__all__'
        labels ={
            'unit': 'Unit Boiler',
            'AH':'Koefisien Excess Air dan AFR (AH)',
            'VM': 'Koefisien Tilting (VM)',
            'nku_size': 'Jumlah Parameter Nilai Kalor Unit',
            'nk_unit': 'Nilai Kalor Unit',

        }
        widgets = {
            'AH': forms.TextInput(attrs={'class': 'form-control','placeholder':'masukkan koefisien AH',
                                               }),
            'VM': forms.TextInput(attrs={'class': 'form-control','placeholder': 'masukkan koefisien VM',
                                         }),
            'nku_size':forms.TextInput(attrs={'class': 'form-control','placeholder':'masukkan jumlah parameter nilai kalor unit',
                                               }),
            'nk_unit': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'masukkan jumlah parameter nilai kalor unit',
                       }),

            'corner1AA': forms.TextInput(attrs={'class': 'form-control','placeholder':'corner1',
                                               }),
            'corner2AA': forms.TextInput(attrs={'class': 'form-control','placeholder':'corner2',
                                               }),
            'corner3AA': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner3',
                                                }),
            'corner4AA': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner4',
                                                }),
            'corner1AB': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner1',
                                                }),
            'corner2AB': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner2',
                                                }),
            'corner3AB': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner3',
                                                }),
            'corner4AB': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner4',
                                                }),
            'corner1CD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner1',
                                                }),
            'corner2CD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner2',
                                                }),
            'corner3CD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner3',
                                                }),
            'corner4CD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner4',
                                                }),
            'corner1EF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner1',
                                                }),
            'corner2EF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner2',
                                                }),
            'corner3EF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner3',
                                                }),
            'corner4EF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner4',
                                                }),
            'corner1FF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner1',
                                                }),
            'corner2FF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner2',
                                                }),
            'corner3FF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner3',
                                                }),
            'corner4FF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corner4',
                                                }),
        }

        def clean(self):
            cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA',
                          'corner1AB', 'corner2AB', 'corner3AB', 'corner4AB',
                          'corner1CD', 'corner2CD', 'corner3CD', 'corner4CD',
                          'corner1EF', 'corner2EF', 'corner3EF', 'corner4EF',
                          'corner1FF', 'corner2FF', 'corner3FF', 'corner4FF',
                          ]
            clean_data = super().clean()
            nk_unit = clean_data.get('nk_unit')
            str_nku = nk_unit.split(sep=',')
            value = [int(x) for x in str_nku]
            nku_size = clean_data.get('nku_size')

            if nk_unit and nku_size:
                if len(value) != nku_size:
                    raise ValidationError("Jumlah parameter 'kalor unit' tidak sesuai")
            corner_dict = {}
            for key in cornerlist:
                data_corner = clean_data.get(key)
                dict1 = {key:data_corner}
                corner_dict.update(dict1)
            for key, v in corner_dict:
                if nk_unit and corner_dict.get(key):
                    koef_list = clean_data.get(key).split(sep=',')
                    value = [float(x) for x in koef_list]
                    if len(value) != nku_size:
                        ValidationError(f' jumlah komponen input data {key} tidak sesuai dengan jumlah parameter kalor unit')





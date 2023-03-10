from django.db import models
import datetime




class HargaPerkiraanBB(models.Model):
    bulan = models.IntegerField(default= datetime.date.today().month)
    tahun = models.IntegerField(default=datetime.date.today().year)
    hbaperton = models.FloatField(max_length=8)
    kursrupiah = models.FloatField(max_length=8)
    hargaperkiraan = models.FloatField(max_length=20,default=0)
    kalori = models.IntegerField(default=4570)
    tm = models.FloatField(max_length=5, default=30.55)
    ts = models.FloatField(max_length=5,default=0.28)
    ash = models.FloatField(max_length=5, default=5.02)

class UnitBoiler(models.Model):
    namapltu = models.CharField(max_length=100)
    namaunit = models.CharField(max_length=100)
    url_tongkang = models.CharField(max_length=150, null=True)
    url_coalyard = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.namapltu} {self.namaunit}'


class RohUnit(models.Model):
    unit = models.ForeignKey(UnitBoiler, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    roh = models.IntegerField(null=True)
    nphr = models.FloatField(max_length=10,null=True)
    coalflow = models.FloatField(null=True)
    ggonet = models.FloatField(null=True)
    rk = models.IntegerField(null=True)

class ParameterBlending(models.Model):
    unit = models.OneToOneField(
        UnitBoiler,
        on_delete=models.CASCADE,
        primary_key=True
    )
    AH = models.FloatField(default=2.91)
    VM = models.IntegerField(default=30)
    nku_size = models.IntegerField()
    nk_unit = models.CharField(max_length=50)
    corner1AA = models.CharField(max_length=50)
    corner2AA = models.CharField(max_length=50)
    corner3AA = models.CharField(max_length=50)
    corner4AA = models.CharField(max_length=50)
    corner1AB = models.CharField(max_length=50)
    corner2AB = models.CharField(max_length=50)
    corner3AB = models.CharField(max_length=50)
    corner4AB = models.CharField(max_length=50)
    corner1CD = models.CharField(max_length=50)
    corner2CD = models.CharField(max_length=50)
    corner3CD = models.CharField(max_length=50)
    corner4CD = models.CharField(max_length=50)
    corner1EF = models.CharField(max_length=50)
    corner2EF = models.CharField(max_length=50)
    corner3EF = models.CharField(max_length=50)
    corner4EF = models.CharField(max_length=50)
    corner1FF = models.CharField(max_length=50)
    corner2FF = models.CharField(max_length=50)
    corner3FF = models.CharField(max_length=50)
    corner4FF = models.CharField(max_length=50)



class ParameterOptPembebanan(models.Model):
    unit = models.OneToOneField(
        UnitBoiler,
        on_delete=models.CASCADE,
        primary_key=True
    )
    daya_min = models.IntegerField()
    daya_max = models.IntegerField()
    koef_a_opt_beban = models.DecimalField(max_digits=15, decimal_places=2)
    koef_b_opt_beban = models.DecimalField(max_digits=15, decimal_places=2)
    koef_c_opt_beban = models.DecimalField(max_digits=15, decimal_places=2)
    koef_d_rek_kalor = models.DecimalField(max_digits=15,decimal_places=3)
    koef_e_rek_kalor = models.DecimalField(max_digits=15, decimal_places=3)
    koef_f_rek_kalor = models.DecimalField(max_digits=15, decimal_places=3)


def cornerfield_defaultvalue():  # This is a callable
    corner = {"corner1AA":[47.8, 48, 28.9, 19.5, 48.4],"corner2AA":[99.4, 99.4, 99.4, 30, 99.5], \
              "corner3AA":[50.1, 50.3, 30.8, 17.2, 50.2], "corner4AA":[48.2, 49.1, 28.6, 18.3, 48.9], \
              "corner1AB":[15.2, 19.9, 19.6, 14.6, 14.6], "corner2AB":[15.8, 20.8, 20.8, 30, 15.8], \
              "corner3AB":[15.2, 20.1, 20.2, 76.1, 14.9], "corner4AB":[17.5, 20.5, 20.5, 16.1, 15.2], \
              "corner1CD":[14.6, 14.2, 39.5, 20.1, 34.9], "corner2CD":[99.1, 99.1, 99.1, 30, 99.2], \
              "corner3CD":[13.7, 13.4, 39.1, 18.8, 34], "corner4CD":[13.7, 13.9, 39.2, 18.6, 34.3], \
              "corner1EF":[98.5, 98.5, 98.5, 30, 98.6], "corner2EF":[98.2, 98.2, 98.3, 30, 98.4], \
              "corner3EF":[98.4, 98.3, 98.3, 30, 98.2], "corner4EF":[15.9, 17.3, 20.7, 30, 19.2], \
              "corner1FF":[19.7, 19.7, 35.4, 59.5, 19.4], "corner2FF":[19.5, 19.4, 34.7, 0, 20.1], \
              "corner3FF":[17.7, 11.8, 27.2, 59.6, 15.3], "corner4FF":[21.6, 22.1, 36, 60.8, 21.9]}

    return corner # Any serializable Python obj, e.g. `["A", "B"]` or `{"price": 0}`

def dayanet_value():
    return {"min":200,"max":315}


class BoilerSetting(models.Model):
    unit = models.OneToOneField(
        UnitBoiler,
        on_delete= models.CASCADE,
        primary_key= True
    )
    dayanet = models.JSONField(default=dayanet_value())  # min dan max
    AH = models.FloatField(default=2.91)
    VM = models.IntegerField(default=30)
    nilaikalorunit = models.CharField(default='5,4000,4200,4500,4600,4700',max_length=100)
    corner = models.JSONField(default=cornerfield_defaultvalue())

    def __str__(self):
        return f'Setting Boiler {self.unit}'

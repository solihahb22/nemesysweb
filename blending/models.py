from django.db import models
from django.conf import settings
import datetime
from coaljson.models import Coal
from setparam.models import UnitBoiler, ParameterBlending
# Create your models here.
# unit
class BlendingOnUnit(models.Model):
    unit = models.ForeignKey(UnitBoiler, on_delete= models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT,null=True)
    tanggal = models.DateField(auto_now_add=False, blank=True, auto_now=False, default=datetime.date.today())
    settingunit = models.ForeignKey(ParameterBlending,on_delete=models.PROTECT)
    coal1 = models.TextField(max_length=500)
    coal2 = models.TextField(max_length=500)
    biomass = models.TextField(max_length=500, blank=True)
    cofiring = models.TextField(max_length=500,blank=True)

class Notes(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    pesan = models.TextField(max_length=500)

class BlendOnUnit(models.Model):
    unit = models.ForeignKey(UnitBoiler, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    tanggal = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today())
    waktu = models.TimeField()
    biomass = models.ForeignKey(Coal, null=True, blank=True,on_delete= models.PROTECT, related_name='asbiomass')
    coalyard = models.ForeignKey(Coal, null=True, blank=True,on_delete= models.PROTECT, related_name='incoalyard')
    tongkang= models.ForeignKey(Coal, null=True, blank=True, on_delete= models.PROTECT, related_name='intongkang')
    persenbio = models.FloatField(default=0)
    persentongkang = models.FloatField(null=True)
    persencoalyard = models.FloatField(null=True)
    kalori = models.FloatField(null=True)
    roh = models.FloatField(null=True)







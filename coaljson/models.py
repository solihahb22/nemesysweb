from django.db import models
from setparam.models import UnitBoiler
import datetime

class Coal(models.Model):
    """
    {
   "Pemasok": "Bukit Asam",
   "Kalori": 4732,
   "TM": 29.19,
   "TS": 0.36,
   "ASH": 5.76,
   "IDTReducing": 1270,
   "SiO2": 57.96,
   "Al2O3": 26.85,
   "Fe2O3": 5.19,
   "CaO": 3.24,
   "MgO": 1.43,
   "Na2O": 1.2,
   "K2O": 0.59,
   "TiO2": 1.02,
   "SO3": 1.95,
   "HTmax": 1400,
   "JenisAbu": "Bituminous",
   "SI": 2268.8,
   "Slagging": "Low",
   "C": 61.28,
   "H": 4.02,
   "N": 0.92,
   "O": 13.29
 },
    """
    KATEGORI_BB = (
        ('BB', 'Batubara'),
        ('BIO', 'Biomass'),
    )

    pemasok = models.CharField(max_length=100, default='not specified')
    kategori_bhn_baku = models.CharField(max_length=3, choices=KATEGORI_BB, default='BB')
    kategori = models.CharField(max_length=13, default='not specified')
    kalori = models.IntegerField()
    tm = models.FloatField()
    ts = models.FloatField()
    ash = models.FloatField()
    idtreducing = models.IntegerField()
    sio2 = models.FloatField()
    al2o3 = models.FloatField()
    fe2o3 = models.FloatField()
    cao = models.FloatField()
    mgo = models.FloatField()
    na2o = models.FloatField()
    k2o = models.FloatField()
    tio2 = models.FloatField()
    so3 = models.FloatField()
    htmax = models.IntegerField()
    jenisabu = models.CharField(max_length=20, default='not specified')
    si = models.FloatField()
    slagging = models.CharField(max_length=10, default='not specified')
    c = models.FloatField()
    h = models.FloatField()
    n = models.FloatField()
    o = models.FloatField()
    tanggal = models.DateField(null=True) #asumsi jika untuk coalyard adalah data coalyard
#bisa dinormalisasi kalau mau meningkatkan response time

class CoalForBlend(models.Model):
    unit = models.ForeignKey(UnitBoiler, on_delete=models.CASCADE)
    tanggal = models.DateField(null=True)
    waktu = models.TimeField()
    coal = models.ForeignKey(Coal, on_delete = models.CASCADE)

class CoalJSON(models.Model):
    data = models.JSONField(default=None)

class CoalSpec(models.Model):
    coalspecdata = models.TextField()

class CoalStockUnit(models.Model):
    KATEGORI_STOK=(
        ('T','Tongkang'),
        ('C','Coal Yard'),
    )
    KATEGORI_BB=(
        ('BB','Batubara'),
        ('BIO','Biomass'),
    )

    unit = models.ForeignKey(UnitBoiler, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=False,blank=True, auto_now=False,default=datetime.date.today())
    timestamp = models.DateField(auto_now_add=True,auto_now=False)
    kategori_stock = models.CharField(max_length=2,choices=KATEGORI_STOK )
    kategori_bhn_baku= models.CharField(max_length=3, choices=KATEGORI_BB)
    coalstock = models.TextField(max_length=550)

    def __str__(self):
        return f'1 item of coal stock at {self.tanggal}'



from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect,reverse
from .forms import CoalDataJSONForm, CoalForm,CoalSpecForm, CoalStockUnitForm, \
                    CoalStockSimpleForm, SearchStockByUnitForm,SetURLAddressForm, CoalStockManualSettingForm, CoalForBlendForm
from blending.forms import PrepareBlandForm
from .models import CoalJSON,CoalSpec, CoalStockUnit, Coal, CoalForBlend

from .serializers import CoalSpecSerializers
from setparam.models import UnitBoiler, RohUnit
import datetime
import  requests
import json
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core import serializers

#https://studygyaan.com/django/how-to-execute-crud-using-django-ajax-and-json
class CoalForBlendView(FormView):
    template_name = 'coalstock/setbiomass.html'
    form_class = CoalForBlendForm

    def form_valid(self, form):
        coalforblend = CoalForBlend.objects.update_or_create(
            unit = form.cleaned_data["unit"],
            tanggal = form.cleaned_data["tanggal"],
            waktu = form.cleaned_data["waktu"]
        )
    def post(self,request,pk,*args,**kwargs):
        if request.is_ajax():
            coal = Coal.objects.get(pk = pk)
            # edit data coal for blending


class SelectCoalView(View):
    form_class = CoalForBlendForm
    coals = []

    def post(self,request, pk, *args, **kwargs):
        coals =[]
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                unit = form.cleaned_data["unit"]
                tanggal = form.cleaned_data["tanggal"]
                waktu = form.cleaned_data["waktu"]
                #data coal yng dipilih harus dikirim sebagai json untuk disimpan kedalam database
                return JsonResponse({"message":"success", "coals":coals})
        return JsonResponse({"message": "Wrong request"})

    def get(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            coal = Coal.objects.get(pk=pk)
            if coal:
                self.coals.append(coal)
                array_result = serializers.serialize('json', [coal], ensure_ascii=False)
                coal_in_json = array_result[1:-1]
                return JsonResponse({"message": "success", "coals": coal_in_json})
        return JsonResponse({"message": "Wrong request"})


def add_bio_to_db_coal(request):
    item1 = {
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 3300,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0,
        'IDTReducing': 0,
        'SiO2': 0,
        'Al2O3': 0,
        'Fe2O3': 0,
        'CaO': 0,
        'MgO': 0,
        'Na2O': 0,
        'K2O': 0,
        'TiO2': 0,
        'SO3': 0,
        'HTmax': 0,
        'JenisAbu': 0,
        'SI': 0,
        'Slagging': 0,
        'C': 0,
        'H': 0,
        'N': 0,
        'O': 0
    }
    item2 = {
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 2300,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0,
        'IDTReducing': 0,
        'SiO2': 0,
        'Al2O3': 0,
        'Fe2O3': 0,
        'CaO': 0,
        'MgO': 0,
        'Na2O': 0,
        'K2O': 0,
        'TiO2': 0,
        'SO3': 0,
        'HTmax': 0,
        'JenisAbu': 0,
        'SI': 0,
        'Slagging': 0,
        'C': 0,
        'H': 0,
        'N': 0,
        'O': 0
    }
    items = [item1,item2]
    for item in items:
        bio = Coal.objects.create(pemasok=item['Pemasok'],
                              kategori_bhn_baku='BIO',
                              kategori=item['Kategori'],
                              kalori=item['Kalori'],
                              tm=item['TM'],
                              ts=item['TS'],
                              ash=item['ASH'],
                              idtreducing=item['IDTReducing'],
                              sio2=item['SiO2'],
                              al2o3=item['Al2O3'],
                              fe2o3=item['Fe2O3'],
                              cao=item['CaO'],
                              mgo=item['MgO'],
                              na2o=item['Na2O'],
                              k2o=item['K2O'],
                              tio2=item['TiO2'],
                              so3=item['SO3'],
                              htmax=item['HTmax'],
                              jenisabu=item['JenisAbu'],
                              si=item['SI'],
                              slagging=item['Slagging'],
                              c=item['C'],
                              h=item['H'],
                              n=item['N'],
                              o=item['O'])

#data still not display at html file
def get_coal_from_db(request):
    #popuate database coal from api coalspec
    item = {
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 3300,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0,
        'IDTReducing': 0,
        'SiO2': 0,
        'Al2O3': 0,
        'Fe2O3': 0,
        'CaO': 0,
        'MgO': 0,
        'Na2O': 0,
        'K2O': 0,
        'TiO2': 0,
        'SO3': 0,
        'HTmax': 0,
        'JenisAbu': 0,
        'SI': 0,
        'Slagging': 0,
        'C': 0,
        'H': 0,
        'N': 0,
        'O': 0
    }
    context = None
    coal_url = 'http://127.0.0.1:8005/api/coalspecstock/'
    try:
        coalresponse = requests.get(coal_url, timeout=5)
        if coalresponse is not None :
            coalstocks = []
            bio = Coal.objects.create(pemasok=item['Pemasok'],
                                      kategori_bhn_baku='BIO',
                                      kategori=item['Kategori'],
                                      kalori=item['Kalori'],
                                      tm=item['TM'],
                                      ts=item['TS'],
                                      ash=item['ASH'],
                                      idtreducing=item['IDTReducing'],
                                      sio2=item['SiO2'],
                                      al2o3=item['Al2O3'],
                                      fe2o3=item['Fe2O3'],
                                      cao=item['CaO'],
                                      mgo=item['MgO'],
                                      na2o=item['Na2O'],
                                      k2o=item['K2O'],
                                      tio2=item['TiO2'],
                                      so3=item['SO3'],
                                      htmax=item['HTmax'],
                                      jenisabu=item['JenisAbu'],
                                      si=item['SI'],
                                      slagging=item['Slagging'],
                                      c=item['C'],
                                      h=item['H'],
                                      n=item['N'],
                                      o=item['O'])
            coalstocks.append(bio)
            coalsjson = json.loads(coalresponse.text)
            for item in coalsjson:
                c = Coal.objects.create(pemasok=item['Pemasok'],
                                      kategori_bhn_baku='BB',
                                      kategori=item['Kategori'],
                                      kalori=item['Kalori'],
                                      tm=item['TM'],
                                      ts=item['TS'],
                                      ash=item['ASH'],
                                      idtreducing=item['IDTReducing'],
                                      sio2=item['SiO2'],
                                      al2o3=item['Al2O3'],
                                      fe2o3=item['Fe2O3'],
                                      cao=item['CaO'],
                                      mgo=item['MgO'],
                                      na2o=item['Na2O'],
                                      k2o=item['K2O'],
                                      tio2=item['TiO2'],
                                      so3=item['SO3'],
                                      htmax=item['HTmax'],
                                      jenisabu=item['JenisAbu'],
                                      si=item['SI'],
                                      slagging=item['Slagging'],
                                      c=item['C'],
                                      h=item['H'],
                                      n=item['N'],
                                      o=item['O'])

                coalstocks.append(c)

            context = {
                'coalstocks': coalstocks,

            }
            # return HttpResponseRedirect(reverse('coaljson:coal_stock_unit_list', args=(unit.id,)))
            return render(request, 'coaljson/preparecoalstock_view.html', context=context)
    except requests.exceptions.ConnectionError as e:
        pesan = "endpoint tidak tersedia"
        context = {
            'pesan': pesan,
        }
#get_coal_cyd_for_blending
# pilih beberapa dan update cookie dengan ajax
# kalau selesai maka lanjut ke proses penentuan unit dan waktu
def submit_coal_for_blending(request):
    #tampilkan form untuk memilih unit tanggal dan waktu

    pass
def nextstep_setunit(request):
    form = None
    if request.method =="POST":
        # ambil data coal dari session
        form = PrepareBlandForm(None)
        form.instance.created_by = request.user
        #selected_bio
        #selected_tkg
        #selected_cyrd
        selected_cyrds = []
        selected_bios = []
        selected_tkgs = []
        if 'selected_bio' in request.session and 'selected_tkg' in request.session and 'selected_cyrd'in request.session:
            selected_cyrds = Coal.objects.filter(pk__in=request.session['selected_cyrd'])
            bio = Coal.objects.get(pk=int(request.session['selected_bio']))
            tkg = Coal.objects.get(pk=int(request.session['selected_tkg']))
            selected_bios.append(bio)
            selected_tkgs.append(tkg)

        context ={
            'form': form,
            "selected_cyrds": selected_cyrds,
            "selected_bios": selected_bios,
            "selected_tkgs": selected_tkgs,

        }
        return render(request, 'blending/prepare_blending.html',context)
    else:
        return render(request, 'coaljson/confirm_setunit.html')


def select_coal_tk_for_blending(request, coaltk_id):
    coal = []
    selected_coals = []
    selected_bios =[]
    context = None
    pesan = None
    items = list(Coal.objects.filter(kategori_bhn_baku='BB'))
    if len(items) >= 10:
        coals = random.sample(items, 10)
    else:
        coals = items
    if 'selected_bio' :
        bio_id = int(request.session['selected_bio'])
        biomass = Coal.objects.get(pk=bio_id)
        selected_bios.append(biomass)
    else :
        pesan = "biomass tidak berhasil diload"

    request.session['selected_tkg'] = coaltk_id
    coal_tkg = Coal.objects.get(pk=coaltk_id)
    selected_coals.append(coal_tkg)
    pesan = "tidak lewat post"
    context = {
        "pesan": pesan,
        'coals': coals,
        'selected_coals': selected_coals,
        'selected_bios': selected_bios,
    }
    return render(request, 'coaljson/settongkang1.html', context)

def get_coal_tk_for_blending(request):
    coals =[]
    items = list(Coal.objects.filter(kategori_bhn_baku='BB'))
    if len(items) >= 10:
        coals = random.sample(items, 10)
    else:
        coals = items
    selected_coals = []
    if 'selected_bio' in request.session:
        bio = Coal.objects.get(pk = int(request.session['selected_bio']))
        selected_coals.append(bio)
        context = {
            "coals": coals,
            "selected_coals": selected_coals,
        }
        return render(request, 'coaljson/settongkang.html', context)
    else:
        pesan = "Biomass gagal ditentukan"
        return redirect('/coalstock/bio')

def get_coal_cyrd_for_blending(request,cyrd_id=None):
    coals =[]
    pesan = None
    if 'row_coal' in request.session :
        raw_list = request.session['row_coal']
        #raws_id = [val for val in enumerate(raw_list) if val is not None]
        coals = Coal.objects.filter(pk__in =  raw_list[0])

    #items = list(Coal.objects.filter(kategori_bhn_baku='BB'))
    else:
        raw_coals = Coal.objects.filter(kategori_bhn_baku='BB')
        list_id = list(raw_coals.values_list('id', flat=True))
        selected_list_id_coals =[]
        if len(list_id) >= 10:
            selected_list_id_coals = list(random.sample(list_id, 10))
        else:
            selected_list_id_coals = list_id
    #dipertahankan selama penentuan batubara di coalyard
        coals = Coal.objects.filter(pk__in=selected_list_id_coals)
        request.session['row_coal'] = [selected_list_id_coals]

    selected_cyrds = []
    selected_bios = []
    selected_tkgs = []
    if 'selected_bio' in request.session and 'selected_tkg' in request.session:
        bio = Coal.objects.get(pk = int(request.session['selected_bio']))
        tkg = Coal.objects.get(pk=int(request.session['selected_tkg']))
        selected_bios.append(bio)
        selected_tkgs.append(tkg)

    if cyrd_id is not None:
        if 'selected_cyrd'in request.session:
            #request.session['selected_cyrd'].append(cyrd_id)
            #tambahkan cyrds_id ke dalam session
            cyrds_list = request.session['selected_cyrd']
            cyrds_list.append(cyrd_id)
            request.session['selected_cyrd'] = cyrds_list
            pesan = f'{cyrds_list}'
            #cyrds_id = [int(val) for val in enumerate(cyrd_id) if val is not None]
            selected_cyrds = Coal.objects.filter(pk__in= cyrds_list)
        else:
            #buat session
            request.session['selected_cyrd'] = [cyrd_id]
            selected_cyrds.append(Coal.objects.get(pk= cyrd_id))

    context = {
        'pesan': pesan,
        "coals": coals,
        "selected_cyrds": selected_cyrds,
        "selected_bios": selected_bios,
        "selected_tkgs": selected_tkgs,
    }
    return render(request, 'coaljson/setcoalyard.html', context)


def select_bio_for_blending(request,bio_id):
    coal = []
    selected_coals=[]
    context = None
    pesan = None
    items = list(Coal.objects.filter(kategori_bhn_baku = 'BB'))
    if len(items)>=10:
        coals = random.sample(items, 10)
    else:
        coals = items
    if request.method == "POST":
        biomass = Coal.objects.get( pk= bio_id)
        if not biomass:
            items = list(Coal.objects.filter(kategori_bhn_baku='BIO'))
            if len(items) >= 3:
                coals = random.sample(items, 3)
            else:
                coals = items
            pesan = "proses pemilihan biomass gagal"
            context = {
                "pesan": pesan,
                'coals': coals,
            }
            return render(request, 'coaljson/setbiomass.html', context)
        else:
            #simpan id coal ke session
            request.session['selected_bio'] = bio_id
            selected_coals.append(biomass)
            pesan = " pemilihan biomass sukses"
            # update cookies coalyard list
            # kirimkan ke halaman selanjutnya
            context = {
                "pesan": pesan,
                "coals": coals,
                "selected_coals": selected_coals,
            }
            render(request, 'coaljson/settongkang.html', context)
            #return redirect('/coalstock/tkg')
    else:
        request.session['selected_bio'] = bio_id
        biomass = Coal.objects.get(pk=bio_id)
        selected_coals.append(biomass)
        pesan = "tidak lewat post"
        context = {
            "pesan": pesan,
            'coals': coals,
            'selected_coals': selected_coals
        }
        return render(request, 'coaljson/setbiomass1.html', context)


def get_bio_for_blending(request):
    if 'selected_cyrd' in request.session:
        del request.session['selected_cyrd']
    items = list(Coal.objects.filter(kategori_bhn_baku = 'BIO'))
    max_items = len(items)
    coals = None
    selected_coals = None
    if  max_items>=1:
        if max_items >= 3:
            coals = random.sample(items, 3)
        else:
            coals = items

        context = {
            'coals': coals,
            "selected_coals": selected_coals,
        }
    else:
        pesan = "biomass tidak tersedia"
        context = {
            'pesan': pesan,
            'coals': coals,
            'selected_coals': selected_coals,
        }
    return render(request, 'coaljson/setbiomass.html', context)
#data coalstock diparsing diambil komponen sumberpasokan, pemasok, kategori kalori, tm ts ash
#input: text --> json loads --> ambil berdasarkan keyword
def parsing_coalstock(csu: CoalStockUnit):
    data = json.loads(csu.coalstock)
    coal_simple_rep ={
        'id': csu.id,
        'unit': csu.unit,
        'tanggal': csu.tanggal,
        'sumberpasokan':data.get("sumberpasokan"),
        'Pemasok': data.get("Pemasok"),
        'Kategori': data.get("Kategori"),
        'Kalori': data.get("Kalori"),
        'TM': data.get("TM"),
        'TS': data.get("TS"),
        'ASH': data.get("ASH"),

    }
    return coal_simple_rep

def get_coal_for_blending_op(request):
    # coal dari
    data = {
        "sumberpasokan": "coalyard",
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 1938,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0,
        'IDTReducing': 0,
        'SiO2': 0,
        'Al2O3': 0,
        'Fe2O3': 0,
        'CaO': 0,
        'MgO': 0,
        'Na2O': 0,
        'K2O': 0,
        'TiO2': 0,
        'SO3': 0,
        'HTmax': 0,
        'JenisAbu': 0,
        'SI': 0,
        'Slagging': 0,
        'C': 0,
        'H': 0,
        'N': 0,
        'O': 0,
        "statusalat":1
    }
    #bio = Coal(data)
    context =None
    coalstock = None
    form = SearchStockByUnitForm(None)
    if request.method== "POST":
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            #cek ke db apakah sudah tersedia untuk hari ini?
            CoalStockUnit.objects.filter(unit = unit, tanggal = datetime.date.today()).delete()
            try:
                ub = UnitBoiler.objects.get(id=unit.id)
                tanggal = datetime.date.today()
                jsoncoal = json.dumps(data)
                # menyimpan data bimassa
                # ambil data dari api (user klik tombol untuk mengaktifkan)
                curl = unit.url_coalyard
                turl = unit.url_tongkang
                if (turl is not None) and (curl is not None):
                    # get data from api
                    try:
                        # r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
                        coalyardresponse = requests.get(curl, timeout=5)
                        tongkangresponse = requests.get(turl, timeout=5)
                        if (coalyardresponse is not None) & (tongkangresponse is not None):

                            # coals.append(data)
                            coalyards = json.loads(coalyardresponse.text)
                            tongkang = json.loads(tongkangresponse.text)
                            # coals.append(coalyards)
                            # coals.append(tongkang)
                            biomass, created = CoalStockUnit.objects.update_or_create(unit=unit, kategori_stock='C',
                                                                                      tanggal=tanggal,
                                                                                      kategori_bhn_baku='BIO',
                                                                                      coalstock=jsoncoal)
                            coal_t, created = CoalStockUnit.objects.update_or_create(unit=unit, kategori_stock="T",
                                                                                     tanggal=tanggal,
                                                                                     kategori_bhn_baku="BB",
                                                                                     coalstock=json.dumps(tongkang[0]))
                            coals = []
                            coalstocks = []
                            coalstocks.append(biomass)
                            coals.append(parsing_coalstock(biomass))
                            coalstocks.append(coal_t)
                            coals.append(parsing_coalstock(coal_t))
                            for coal in coalyards:
                                kategori_stock = "C"
                                kategori_bhn_baku = "BB"
                                coalstock = json.dumps(coal)
                                stock, created = CoalStockUnit.objects.update_or_create(unit=unit,
                                                                                        kategori_stock=kategori_stock,
                                                                                        tanggal=tanggal,
                                                                                        kategori_bhn_baku=kategori_bhn_baku,
                                                                                        coalstock=coalstock)
                                coalstocks.append(stock)
                                coals.append(parsing_coalstock(stock))
                            pesan = 'sukses'
                            context = {
                                'pesan': pesan,
                                'coalstocks': coalstocks,
                                'coals': coals,

                            }
                            # return HttpResponseRedirect(reverse('coaljson:coal_stock_unit_list', args=(unit.id,)))
                            return render(request, 'coaljson/preparecoalstock_view.html', context=context)

                    except requests.exceptions.ConnectionError as e:
                        pesan = "endpoint tidak tersedia"
                        context = {
                            'pesan': pesan,

                        }
                else:
                    pesan = "mohon info ke admin terkait setting pada menu unit boiler --> daftar unit boiler"
                    context = {
                        'pesan': pesan,

                    }
            except UnitBoiler.DoesNotExist:
                status = 'Unit Boiler Belum diset'
                context = {
                    'form': form,
                    'status': status,
                }

                context={
                    'pesan': 'data sudah tersedia',
                    'coals': coals,
                }
                return render(request, 'coaljson/preparecoalstock_view.html', context=context)

    else:
        context ={
            'form':form,

        }
    return render(request,'coaljson/preparecoalstock_operator.html',context)

def search_stock_unit_short(request):
    tampil = False
    pesan = None
    coals = None
    if request.method == 'POST':
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            # sekarang = datetime.date.today()
            # stocks = CoalStockUnit.objects.filter(unit = unit, tanggal__year = sekarang.year, tanggal__month= sekarang.month, tanggal__day = sekarang.day )
            # stocks = CoalStockUnit.objects.filter(unit=unit, tanggal = sekarang)
            #stocks = CoalStockUnit.objects.filter(unit=unit).order_by('-tanggal')
            csus = CoalStockUnit.objects.filter(unit=unit, tanggal=datetime.date.today()).order_by('-tanggal')
            if not csus:
                pesan = "Data tidak ditemukan"
                tampil = False
            else:
                tampil = True
                coals = []
                for csu in csus:
                    coals.append(parsing_coalstock(csu))
                context = {
                    'form': form,
                    'tampil': tampil,
                     'coals': coals,
                }
                return render(request, 'coaljson/coalstocklist_short.html', context=context)
            #return HttpResponseRedirect(reverse('coaljson:coal_stock_unit_list', args=(unit.id,)))
    else:
        form = SearchStockByUnitForm()
    context = {
        'form': form,
        'tampil': tampil,
        'pesan': pesan,
        'coals': coals,

    }
    return render(request, 'coaljson/coalstocklist_short.html', context=context)

def get_coal_for_blending(request):
    data = {
        "sumberpasokan": "coalyard",
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 1938,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0
    }
    #bio = Coal(data)
    context =None
    coalstock = None
    form = SearchStockByUnitForm(None)
    if request.method== "POST":
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            #get api setting from unit
            try:
                ub = UnitBoiler.objects.get(id=unit.id)
                tanggal = datetime.date.today()
                jsoncoal = json.dumps(data)
                #menyimpan data bimassa
                #ambil data dari api (user klik tombol untuk mengaktifkan)
                curl = unit.url_coalyard
                turl = unit.url_tongkang
                if (turl is not None) and  (curl is not None):
                    #get data from api
                    biomass = CoalStockUnit.objects.update_or_create(unit=unit, kategori_stock='C', tanggal=tanggal,
                                                                 kategori_bhn_baku='BIO', coalstock=jsoncoal)
                    try:
                        #r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
                        coalyardresponse = requests.get(curl,timeout=5)
                        tongkangresponse = requests.get(turl,timeout= 5)
                        if (coalyardresponse is not None) & (tongkangresponse is not None):
                            coalyards = json.loads(coalyardresponse.text)
                            tongkang = json.loads(tongkangresponse.text)
                            coal_t = CoalStockUnit.objects.update_or_create(unit=unit, kategori_stock="T",
                                                                            tanggal=tanggal,
                                                                            kategori_bhn_baku="BB",
                                                                            coalstock=json.dumps(tongkang[0]))
                            coalstocks = []
                            coalstocks.append(biomass)
                            coalstocks.append(coal_t)
                            for coal in coalyards:
                                kategori_stock = "C"
                                kategori_bhn_baku = "BB"
                                coalstock = json.dumps(coal)
                                stock = CoalStockUnit.objects.create(unit=unit, kategori_stock=kategori_stock,
                                                                     tanggal=tanggal,
                                                                     kategori_bhn_baku=kategori_bhn_baku,
                                                                     coalstock=coalstock)
                                coalstocks.append(stock)
                            pesan ='sukses'
                            context = {
                                'pesan': pesan,
                                'coalstocks': coalstocks,

                            }


                    except requests.exceptions.ConnectionError as e:
                        pesan = "endpoint tidak tersedia"
                        context = {
                            'pesan': pesan,


                        }
                else:
                    pesan = "mohon info ke admin terkait setting pada menu unit boiler --> daftar unit boiler"
                    context = {
                        'pesan': pesan,

                    }
            except UnitBoiler.DoesNotExist:
                status = 'Unit Boiler Belum diset'
                context ={
                'form':form,
                'status': status,
                }

    else:
        context ={
            'form':form,

        }
    return render(request,'coaljson/preparecoalstock.html',context)

def coalstockfromapi(request):
    context =None
    form = SetURLAddressForm(None)
    if request.method== "POST":
        form = SetURLAddressForm(request.POST)
        if form.is_valid():
            curl = form.cleaned_data['coalyardurl']
            turl = form.cleaned_data['tongkangurl']
            unit = form.cleaned_data['unit']
            tanggal = datetime.date.today()
            coalyardresponse = requests.get(curl)
            tongkangresponse = requests.get(turl)
            coalyards = json.loads(coalyardresponse.text)
            tongkang = json.loads(tongkangresponse.text)
            coal_t = CoalStockUnit.objects.create(unit=unit,kategori_stock="T",tanggal=tanggal,kategori_bhn_baku="BB",coalstock=json.dumps(tongkang[0]))
            coalstocks=[]
            coalstocks.append(coal_t)
            for coal in coalyards:
                kategori_stock ="C"
                kategori_bhn_baku ="BB"
                coalstock = json.dumps(coal)
                stock = CoalStockUnit.objects.create(unit=unit,kategori_stock=kategori_stock,tanggal=tanggal,
                                                     kategori_bhn_baku=kategori_bhn_baku,coalstock=coalstock)
                coalstocks.append(stock)

            context ={
                'form':form,
                'coalstocks': coalstocks,

            }

    else:
        context ={
            'form':form,
        }
    return render(request,'coaljson/coalstockfromapi.html',context)

def index_old(request):
    context = {
        'heading': 'nemesys eom system',
        'content': 'coal json sebagai home'
    }

    return render(request,'index.html',context)

def index(request):
    form = AuthenticationForm(data=request.POST or None)
    context = {
        'form':form,
    }

    return render(request,'index.html',context)

def coalspecserializer_list(request):
    if request.method == 'GET':
        coalspecs = CoalSpec.objects.all()
        serializer = CoalSpecSerializers(coalspecs, many = True)
        return JsonResponse(serializer.data, safe = False)

def coalspec_list(request):
    coalspecs = CoalSpec.objects.all()

    #create Coal object and append to list
    coals =[]
    for item in coalspecs:
       coal = Coal(item.coalspecdata)
       coals.append(coal)
        #print(coal.jsoninshortformat())

    return render(request,'coaljson/coalstockasli.html',{'coalspecs':coalspecs,'coals':coals})

def new_coal_stock_unit(request):
    if request.method == 'POST':
        form = CoalStockUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            form.save()
            return HttpResponseRedirect(reverse('coaljson:coal_stock_unit',args=(unit.id,)))

    else:
        form = CoalStockUnitForm()
    return render(request,'coaljson/formstock.html',{'form':form})

def search_stock_unit_old(request):
    tampil = False
    pesan = None
    stocks = None
    if request.method == 'POST':
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            #sekarang = datetime.date.today()
            #stocks = CoalStockUnit.objects.filter(unit = unit, tanggal__year = sekarang.year, tanggal__month= sekarang.month, tanggal__day = sekarang.day )
            #stocks = CoalStockUnit.objects.filter(unit=unit, tanggal = sekarang)
            stocks = CoalStockUnit.objects.filter(unit=unit).order_by('-tanggal')
            if not stocks:
                pesan = "Data tidak ditemukan"
                tampil = False
            else:
                tampil = True
                context = {
                    'form': form,
                    'tampil': tampil,
                    'pesan': pesan,
                    'stocks': stocks,

                }

            return render(request,'coaljson/coalstocklist.html',context=context)
    else:
        form = SearchStockByUnitForm()
    context = {
        'form':form,
        'tampil': tampil,
        'pesan':pesan,
        'stocks': stocks,

    }
    return render(request,'coaljson/coalstocklist.html',context=context)

def search_stock_unit(request):
    tampil = False
    pesan = None
    stocks = None
    if request.method == 'POST':
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            #stocks = CoalStockUnit.objects.filter(unit = unit, tanggal__year = sekarang.year, tanggal__month= sekarang.month, tanggal__day = sekarang.day )
            stocks = CoalStockUnit.objects.filter(unit=unit, tanggal = sekarang)
            #stocks = CoalStockUnit.objects.filter(unit=unit).order_by('-tanggal')
            if stocks is None:
                pesan = "Data tidak ditemukan"
                tampil = False
            else:
                tampil = True

            return HttpResponseRedirect(reverse('coaljson:coal_stock_unit_list', args=(unit.id,)))
    else:
        form = SearchStockByUnitForm()
    context = {
        'form':form,
        'tampil': tampil,
        'pesan':pesan,
        'stocks': stocks,

    }
    return render(request,'coaljson/coalstocklist.html',context=context)

def coal_stock_unit_list(request, unit):
    stocks = CoalStockUnit.objects.filter(unit=unit,tanggal = datetime.date.today()).order_by('-tanggal')
    #stocks = CoalStockUnit.objects.filter(unit=unit).order_by('-tanggal')
    pesan=None
    if stocks is None:
        pesan = "Data tidak ditemukan"
        tampil = False
    else:
        tampil = True
    form = SearchStockByUnitForm(request.POST)
    context = {
        'form': form,
        'tampil': tampil,
        'pesan': pesan,
        'stocks': stocks,
    }
    return render(request, 'coaljson/coalstocklist.html', context=context)

def update_stock_simple2(request,id):
    coalstock = get_object_or_404(CoalStockUnit, id=id)
    simple_rep = parsing_coalstock(coalstock)
    form = CoalStockSimpleForm(simple_rep)

    stock = json.loads(coalstock.coalstock)

    context ={}
    if request.method == 'POST':
        form = CoalStockSimpleForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            stock['Kalori'] = form.cleaned_data['Kalori']
            stock['TM'] = form.cleaned_data['TM']
            stock['TS'] = form.cleaned_data['TS']
            stock['ASH'] = form.cleaned_data['ASH']
            coalstock.coalstock = json.dumps(stock)
            coalstock.tanggal = form.cleaned_data['tanggal']
            coalstock.save()
            pesan = 'edit sukses'
            coalstocks = CoalStockUnit.objects.filter(unit=coalstock.unit, tanggal=coalstock.tanggal)
            coals =[]
            for item in coalstocks:
                simple = parsing_coalstock(item)
                coals.append(simple)

            context ={
                'pesan': pesan,
                'coals': coals,
            }
            #redirect('coaljson:coal_stock_unit_list',context)
            #return HttpResponseRedirect(reverse('coaljson:coal_stock_unit', args=(unit.id,)))
            return render(request, 'coaljson/preparecoalstock_view.html', context=context)
    else:
        context = {
            'form': form,
        }

    return render(request, 'coaljson/simpleformstock.html', context)
#fungsi update stock
#data dibaca dari simple rep
#edit
#update database dengan update or create
def update_stock_simple(request,id):
    coalstock = get_object_or_404(CoalStockUnit, id=id)
    simple_rep = parsing_coalstock(coalstock)
    form = CoalStockSimpleForm(simple_rep)
    stock = json.loads(coalstock.coalstock)

    context ={}
    if request.method == 'POST':
        form = CoalStockSimpleForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            stock['Kalori'] = form.cleaned_data['Kalori']
            stock['TM'] = form.cleaned_data['TM']
            stock['TS'] = form.cleaned_data['TS']
            stock['ASH'] = form.cleaned_data['ASH']
            coalstock.tanggal = form.cleaned_data['tanggal']
            coalstock.coalstock = json.dumps(stock)
            coalstock.save()
            pesan = 'edit sukses'
            coalstocks = CoalStockUnit.objects.filter(unit=coalstock.unit, tanggal=coalstock.tanggal)
            coals =[]
            for item in coalstocks:
                simple = parsing_coalstock(item)
                coals.append(simple)

            context ={
                'pesan': pesan,
                'coals': coals,
            }
            #redirect('coaljson:coal_stock_unit_list',context)
            return HttpResponseRedirect(reverse('coaljson:coal_stock_unit', args=(unit.id,)))
    else:
        context = {
            'form': form,
        }

    return render(request, 'coaljson/simpleformstock.html', context)

def update_coal_stock_unit(request, id):
    coalstock = get_object_or_404(CoalStockUnit, id=id)


    if request.method == 'POST':
        form = CoalStockUnitForm(request.POST, instance=coalstock)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            form.save()
            return HttpResponseRedirect(reverse('coaljson:coal_stock_unit', args=(unit.id,)))

    else:
        form = CoalStockUnitForm(instance=coalstock)

    context = {
        'form': form,
    }

    return render(request, 'coaljson/formstock.html', context)


def delete_coal_stock_unit(request, id):
    csu = get_object_or_404(CoalStockUnit, id=id)
    unit = csu.unit
    if request.method == "POST":
        csu.delete()
        return HttpResponseRedirect(reverse('coaljson:coal_stock_unit_list',args =(unit.id,)))
    else:
        context = {
            'object': csu,
            'unit':unit,
        }
    return render(request, 'coaljson/confirm_deletecsu.html', context)

    coal = get_object_or_404(CoalStockUnit, id=id)
    if request.method=="POST":
        unit = coal['unit']
        coal.delete()
        return redirect('coaljson:search_coal_stock_unit')
    context ={
        "coal": coal,
    }
    return render(request,"coaljson/confirm_delcoalstocklist.html",context)



def get_coal_stock_from_api(request):
    # 
    pass

def coalstockunit(request, unit):
    pass
def view_coal_stock_unit(request, unit):
    sekarang = datetime.datetime.now()
    stocks = CoalStockUnit.objects.filter(unit = unit, tanggal__year = sekarang.year, \
                                          tanggal__month= sekarang.month, tanggal__day = sekarang.day )
    form = SearchStockByUnitForm()
    tampil = True
    pesan = None
    context = {
        'form': form,
        'tampil': tampil,
        'pesan': pesan,
        'stocks': stocks,

    }
    return render(request, 'coaljson/coalstocklist.html', context=context)


def generatebiofromtemp(request):
    data = {
        "sumberpasokan": "coalyard",
        "Pemasok": "Arta Daya Coalindo",
        "Kategori": "biomassa",
        "Kalori": 1938,
        "TM": 59.35,
        "TS": 0,
        "ASH": 0
    }
    bio = Coal(data)
    form = SearchStockByUnitForm(None)
    if request.method == 'POST':
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            jsoncoal = json.dumps(data)
            tanggal = datetime.date.today()
            csu = CoalStockUnit.objects.get_or_create(unit=unit, kategori_stock='Coal Yard', tanggal=tanggal,
                                                      kategori_bhn_baku='Biomass', coalstock=jsoncoal)
            context = {
                'csu': csu,
                'unit': unit,

            }

    else:
        context = {
            'form': form,
        }

    return render(request, 'coaljson/coalstocklist.html', context=context)

def new_coal_spec(request):
    if request.method == 'POST':
        form = CoalSpecForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CoalSpecForm()
    return render(request,'coaljson/formspec.html',{'form':form})


def coaljson_stock_list(request):
    coaljsons = CoalJSON.objects.all()

    return render(request,'coaljson/coalstock.html',{'coaljsons':coaljsons})

def new_coal_json(request):
    if request.method == 'POST':
        form = CoalDataJSONForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = CoalDataJSONForm()
    return render(request,'formjson.html',{'form':form})


def new_coal(request):
    if request.method == 'POST':
        form = CoalForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CoalForm()
    return render(request, 'formjson.html',{'form':form})

def coal_view(request):
    if request.method == 'POST':
        form = CoalDataJSONForm(request.POST)
        if form.is_valid():
           # tampilkan data
           data = form['coal']
           print(data)
    else:
        form = CoalDataJSONForm()
    return render(request,'formjson.html',{'form': form})

def generatebiofromtemp(request):
    data =  {
		   "sumberpasokan": "coalyard",
		   "Pemasok": "Arta Daya Coalindo",
		   "Kategori": "biomassa",
		   "Kalori": 1938,
		   "TM": 59.35,
		   "TS": 0,
		   "ASH": 0
    }
    bio = Coal(data)

    form = SearchStockByUnitForm(None)
    if request.method == 'POST':
        form = SearchStockByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            jsoncoal = json.dumps(data)
            tanggal = datetime.date.today()
            csu = CoalStockUnit.objects.get_or_create(unit = unit, kategori_stock='Coal Yard', tanggal=tanggal,
                                                      kategori_bhn_baku = 'Biomass',coalstock = jsoncoal)
            context ={
                'csu': csu,
                'unit': unit,

            }

    else:
        context ={
            'form': form,
        }

    return render(request, 'coaljson/coalstocklist.html', context=context)
from django.shortcuts import render, get_object_or_404
from .forms import PembebananForm, RekomendasiKalorForm, SearchRKForm
from . import optbeban
from  setparam.models import UnitBoiler, ParameterOptPembebanan, HargaPerkiraanBB, RohUnit
from .optbeban import OptimasiBebanUnit
from django.contrib import messages
import csv,io, pytz, datetime
from datetime import date
from . import forms
import decimal

def view_rk_unit(request):
    context = None
    form = SearchRKForm(None)
    if request.method=="POST":
        form = SearchRKForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            time = datetime.date.today()
            bulan = time.month
            tahun = time.year
            hp = HargaPerkiraanBB.objects.filter(bulan=bulan, tahun=tahun).first()
            rohunit = RohUnit.objects.filter(timestamp__year=time.year, timestamp__month=time.month,
                                             timestamp__day=time.day, unit=unit)
            context ={
                'form': form,
                'hp': hp,
                'rohunits': rohunit,
            }
    else:
        context ={
            'form':form,
        }
    return render(request, 'optpembebanan/view_rk.html', context)

def unggah_roh_unit_harian(request):
    form = RekomendasiKalorForm(None)
    pesan = None
    context = None
    judul = "Form Unggah ROH"
    unit = None

    if request.method == "POST":
        form = RekomendasiKalorForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            #get data roh today
            time = datetime.date.today()
            rohunit = RohUnit.objects.filter(timestamp__year=time.year, timestamp__month=time.month,
                                                 timestamp__day=time.day, unit=unit).order_by('timestamp')
            if not rohunit:
                try:
                    csv_file = request.FILES['file']
                    if not csv_file.name.endswith('.csv'):
                        messages.error(request, 'This is no a csv file')
                    dataset = csv_file.read().decode('UTF-8')
                    io_string = io.StringIO(dataset)
                    next(io_string)
                    time2 = None
                    all_roh = []
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                        dt_format = '%Y-%m-%d %H:%M:%S'
                        time = datetime.datetime.strptime(column[0], dt_format)
                        time = time.replace(tzinfo=pytz.UTC)
                        rohgross = int(column[1])
                        _, created = RohUnit.objects.update_or_create(
                            unit=unit,
                            timestamp=time,
                            roh=rohgross,

                        )
                    rohunit = RohUnit.objects.filter(timestamp__year=time.year, timestamp__month=time.month,
                                                     timestamp__day=time.day, unit=unit).order_by('timestamp')
                    pesan = "Unggah ROH berhasil"
                except Exception as e:
                    pesan = "penulisan ROH ke DB gagal"

                context={
                    'judul': judul,
                    'form': form,
                    'rohunits' :rohunit,
                    'pesan': pesan,
                }
                return render(request, 'optpembebanan/calculate_rk.html', context)
            else:
                context = {
                    'judul': judul,
                    'form': form,
                    'pesan': 'data sudah tersedia',
                    'rohunits': rohunit,
                }
    else:
        context={
            'judul': judul,
            'form' : form,
            'unit': unit,
            'pesan':pesan
        }

    return render(request, 'optpembebanan/calculate_rk.html', context)

def calculate_rk_unit_update(request):
    spo = forms.get_unit_with_spoptb()
    pesan = None
    if len(spo)==0:
        pesan = 'Belum ada unit yang diset parameter pembebanannya'
    form = RekomendasiKalorForm(None)
    context = None
    judul = "Form perkiraan Harga Batubara"
    punits = None
    unit = None
    bulan = datetime.date.today().month
    tahun = datetime.date.today().year
    hp = HargaPerkiraanBB.objects.filter(bulan=bulan, tahun=tahun).first()
   # harga_bb = get_object_or_404(HargaPerkiraanBB, bulan = datetime.date.today().month, tahun = datetime.date.today().year)
    #poptb
    if request.method == "POST":
        form = RekomendasiKalorForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            #get data roh today
            time = datetime.date.today()

            rohunit = RohUnit.objects.filter(timestamp__year=time.year, timestamp__month=time.month,
                                                 timestamp__day=time.day, unit=unit).order_by('timestamp')
            if not rohunit:
                poptbs = []
                poptb = get_object_or_404(ParameterOptPembebanan, unit = unit)
                poptbs.append(poptb)
                koefrk = optbeban.get_koef_rekomendasi_kalor(poptbs)
                koefic = optbeban.get_koef_ic(poptbs)
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'This is no a csv file')
                dataset = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(dataset)
                next(io_string)
                time2 = None
                all_roh=[]
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    dt_format = '%Y-%m-%d %H:%M:%S'
                    time = datetime.datetime.strptime(column[0], dt_format)
                    time = time.replace(tzinfo=pytz.UTC)
                    rohgross = int(column[1])
                    #biayapembangkitunit = optbeban.hitung_biaya_pembangkitan(rohgross, koef_ic=koefic)
                    bpu = poptb.koef_a_opt_beban * rohgross * rohgross + poptb.koef_b_opt_beban * rohgross + poptb.koef_c_opt_beban
                    #biayapembangkitunit =optbeban.hitung_bpu( rohgross, koefic)

                   # nphrunits = optbeban.hitungnphrunit(punits, biayapembangkitunit, hp.hargaperkiraan)
                    #nphru = optbeban.hitungnphru(punits,biayapembangkitunit,hp.hargaperkiraan)
                    nphr = bpu *hp.kalori/ (rohgross * 1000 * decimal.Decimal(hp.hargaperkiraan))
                    #rk = optbeban.hitung_rekomendasi_kalor(punits, nphrunits, koefrk)_
                   # rk = optbeban.hitung_rekomendasi_kalor(punits, nphru, koefrk)
                    rk = poptb.koef_d_rek_kalor + poptb.koef_e_rek_kalor*rohgross + poptb.koef_f_rek_kalor*nphr
                    print(f'roh:{rohgross}, rk:{rk}')
                    _, created = RohUnit.objects.update_or_create(
                        unit=unit,
                        timestamp=time,
                        roh=rohgross,
                        biaya_pembangkitan =bpu,
                        nphr = nphr,
                        rk = rk
                    )

                rohunit = RohUnit.objects.filter(timestamp__year = time.year, timestamp__month = time.month,
                                                 timestamp__day = time.day, unit = unit).order_by('timestamp')
                context={
                    'judul': judul,
                    'form': form,
                    'hp': hp,
                    'rohunits' :rohunit,
                }
                return render(request, 'optpembebanan/calculate_rk.html', context)
            else:
                context = {
                    'judul': judul,
                    'form': form,
                    'hp': hp,
                    'pesan': 'data sudah tersedia',
                    'rohunits': rohunit,
                }


    else:
        context={
            'judul': judul,
            'form' : form,
            'hp': hp,
            'unit': unit,
            'pesan':pesan
        }

    return render(request, 'optpembebanan/calculate_rk.html', context)

def calculate_rk_unit(request):
    spo = forms.get_unit_with_spoptb()
    pesan = None
    if len(spo)==0:
        pesan = 'Belum ada unit yang diset parameter pembebanannya'
    form = RekomendasiKalorForm(None)
    context = None
    judul = "Form perkiraan Harga Batubara"
    punits = None
    unit = None
    bulan = datetime.date.today().month
    tahun = datetime.date.today().year
    hp = HargaPerkiraanBB.objects.filter(bulan=bulan, tahun=tahun).first()
   # harga_bb = get_object_or_404(HargaPerkiraanBB, bulan = datetime.date.today().month, tahun = datetime.date.today().year)
    #poptb
    if request.method == "POST":
        form = RekomendasiKalorForm(request.POST, request.FILES)
        if form.is_valid():
            poptbs = []
            unit = form.cleaned_data['unit']
            poptb = get_object_or_404(ParameterOptPembebanan, unit = unit)
            poptbs.append(poptb)
            koefrk = optbeban.get_koef_rekomendasi_kalor(poptbs)
            koefic = optbeban.get_koef_ic(poptbs)
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is no a csv file')
            dataset = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(dataset)
            next(io_string)
            time2 = None
            all_roh=[]
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                dt_format = '%Y-%m-%d %H:%M:%S'
                time = datetime.datetime.strptime(column[0], dt_format)
                time = time.replace(tzinfo=pytz.UTC)
                rohgross = int(column[1])
                #biayapembangkitunit = optbeban.hitung_biaya_pembangkitan(rohgross, koef_ic=koefic)
                bpu = poptb.koef_a_opt_beban * rohgross * rohgross + poptb.koef_b_opt_beban * rohgross + poptb.koef_c_opt_beban
                #biayapembangkitunit =optbeban.hitung_bpu( rohgross, koefic)

               # nphrunits = optbeban.hitungnphrunit(punits, biayapembangkitunit, hp.hargaperkiraan)
                #nphru = optbeban.hitungnphru(punits,biayapembangkitunit,hp.hargaperkiraan)
                nphr = bpu / (rohgross * 1000 * decimal.Decimal(hp.hargaperkiraan))
                #rk = optbeban.hitung_rekomendasi_kalor(punits, nphrunits, koefrk)_
               # rk = optbeban.hitung_rekomendasi_kalor(punits, nphru, koefrk)
                rk = poptb.koef_d_rek_kalor + poptb.koef_e_rek_kalor*rohgross + poptb.koef_f_rek_kalor*nphr
                print(f'roh:{rohgross}, rk:{rk}')
                _, created = RohUnit.objects.update_or_create(
                    unit=unit,
                    timestamp=time,
                    roh=rohgross,
                    biaya_pembangkitan =bpu,
                    nphr = nphr,
                    rk = rk
                )

            rohunit = RohUnit.objects.filter(timestamp__year = time.year, timestamp__month = time.month,
                                             timestamp__day = time.day, unit = unit)
            context={
                'judul': judul,
                'form': form,
                'hp': hp,
                'rohunits' :rohunit,
            }
            return render(request, 'optpembebanan/calculate_rk.html', context)

    else:
        context={
            'judul': judul,
            'form' : form,
            'hp': hp,
            'unit': unit,
            'pesan':pesan
        }

    return render(request, 'optpembebanan/calculate_rk.html', context)


def select_unit_optb(request):
    units = UnitBoiler.objects.all()
    selected_values = None
    poptbs = None
    optb_all = None
    form = PembebananForm()
    if request.method == "POST":
        selected_values = request.POST.getlist('unit')
        form = PembebananForm(request.POST)
        if form.is_valid():
            p_req = form.cleaned_data['roh']
            harga_bb = form.cleaned_data['harga_bb']

            #ambil parameter optimasi pembebanan
            try:
                poptbs = ParameterOptPembebanan.objects.filter(unit__in = selected_values)

                punits = optbeban.optimasi_beban_unit(p_req,poptbs)
                koefic = optbeban.get_koef_ic(poptbs)
                koefrk = optbeban.get_koef_rekomendasi_kalor(poptbs)
                biayapembangkitunit = optbeban.hitung_biaya_pembangkitan(punits,koef_ic=koefic)
                nphrunits = optbeban.hitungnphrunit(punits,biayapembangkitunit,harga_bb)
                beaprod = optbeban.hitungbiayaproduksi(punits,biayapembangkitunit)
                rk  = optbeban.hitung_rekomendasi_kalor(punits,nphrunits,koefrk)
                optb_all=[]
                for i in range(len(rk)):
                    opti = OptimasiBebanUnit(poptbs[i].unit,punits[i],biayapembangkitunit[i],round(nphrunits[i]),beaprod[i],round(rk[i]))
                    optb_all.append(opti)
                """
                spek_poptbs ={
                    'poptbs': poptbs,
                    'optimasi_beban': optimasi_beban,
                    'punits': punits,
                    'biayapembangkitan': biayapembangkitunit,
                    'nphr': nphrunits,
                    'beaprod':beaprod,
                    'rk':rk,
                }
                """


            except ParameterOptPembebanan.DoesNotExist:
                poptbs = None


    context ={
        'form':form,
        'units':units,
        'selected_values':selected_values,
        'param_opt_b': poptbs,
        'optb_all':optb_all,

    }
    return render(request,'optpembebanan/selectunitoptbeban.html',context)





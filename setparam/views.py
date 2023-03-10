from django.shortcuts import render, get_object_or_404,redirect, HttpResponseRedirect,reverse
from django.contrib import messages
from .models import UnitBoiler, ParameterBlending,ParameterOptPembebanan,RohUnit, HargaPerkiraanBB
from .forms import (UnitBoilerForm, ParameterBlendingForm,UploadParamFromFileForm,
                    ParameterOptPembebananForm, UploadROHFromFileForm, HargaPerkiraanBBForm,)
import os
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.core.files.storage import  FileSystemStorage
from . import helper
import decimal
from datetime import date, datetime, timedelta
from django.shortcuts import redirect
import csv,io,datetime, pytz
from django.utils.timezone import get_current_timezone
from django.utils.datastructures import MultiValueDictKeyError
import calendar
from django.db.models import ProtectedError


def roh_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'Attachment;filename = rohunit.csv'
    writer = csv.writer(response)
    writer.writerow(['timestamp','roh'])
    #lines =[]
    today = datetime.datetime.today()
    delta = timedelta(minutes=30)
    #dt_format = '%Y-%m-%d %H:%M:%S'
    start = datetime.datetime(today.year, today.month, today.day)
    for i in range(48):
        time = start + (i+1) * delta
        if i == 47:
            time = time - timedelta(minutes=1)
            #time = time.strftime(dt_format)
        #lines.append(time)
        writer.writerow([time])

    return response

def hitung_hpb(hba,kalori,tm,ash,ts):
    k = kalori/6322
    a = (100-tm)/(100-8)
    b = (ts-0.8)* 4
    u = (ash - 15)* 0.4
    return (hba*k*a)-(b+u)

def createHargaPerkiraanBB(request):
    judul = "Form Perkiraan Harga Batubara"
    bulan = datetime.date.today().month
    tahun = datetime.date.today().year
    pesan = None
    hp = HargaPerkiraanBB.objects.filter(bulan=bulan, tahun=tahun).order_by('id').first();
    if not hp:
        pesan = f'Harga patokan bulan {bulan} belum diset'
    else:
        pesan = f'Harga patokan batubara bulan {bulan} sudah diset'
    form = HargaPerkiraanBBForm(request.POST or None)
    context = None

    template = 'setparam/createHPBB.html'
    if request.method =="POST":
        #form = HargaPerkiraanBBForm(request.POST)
        if form.is_valid():
            bulan = form.cleaned_data['bulan']
            tahun = form.cleaned_data['tahun']
            kurs = form.cleaned_data['kursrupiah']
            hba = form.cleaned_data['hbaperton']
            kalori = form.cleaned_data['kalori']
            tm = form.cleaned_data['tm']
            ts = form.cleaned_data['ts']
            ash = form.cleaned_data['ash']
            harga = hitung_hpb(hba, kalori, tm, ash, ts) * kurs / 1000
            hp = HargaPerkiraanBB.objects.create(bulan=form.cleaned_data['bulan'],
                                                               tahun=form.cleaned_data['tahun'],
                                                               hbaperton=hba, kursrupiah=kurs,
                                                               kalori=kalori, tm=tm, ts=ts, ash=ash,
                                                               hargaperkiraan=harga)
            pesan = f'Harga patokan batubara bulan {bulan} sudah diset'

            context ={
                'judul': judul,
                'form': form,
                'hpb': hp,
                'pesan': pesan
            }


    else:
        context={
            'judul': judul,
            'form' : form,
            'hpb': hp,
            'pesan':pesan
        }
    return render(request, 'setparam/createHPBB.html', context)

def editHargaPerkiraanBB(request,id):
    hp = HargaPerkiraanBB.objects.get(id=id)
    form = HargaPerkiraanBBForm(instance=hp)

    if request.method == 'POST':
        form = HargaPerkiraanBBForm(request.POST, instance=hp)
        if form.is_valid():
            form.save()
            return redirect('setparam:createhpbb')
    judul = 'Update Harga Perkiraan Batubara'
    context = {
        'form': form,
        'judul': judul,
    }
    return render(request, 'setparam/createHPBB.html', context)

def deleteHargaPerkiraanBB(request,id):
    hp = HargaPerkiraanBB.objects.get(id=id)
    if request.method == "POST":
        hp.delete()
        return HttpResponseRedirect(reverse('setparam:createhpbb'))
    else:
        context={
            'object':hp,
        }
    return render(request,'setparam/confirm_deletehpb.html', context)




def set_rohunit_fromfile(request):
    context = None
    template = 'setparam/upload_rohunit.html'
    form = UploadROHFromFileForm(None)
    if request.method == "POST":
        form = UploadROHFromFileForm(request.POST,request.FILES)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a csv file')
            dataset = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(dataset)
            next(io_string)
            time2 = None
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                dt_format = '%Y-%m-%d %H:%M:%S'
                dt_format2 = 'l, %Y-%m-%d'
                tz = get_current_timezone()
                time = datetime.datetime.strptime(column[0],dt_format)
                time = time.replace(tzinfo= pytz.UTC)
                time2 = time.date()


                #print(f'time:{time}')

                #dt = tz.localize(datetime.datetime.strptime(column[0],dt_format))

                #tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
                #print("datetime.now() :", tz_string)
                _, created = RohUnit.objects.update_or_create(
                        unit=unit,
                        timestamp=time,
                        roh=column[1]
                    )
            rohunit = RohUnit.objects.filter()
            times = time2.strftime('%m/%d/%Y')
            context = {
                'unit': unit,
                'time':times,
                'rohunits': rohunit,
            }
            template = 'setparam/rohunit.html'
            return render(request, template, context)
    else:
        context ={
            'form': form,
        }
    return render(request, template, context)



def download(request):
    #url('/static/images/power.png');
    fs = FileSystemStorage('/media/')
    response = FileResponse(fs.open('settingpembebanan.txt', 'rb'),content_type='text')
    response['Content-Disposition']= 'attachment; filename="settingpembebanan.txt"'
    return response


def set_param_fromfile(request):
    context = None
    data = None
    form = UploadParamFromFileForm(None)
    if request.method == "POST":
        form = UploadParamFromFileForm(request.POST,request.FILES)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            kategori = form.cleaned_data['kategori_param']
            uploadedfile = request.FILES['file']
            #str =[]
            if (kategori=='OPTB'):
                param_value=[]
                for line in uploadedfile:
                    text = line.decode()
                    textsplit = text.split(":")
                    param_value.append(textsplit[1])
                paramoptb= ParameterOptPembebanan.objects.get_or_create(unit = unit, daya_min = int(param_value[0]),
                                                                 daya_max = int(param_value[1]), koef_a_opt_beban = decimal.Decimal(param_value[2]),
                                                                 koef_b_opt_beban = decimal.Decimal(param_value[3]),
                                                                 koef_c_opt_beban = decimal.Decimal(param_value[4]),
                                                                 koef_d_rek_kalor = decimal.Decimal(param_value[5]),
                                                                 koef_e_rek_kalor = decimal.Decimal(param_value[6]),
                                                                 koef_f_rek_kalor = decimal.Decimal(param_value[7]))
                return redirect('setparam:detailpoptbunit',unit=unit.id)
            elif kategori=='BLEND':
                param_value=[]
                for line in uploadedfile:
                     text = line.decode()
                     textsplit = text.split(":")
                     param_value.append(textsplit[1])
                if (len(param_value) == 24):
                    param_blend = ParameterBlending.objects.get_or_create(unit=unit,AH = float(param_value[0]),
                                                                      VM = int(param_value[1]),
                                                                      nku_size = param_value[2],
                                                                      nk_unit = param_value[3],
                                                                      corner1AA = param_value[4],corner2AA = param_value[5],corner3AA = param_value[6],corner4AA = param_value[7],
                                                                      corner1AB=param_value[8],corner2AB = param_value[9],corner3AB = param_value[10],corner4AB = param_value[11],
                                                                      corner1CD=param_value[12],corner2CD = param_value[13],corner3CD = param_value[14],corner4CD = param_value[15],
                                                                      corner1EF=param_value[16],corner2EF = param_value[17],corner3EF = param_value[18],corner4EF = param_value[19],
                                                                      corner1FF=param_value[20], corner2FF=param_value[21],corner3FF=param_value[22], corner4FF=param_value[23])
                    return redirect('setparam:detailpbunit',unit=unit.id)


    else:
        context ={
            'form': form,
        }
    return render(request, 'setparam/setparamfromfile.html', context)

def delete_parameterblending(request,unit):
    pbu = get_object_or_404(ParameterBlending,unit=unit)
    if request.method == "POST":
        pbu.delete()
        return HttpResponseRedirect(reverse('setparam:parameterblendinglist'))
    else:
        context={
            'object':pbu,
        }
    return render(request,'setparam/confirm_deleteub.html', context)


def parameterblending_update(request,unit):
    paramblending = get_object_or_404(ParameterBlending,unit=unit)
    form = ParameterBlendingForm(instance=paramblending)
    if request.method =='POST':
        form = ParameterBlendingForm(request.POST,instance=paramblending)
        if form.is_valid():
            form.save()
            return redirect('setparam:detailpbunit', unit = unit)
    judul = 'Update Setting Unit Boiler Untuk Optimasi Blending'
    context = {
        'form':form,
        'judul':judul,
    }
    return render(request,'setparam/spoptblending.html',context)

def parameterblending_view(request, unit):
    parameterblending = get_object_or_404(ParameterBlending, unit=unit)
    context = {
        'parameterblending': parameterblending,
    }

    return render(request, 'setparam/parameterblendingview.html', context)

def parameterblendinglist(request):
    parameterblendings = ParameterBlending.objects.all()
    context = {
        'parameterblendings': parameterblendings,
    }
    return render(request, 'setparam/pblist.html', context)

def create_prm_opt_blending (request):
    form = ParameterBlendingForm()
    judul = 'Create Setting Unit Boiler Untuk Optimasi Blending'
    if request.method == 'POST':
        form = ParameterBlendingForm(request.POST)
        if form.is_valid():
            form.save()
            dt_unit = form.cleaned_data['unit']
            redirect('setparam:detailpbunit',unit=dt_unit )
    context ={
        'form': form,
        'judul':judul
    }
    return render(request,'setparam/spoptblending.html',context)

def parameteroptbebanlist(request):
    paramoptbebans = ParameterOptPembebanan.objects.all()
    unit_id =[]
    for item in paramoptbebans:
        unit_id.append(item.unit.id)
    context = {
        'unit_id': unit_id,
        'paramoptbebans': paramoptbebans,
    }
    return render(request, 'setparam/poptbeban.html', context)

def create_prm_opt_beban (request):
    form = ParameterOptPembebananForm()
    judul = 'Create Setting Unit Boiler Untuk Optimasi Pembebanan'
    if request.method == 'POST':
        form = ParameterOptPembebananForm(request.POST)
        if form.is_valid():
            form.save()
            dt_unit = form.cleaned_data['unit']
            return redirect('setparam:prmoptbebanlist')

    context ={
        'form': form,
        'judul':judul
    }
    return render(request,'setparam/spoptbeban.html',context)

def prm_opt_beban_view(request, unit):
    paramoptb = get_object_or_404(ParameterOptPembebanan, unit=unit)
    context = {
        'paramoptb': paramoptb,
    }

    return render(request, 'setparam/paramoptbview.html', context)

def update_paramoptb(request,unit):
    paramoptb = get_object_or_404(ParameterOptPembebanan, unit=unit)
    form = ParameterOptPembebananForm(instance=paramoptb)
    if request.method == 'POST':
        form = ParameterOptPembebananForm(request.POST, instance=paramoptb)
        if form.is_valid():
            form.save()
            return redirect('setparam:prmoptbebanlist')
    judul = 'Update Setting Unit Boiler Untuk Optimasi Pembebanan'
    context = {
        'form': form,
        'judul': judul,
    }
    return render(request, 'setparam/spoptbeban.html', context)

def delete_parameteroptb(request, unit):
    optb = get_object_or_404(ParameterOptPembebanan, unit=unit)
    if request.method == "POST":
        optb.delete()
        return HttpResponseRedirect(reverse('setparam:prmoptbebanlist'))
    else:
        context = {
            'object': optb,
            }
        return render(request, 'setparam/confirm_deleteoptb.html', context)




def create_ub(request):
    context ={}
    judul = 'Tambahkan Identitas Unit Boiler'
    units = UnitBoiler.objects.all()
    form = UnitBoilerForm(request.POST or None)
    edited = True
    error = False
    pesan = None
    if request.method =="POST":
        if form.is_valid():
            namapltu = form.cleaned_data["namapltu"]
            namaunit = form.cleaned_data["namaunit"]
            unit = UnitBoiler.objects.filter(namapltu=namapltu, namaunit=namaunit)
            if not unit:
                form.save()
            else:
                error = True
                pesan= 'unit sudah diset di database'

        else:
            form = form
    context = {
        'error': error,
        'pesan': pesan,
        'form':form,
        'units':units,
        'judul': judul,
        'edited': edited,
    }
    return render(request,'setparam/unitform.html',context)

def list_ub(request):
    units = UnitBoiler.objects.all()
    context = {
        'units': units,
    }
    return render(request, 'setparam/listub.html', context)

def delete_unitboiler(request, id):
    ub = get_object_or_404(UnitBoiler, id=id)
    context={}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            ub.delete()
            return HttpResponseRedirect(reverse('setparam:createub'))
        except ProtectedError:
            judul = 'Tambahkan Identitas Unit Boiler'
            units = UnitBoiler.objects.all()
            form = UnitBoilerForm(None)
            pesan = "Unit boiler tidak bisa dihapus"
            context ={
                'judul':judul,
                'form': form,
                'units': units,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'setparam/unitform.html', context)
    else:
        context = {
            'object': ub,
            }
        return render(request, 'setparam/confirm_deleteunit.html', context)

def update_unitboiler(request,id):
    units = UnitBoiler.objects.all()
    context ={}
    unit = get_object_or_404(UnitBoiler, id=id)
    form = UnitBoilerForm(instance=unit)
    judul = 'Update Identitas Unit Boiler'
    edited = True
    if request.method == 'POST':
        form = UnitBoilerForm(request.POST,instance=unit)
        if form.is_valid():
           form.save()
           return redirect('setparam:viewunit',id = unit.id)

    context = {

               'form': form,
               'units': units,
               'judul': judul,
               'edited': edited,
    }
    return render(request, 'setparam/unitform.html', context)

def view_unitboiler(request, id):
    units = UnitBoiler.objects.all()
    unit = get_object_or_404(UnitBoiler, id=id)
    form = UnitBoilerForm(instance=unit)
    edited = False
    judul = 'View Unit Boiler'
    context = {
            'unit': unit,
            'units': units,
            'judul': judul,
            'form':form,
            'edited': edited,
    }
    return render(request, 'setparam/unitform.html', context)


# Create your views here.
def update_hargaparkiraanbb(request,id):
    judul = 'Edit Harga Perkiraan Batubara'

    context ={}
    hpb = get_object_or_404(HargaPerkiraanBB, id=id)
    form = HargaPerkiraanBBForm(instance=hpb)

    if request.method == 'POST':
        form = UnitBoilerForm(request.POST,instance=hpb)
        if form.is_valid():
           form.save()
           return HttpResponseRedirect(reverse('setparam:createhpbb'))
    judul = 'Update Identitas Unit Boiler'
    context = {
        'form': form,
        'hpb': hpb,
        'judul': judul,
    }

    return render(request,'setparam/createHPBB.html', context)


from django.shortcuts import render, get_object_or_404,redirect, HttpResponseRedirect,reverse
from .forms import BlendingForm,SearchBlendingHistoryByUnitForm, NotesForm, BlendOnUnitFrom, PrepareBlandForm
from coaljson.models import CoalSpec, CoalStockUnit, CoalForBlend
from .nemesys import Coal,Blending, CoFiring, CoalBlending, BlendingHistories,CofiringWithoutGA
from setparam.models import BoilerSetting, UnitBoiler, ParameterBlending, RohUnit
from .models import BlendingOnUnit, Notes, BlendOnUnit
import datetime, json
from .gacofiringalpha import GACofiringAlpha as gca
import random

def prepare_for_blend(request):
    current_user = request.user
    pesan =None
    form = PrepareBlandForm(request.POST or None)
    if request.method == "POST":
        #form = PrepareBlandForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            tanggal = form.cleaned_data['tanggal']
            waktu = form.cleaned_data['waktu']
            # get roh from setting: RohUnit unit timestamp roh

            rohunit = RohUnit.objects.filter(unit= unit,timestamp__date=tanggal, timestamp__hour = waktu.hour, timestamp__minute = waktu.minute)
            if not rohunit:
                #pesan kesalahan kalau roh unit belum di set
                pesan = "Roh Unit belum diset, lakukan pengecekan di setting parameter"
                context = {
                    'form': form,
                    'pesan': pesan,
                }
                return render(request, 'blending/prepare_blending.html', context)

            else:
                roh = rohunit[0].roh
                pesan = rohunit[0].roh
                form = BlendingForm(initial={'unit':unit, 'rohunit':roh, 'tanggal': tanggal, 'waktu':waktu})
                context = {
                    'form':form,
                    'pesan':pesan,
                }
                return render(request, 'blending/blending.html', context)
                #redirect = HttpResponseRedirect('urlblending') #change the part of urlblending with url goal
    else:
        context ={
            'form': form,
            'pesan': current_user,
        }
    return render(request, 'blending/prepare_blending.html', context)



def blend(request):
    if request.method == 'POST':
        current_user = request.user
        #perlu fungsi untuk membaca roh berdasarkan unit, tanggal dan waktu blending

    context = {}
    form = BlendOnUnitFrom(None)
    bio = None
    coalyard = None
    tongkang = None
    pesan ="siapkan untuk proses blending"
    status= "inisiasi proses"
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            tanggal = form.cleaned_data['tanggal']
            waktu = form.cleaned_data['waktu']

            kalori = form.cleaned_data['targetkalor']
            roh = form.cleaned_data['roh']
            persenbio = form.cleaned_data['persenbio']
            #sekarang = datetime.date.today()
            #pb = ParameterBlending.objects.get(unit=unit)
            #ambil data coal pada basisdata
            items = list(Coal.objects.filter(kategori_bhn_baku='BIO'))
            bio = random.sample(items, 1)[0]
            items = list(Coal.objects.filter(kategori_bhn_baku='BB'))
            tongkang = random.sample(items, 1)[0]
            items = gca.get_coal_opposite_category(tongkang,items)
            coalyard = random.sample(items,random.randint(len(items)))
            #stocks = CoalForBlend.objects.filter(unit=unit, tanggal=tanggal, waktu = waktu)
            if not bio or tongkang or not coalyard:
                #coals = None #lakukan penanganan
                status = "tidak ada bahan bakar untuk diproses"
                pesan = 'lakukan pengecekan melalui menu stock bahan bakar'
                context = {
                    'form': form,
                    'bio': bio,
                    'tongkang': tongkang,
                    'coalyard': coalyard,
                    'pesan': pesan,
                    'status': status,
                    'user': current_user
                }
                return render(request, 'blending/blending.html', context)
            else:
                if len(bio)==1 and len(tongkang)==1 and len(coalyard)>=1:
                    #pengecekan status perlu atau tidak blending
                    # jika tidak perlu maka tampilkan batubara yang sesuai dan kembaikan respon
                    if (tongkang.kalori > kalori):
                        pesan = "tidak perlu blending!"
                        status = "bahan bakar yang tersedia tidak perlu blending"
                        context = {
                            'form': form,
                            'bio': bio,
                            'tongkang': tongkang,
                            'coalyard': coalyard,
                            'pesan': pesan,
                            'status': status,
                            'user': current_user
                        }
                        return render(request, 'blending/blending.html', context)
                    else:
                        #jika ya maka lakukan proses blending
                        # 'unit','tanggal','waktu','kalori','persenbio','roh',
                        gacof = gca.GACofiringAlpha()
                        # default n_pop=1000, laju_mutasi=0.6, iter=30
                        best_cromosom = gacof.ga_cofiring(target_kalor= kalori, tongkang=tongkang, coalyard=coalyard, biomassa=bio, persen_biomassa=persenbio)
                        #urutkan best cromosom menjadi coal
                        idx_coal= [cromosom[1] for cromosom in enumerate(best_cromosom)]
                        coalyard =  [x for _, x in sorted(zip(idx_coal, coalyard))]
                        status = "proses optimasi blending selesai"
                        pesan = "silahkan pilih putusan blending yang akan diambil"
                        context = {
                            'form': form,
                            'bio': bio,
                            'tongkang': tongkang,
                            'coalyard': coalyard,
                            'pesan': pesan,
                            'status': status,
                            'user': current_user
                        }
                        return render(request, 'blending/blending.html', context)
    else:
        coals = None
        form = BlendingForm(initial={'persenbiomassa': 1})
        context = {
            'form': form,
            'bio': bio,
            'tongkang': tongkang,
            'coalyard': coalyard,
            'pesan':pesan,
            'status': status,
            'user': current_user
        }
    return render(request, 'blending/blending.html', context)

def create_note(request):
    context ={}
    notes = Notes.objects.all()
    if request.method =="POST":
        form = NotesForm(request.POST)
        if form.is_valid():
           note = form.save(commit= False)
           note.user = request.user
           note.save()
    else:
        form = NotesForm()

    judul ='Tambahkan Pesan'
    context = {
        'form':form,
        'notes':notes,
        'judul': judul,
    }
    return render(request,'blending/noteform.html',context)

def search_resume_history(request):
    tampil = False
    pesan = None
    histories = None
    if request.method == 'POST':
        form = SearchBlendingHistoryByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            blendinghistories = BlendingOnUnit.objects.filter(unit=unit)
            #ekstraksi informasi
            histories =[]
            for blendinghistory in blendinghistories:
                history = BlendingHistories(blendinghistory)
                histories.append(history)

            if blendinghistories is None:
                pesan = "Data tidak ditemukan"
                tampil = False
            else:
                tampil = True
    else:
        form = SearchBlendingHistoryByUnitForm()
    context = {
        'form': form,
        'tampil': tampil,
        'pesan': pesan,
        'histories': histories

    }
    return render(request, 'blending/arsipblendingresume.html', context=context)

def search_history(request):
    tampil = False
    pesan = None
    blendinghistories = None
    if request.method == 'POST':
        form = SearchBlendingHistoryByUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            blendinghistories= BlendingOnUnit.objects.filter(unit=unit)
            if blendinghistories is None:
                pesan = "Data tidak ditemukan"
                tampil = False
            else:
                tampil = True
    else:
        form = SearchBlendingHistoryByUnitForm()
    context = {
        'form':form,
        'tampil': tampil,
        'pesan':pesan,
        'blendinghistories':blendinghistories

    }
    return render(request,'blending/arsipblending.html',context=context)

def fill_form_blending2(request):
    current_user = request.user
    context = {}
    status = None
    coals = None
    parameterblending = None
    cofiring = None
    biomassa = None
    blending_result = None
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            #pb = ParameterBlending.objects.get(unit=unit)
            try:
                stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
                coals = []
                for item in stocks:
                    coal = Coal(item.coalstock)
                    coals.append(coal)

                blending = Blending()
                TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                status_split=f'tmrc:{len(TMRC)}, tlrc:{len(TLRC)},cmrc:{len(CMRC)},clrc:{len(CLRC)},bio:{len(Biomass)}'
                statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
                strstatus = "".join(str(x) for x in statusstok)
                #statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                #    targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                #   persen_biomass=persenbiomassa)
                statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending_update(
                        targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                       persen_biomass=persenbiomassa)
                if persenbiomass > 0 or persenbiomassa > 0:
                    status_br= 'cofiring'
                else:
                    status_br = 'coalblending'
                blending_result ={
                    'status_split': status_split,
                    'statusblending': statusblending,
                    'coal1': coal1,
                    'coal2':coal2,
                    'biomassa': biomassa,
                    'persenc1':persenc1,
                    'persenc2': persenc2,
                    'persenbiomassa':persenbiomass,
                    'status': status_br
                }

                if status_br == 'cofiring':
                    # boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                    # parameterblending = ParameterBlending.objects.get(pk=1)
                    #parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                    status = True
                    cofiring = None
                    try:
                        pb = ParameterBlending.objects.get(unit=unit)
                        cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass,pb)
                        status = 'cofiring'
                        c1 = json.dumps(coal1)
                        c2 = json.dumps(coal2)
                        b = json.dumps(biomassa)
                        cof = json.dumps(cofiring.cofiringinjsonformat())
                        blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang, settingunit=pb,
                                                   coal1=c1, coal2=c2,biomass=b,cofiring=cof)
                        parameterblending = {
                                'statusstok': strstatus,
                                'targetkalor': targetkalor,
                                'cofiring': cofiring,
                                'status': status,
                            }


                    except ParameterBlending.DoesNotExist:
                        form.ValidationError()
                elif status_br == 'coalbending':
                    pb = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoalBlending(coal1, coal2, persenc1, persenc2, pb)
                    status = 'coalblending'

                    c1 = json.dumps(coal1)
                    c2 = json.dumps(coal2)

                    """

                    c1 = json.dumps(coal1.jsoninlongformat())
                    c2 = json.dumps(coal2.jsoninlongformat())
                    """
                    cof = json.dumps(cofiring.coalblendinginlongformat())
                    blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                          settingunit=pb,
                                                          coal1=c1, coal2=c2, cofiring=cof)
                    parameterblending = {
                        'statusstok': strstatus,
                        'targetkalor': targetkalor,
                        'cofiring': cofiring,
                        'status': status,
                    }
                # save data ke database blendingresult
                # unit, user, tanggal,settingunit coal1 coal2 biomass cofiring


            except CoalStockUnit.DoesNotExist:
                coals = None
                status = 'nostock'
                parameterblending ={
                    'status': status,
                    'coals':coal,
                }
    else:
        coals = None
        parameterblending = None
        form = BlendingForm(request.POST)
    context = {
        'form': form,
        'coals': coals,
        'blending_result':blending_result,
        'parameterblending': parameterblending,
    }
    return render(request, 'blending/blending2.html', context)

def fill_form_blending2old(request):
    current_user = request.user
    context = {}
    status = None
    coals = None
    parameterblending = None
    cofiring = None
    biomassa = None
    blending_result = None
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            # pb = ParameterBlending.objects.get(unit=unit)
            try:
                stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
                coals = []
                for item in stocks:
                    coal = Coal(item.coalstock)
                    coals.append(coal)

                blending = Blending()
                TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                status_split = f'tmrc:{len(TMRC)}, tlrc:{len(TLRC)},cmrc:{len(CMRC)},clrc:{len(CLRC)},bio:{len(Biomass)}'
                statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
                strstatus = "".join(str(x) for x in statusstok)
                # statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                #    targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                #   persen_biomass=persenbiomassa)
                statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending_update(
                    targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                    persen_biomass=persenbiomassa)
                if persenbiomass > 0 or persenbiomassa > 0:
                    status_br = 'cofiring'
                else:
                    status_br = 'coalblending'
                blending_result = {
                    'status_split': status_split,
                    'statusblending': statusblending,
                    'coal1': coal1,
                    'coal2': coal2,
                    'biomassa': biomassa,
                    'persenc1': persenc1,
                    'persenc2': persenc2,
                    'persenbiomassa': persenbiomass,
                    'status': status_br
                }

                if status_br == 'cofiring':
                    # boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                    # parameterblending = ParameterBlending.objects.get(pk=1)
                    # parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                    status = True
                    cofiring = None
                    try:
                        pb = ParameterBlending.objects.get(unit=unit)
                        if biomassa != None:
                            cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, pb)
                            status = 'cofiring'

                            """

                            c1 = json.dumps(coal1.jsoninlongformat())
                            c2 = json.dumps(coal2.jsoninlongformat())
                            b = json.dumps(biomassa.jsoninlongformat())
                            """
                            c1 = json.dumps(coal1)
                            c2 = json.dumps(coal2)
                            b = json.dumps(biomassa)
                            cof = json.dumps(cofiring.cofiringinjsonformat())
                            blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                                  settingunit=pb,
                                                                  coal1=c1, coal2=c2, biomass=b, cofiring=cof)
                            parameterblending = {
                                'statusstok': strstatus,
                                'targetkalor': targetkalor,
                                'cofiring': cofiring,
                                'status': status,
                            }


                    except ParameterBlending.DoesNotExist:
                        form.ValidationError()
                elif status_br == 'coalbending':
                    pb = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoalBlending(coal1, coal2, persenc1, persenc2, pb)
                    status = 'coalblending'

                    c1 = json.dumps(coal1)
                    c2 = json.dumps(coal2)

                    """

                    c1 = json.dumps(coal1.jsoninlongformat())
                    c2 = json.dumps(coal2.jsoninlongformat())
                    """
                    cof = json.dumps(cofiring.coalblendinginlongformat())
                    blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                          settingunit=pb,
                                                          coal1=c1, coal2=c2, cofiring=cof)
                    parameterblending = {
                        'statusstok': strstatus,
                        'targetkalor': targetkalor,
                        'cofiring': cofiring,
                        'status': status,
                    }
                # save data ke database blendingresult
                # unit, user, tanggal,settingunit coal1 coal2 biomass cofiring


            except CoalStockUnit.DoesNotExist:
                coals = None
                status = 'nostock'
                parameterblending = {
                    'status': status,
                    'coals': coal,
                }
    else:
        coals = None
        parameterblending = None
        form = BlendingForm(request.POST)
    context = {
        'form': form,
        'coals': coals,
        'blending_result': blending_result,
        'parameterblending': parameterblending,
    }
    return render(request, 'blending/blending2.html', context)

def get_dist(elem):
        return elem[1]

def dist_to_target(coals:[Coal],bio:[Coal], target_kalor,persenbiomassa):
    #ambil data bio
    if bio is not None:
        target_kalor_baru = target_kalor - (persenbiomassa / 100) * bio[0].Kalori
        coal_dist = [(coal, coal.Kalori-target_kalor_baru) for coal in coals if coal.Kalori>target_kalor_baru]

    else:
        coal_dist = [(coal, coal.Kalori - target_kalor) for coal in coals if coal.Kalori > target_kalor]

    coal_dist = sorted(coal_dist, key=get_dist, reverse=False)
    #print(f'{coal_dist[0][1]}')
    #print(f'{coal_dist[4][1]}')
    return coal_dist[0], bio[0]

def calculate_blending(request):
    current_user = request.user
    context = {}
    status = True
    pesan = None
    coals = None
    cofiring = None
    coalblending = None
    statusblending = None
    if request.method == "POST":
        status = False
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            pb = ParameterBlending.objects.get(unit=unit)
            stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
            if not stocks:
                coals = None #lakukan penanganan
                pesan = 'stok batubara belum tersedia, lakukan pengecekan melalui menu stock bahan bakar'
                context = {
                    'form': form,
                    'coals': None,
                    'cofiring': None,
                    'coalblending': None,
                    'pesan': pesan,
                    'status':status
                }
                return render(request, 'blending/blending.html', context)
            else:
                coals = []
                biomassa =[]
                for coalspec in stocks:
                    coal = Coal(coalspec.coalstock)
                    if coal.jsoninlongformat().get('Kategori')=='biomassa':
                        biomassa.append(coal)
                    else:
                        coals.append(coal)
                #cek apakah perlu blending atau tidak
                #newcoals = coals.sort(key= lambda x:x.Kalori,reverse=True)

                coal_sesuai =[(coal, coal.Kalori) for coal in coals if coal.Kalori == targetkalor]
                print(f'coal sesuai:{len(coal_sesuai)} ')
                if len(coal_sesuai)>0  :
                    target_coal,bio = dist_to_target(coals,biomassa, targetkalor,persenbiomassa)
                    #cofiring
                    cofiring = CofiringWithoutGA(target_coal[0], bio, persenbiomassa, pb)
                    pesan = 'cofiring tanpa optimasi karena target kalor sudah terpenuhi'
                    context = {
                        'form': form,
                        'coals': coals,
                        'cofiring': cofiring,
                        'coalblending': None,
                        'pesan': pesan,
                        'status': status
                    }
                    return render(request, 'blending/blending.html', context)
                else:
                    coals.append(biomassa[0])
                    blending = Blending()
                    TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                   #blending = Blending()
                    #TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                    statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending_update(
                            targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomass=Biomass,persen_biomass=persenbiomassa)
                    if statusblending == 'cofiring':
                        cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, pb)

                        c1 = json.dumps(coal1)
                        c2 = json.dumps(coal2)
                        b = json.dumps(biomassa)
                        cof = json.dumps(cofiring.cofiringinjsonformat())
                        blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                              settingunit=pb,
                                                              coal1=c1, coal2=c2, biomass=b, cofiring=cof)
                        pesan = 'cofiring dapat dilakukan'
                        context = {
                            'form': form,
                            'coals': coals,
                            'cofiring': cofiring,
                            'coalblending': coalblending,
                            'pesan': pesan,
                            'status': status
                        }
                        return render(request, 'blending/blending.html', context)
                    elif statusblending == 'coalblending':
                        coalblending = CoalBlending(coal1, coal2, persenc1, persenc2, pb)
                        c1 = json.dumps(coal1)
                        c2 = json.dumps(coal2)

                        cof = json.dumps(coalblending.coalblendinginlongformat())
                        blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                              settingunit=pb,
                                                              coal1=c1, coal2=c2, cofiring=cof)
                        pesan = 'bleanding bisa dilakukan'
                        context = {
                            'form': form,
                            'coals': coals,
                            'cofiring': cofiring,
                            'coalblending': coalblending,
                            'pesan': pesan,
                            'status': status
                        }
                        return render(request, 'blending/blendingcb.html', context)


    else:
        coals = None
        form = BlendingForm(initial={'persenbiomassa': 1})
    context = {
        'form': form,
        'coals': coals,
        'cofiring': cofiring,
        'coalblending':coalblending,
        'pesan':pesan,
        'status': status
    }
    return render(request, 'blending/blending.html', context)
def calculate_blending_old(request):
    current_user = request.user
    context = {}
    pesan = None
    coals = None
    cofiring = None
    coalblending = None
    statusblending = None
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            pb = ParameterBlending.objects.get(unit=unit)
            stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
            if not stocks:
                coals = None #lakukan penanganan
                pesan = 'stok batubara belum tersedia, lakukan pengecekan melalui menu stock bahan bakar'
                context = {
                    'form': form,
                    'coals': None,
                    'cofiring': None,
                    'coalblending': None,
                    'pesan': pesan,
                }
                return render(request, 'blending/blending.html', context)
            else:
                coals = []
                biomassa =[]
                for coalspec in stocks:
                    coal = Coal(coalspec.coalstock)
                    coals.append(coal)
                #cek apakah perlu blending atau tidak
                #newcoals = coals.sort(key= lambda x:x.Kalori,reverse=True)

                coal_diatas_treshold =[(coal, coal.Kalori) for coal in coals if coal.Kalori>= targetkalor]
                if len(coal_diatas_treshold)>0  :
                    target_coal,bio = dist_to_target(coals,targetkalor,persenbiomassa)
                    #cofiring
                    cofiring = CofiringWithoutGA(target_coal[0], bio, persenbiomassa, pb)
                    pesan = 'cofiring tanpa optimasi karena target kalor sudah terpenuhi'
                    context = {
                        'form': form,
                        'coals': coals,
                        'cofiring': cofiring,
                        'coalblending': None,
                        'pesan': pesan,
                    }
                    return render(request, 'blending/blending.html', context)
                else:
                    blending = Blending()
                    TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                   #blending = Blending()
                    #TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                    statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending_update(
                            targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomass=Biomass,persen_biomass=persenbiomassa)
                    if statusblending == 'cofiring':
                        cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, pb)

                        c1 = json.dumps(coal1)
                        c2 = json.dumps(coal2)
                        b = json.dumps(biomassa)
                        cof = json.dumps(cofiring.cofiringinjsonformat())
                        blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                              settingunit=pb,
                                                              coal1=c1, coal2=c2, biomass=b, cofiring=cof)
                        pesan = 'cofiring dapat dilakukan'
                        context = {
                            'form': form,
                            'coals': coals,
                            'cofiring': cofiring,
                            'coalblending': coalblending,
                            'pesan': pesan,
                        }
                        return render(request, 'blending/blending.html', context)
                    elif statusblending == 'coalblending':
                        coalblending = CoalBlending(coal1, coal2, persenc1, persenc2, pb)
                        c1 = json.dumps(coal1)
                        c2 = json.dumps(coal2)

                        cof = json.dumps(coalblending.coalblendinginlongformat())
                        blend = BlendingOnUnit.objects.create(unit=unit, user=current_user, tanggal=sekarang,
                                                              settingunit=pb,
                                                              coal1=c1, coal2=c2, cofiring=cof)
                        pesan = 'bleanding bisa dilakukan'
                        context = {
                            'form': form,
                            'coals': coals,
                            'cofiring': cofiring,
                            'coalblending': coalblending,
                            'pesan': pesan,
                        }
                        return render(request, 'blending/blendingcb.html', context)


    else:
        coals = None
        form = BlendingForm(request.POST)
    context = {
        'form': form,
        'coals': coals,
        'cofiring': cofiring,
        'coalblending':coalblending,
        'pesan':pesan,
    }
    return render(request, 'blending/blending.html', context)

def fill_form_blending1(request):
    context ={}
    status = None
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.datetime.now()
            try:
                parameterblending = ParameterBlending.objects.get(unit=unit)
                status = 'Ok'
            except parameterblending.DoesNotExist:
                param = {

                }
            try:
                stocks = CoalStockUnit.objects.filter(unit=unit, tanggal__year=sekarang.year,
                                                      tanggal__month=sekarang.month,
                                                      tanggal__day=sekarang.day)
                try:
                    parameterblending = ParameterBlending.objects.get(unit= unit)
                    coals = []
                    for coalspec in stocks:
                        coal = Coal(coalspec.coalstock)
                        coals.append(coal)
                    blending = Blending()
                    TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
                    statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
                    strstatus = "".join(str(x) for x in statusstok)
                    statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                        targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                        persen_biomass=persenbiomassa)
                    if statusblending:
                        cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass,
                                            parameterblending)
                        status = True
                    parameterblending = {
                        'statusstok': strstatus,
                        'targetkalor': targetkalor,
                        'cofiring': cofiring,
                        'status': status,
                    }
                except parameterblending.DoesNotExist:
                    parameterblending = {

                    }

            except:
                stocks = None

    else:
        coals = None
        parameterblending = None
        form = BlendingForm(request.POST)
    context = {
        'form': form,
        'coals': coals,
        'parameterblending': parameterblending
    }
    return render(request, 'blending/blending.html', context)

def calculate_opt_blending1(request):
    parameterblending = None
    #coalspecs = CoalSpec.objects.all()
    unit = UnitBoiler.objects.all()
    # create Coal object and append to list
    cofiring = None
    coals = None
    status =None
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)

            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']
            sekarang = datetime.date.today()
            stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
            coals = []
            for item in stocks:
                coal = Coal(item.coalstock)
                coals.append(coal)

            blending = Blending()
            TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
            statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
            strstatus = "".join(str(x) for x in statusstok)
            statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                persen_biomass=persenbiomassa)

            if statusblending:
                #boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                #parameterblending = ParameterBlending.objects.get(pk=1)
                parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                status = True

                try:
                    instance = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, parameterblending)
                except ParameterBlending.DoesNotExist:
                    form.ValidationError()
            parameterblending = {
                'statusstok': strstatus,
                'targetkalor': targetkalor,
                'cofiring': cofiring,
                'status': status,
            }
            # redirect('boilersettingunit_view',unit_pk = pk)

    else:
        form = BlendingForm()
    context = {
        'form': form,
        'coals': coals,
        'parameterblending': parameterblending
    }
    return render(request, 'blending/blending.html', context)

def calculate_opt_blending(request):
    parameterblending = None
    status = None
    cofiring = None
    #coalspecs = CoalSpec.objects.all()
    sekarang = datetime.date.today()
   # stocks = CoalStockUnit.objects.filter(unit=unit, tanggal=sekarang)
    stocks = CoalStockUnit.objects.filter(tanggal=sekarang)
    coalspecs =stocks
    coals = []
    for item in stocks:
        coal = Coal(item.coalstock)
        coals.append(coal)

    unit = UnitBoiler.objects.all()
    # create Coal object and append to list

    coals = []
    for item in coalspecs:
        coal = Coal(item.coalstock)
        coals.append(coal)
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)

            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']

            blending = Blending()
            TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
            statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
            strstatus = "".join(str(x) for x in statusstok)
            statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                persen_biomass=persenbiomassa)

            if statusblending:
                #boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                #parameterblending = ParameterBlending.objects.get(pk=1)
                parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                status = True

                try:
                    instance = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, parameterblending)
                except ParameterBlending.DoesNotExist:
                    form.ValidationError()
            parameterblending = {
                'statusstok': strstatus,
                'targetkalor': targetkalor,
                'cofiring': cofiring,
                'status': status,
            }
            # redirect('boilersettingunit_view',unit_pk = pk)

    else:
        form = BlendingForm()
    context = {
        'form': form,
        'coals': coals,
        'parameterblending': parameterblending
    }
    return render(request, 'blending/blending2.html', context)

def calculate_opt_blending2(request):
    parameterblending = None
    coalspecs = CoalSpec.objects.all()
    unit = UnitBoiler.objects.all()
    # create Coal object and append to list

    coals = []
    for item in coalspecs:
        coal = Coal(item.coalspecdata)
        coals.append(coal)
    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)

            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']

            blending = Blending()
            TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
            statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
            strstatus = "".join(str(x) for x in statusstok)
            statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                persen_biomass=persenbiomassa)

            if statusblending:
                #boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                #parameterblending = ParameterBlending.objects.get(pk=1)
                parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                status = True
                cofiring = None
                try:
                    instance = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, parameterblending)
                except ParameterBlending.DoesNotExist:
                    form.ValidationError()
            parameterblending = {
                'statusstok': strstatus,
                'targetkalor': targetkalor,
                'cofiring': cofiring,
                'status': status,
            }
            # redirect('boilersettingunit_view',unit_pk = pk)

    else:
        form = BlendingForm()
    context = {
        'form': form,
        'coals': coals,
        'parameterblending': parameterblending
    }
    return render(request, 'blending/blending.html', context)
# Create your views here.
def calculate_blending_old(request):
    parameterblending = None
    coalspecs = CoalSpec.objects.all()
    unit = UnitBoiler.objects.all()
    # create Coal object and append to list

    coals = []
    for item in coalspecs:
        coal = Coal(item.coalspecdata)
        coals.append(coal)

    if request.method =="POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            #form.save(commit=False)

            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']

            blending = Blending()
            TMRC,TLRC,CMRC,CLRC, Biomass = blending.split_coal_by_tag_category(coals)
            statusstok= blending.coal_stock_status(TMRC,TLRC,CMRC,CLRC, Biomass)
            strstatus = "".join(str(x) for x in statusstok)
            statusblending, coal1,coal2,biomassa,persenc1,persenc2,persenbiomass= blending.calculate_blending(targetkalor,TMRC=TMRC,TLRC=TLRC,CMRC=CMRC,CLRC=CLRC,biomassa=Biomass,persen_biomass=persenbiomassa)
            if statusblending:
                boilersetting = BoilerSetting.objects.get(pk=1)
                cofiring = CoFiring(coal1,coal2,biomassa,persenc1,persenc2,persenbiomass,boilersetting)
                status = True
            else:
                cofiring = None
                status = False

            parameterblending = {
                'statusstok': strstatus,
                'targetkalor': targetkalor,
                'cofiring': cofiring,
                'status': status,
            }
            #redirect('boilersettingunit_view',unit_pk = pk)

    else:
        form = BlendingForm()
    context ={
        'form':form,
        'coals':coals,
        'parameterblending':parameterblending
    }
    return render(request,'blending/blending.html',context)

#
def calculate_opt_blending_old1(request):
    parameterblending = None
    coalspecs = CoalSpec.objects.all()

    # create Coal object and append to list

    coals = []
    for item in coalspecs:
        coal = Coal(item.coalspecdata)
        coals.append(coal)

    if request.method == "POST":
        form = BlendingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)

            targetkalor = form.cleaned_data['targetkalor']
            persenbiomassa = form.cleaned_data['persenbiomassa']
            unit = form.cleaned_data['unit']

            blending = Blending()
            TMRC, TLRC, CMRC, CLRC, Biomass = blending.split_coal_by_tag_category(coals)
            statusstok = blending.coal_stock_status(TMRC, TLRC, CMRC, CLRC, Biomass)
            strstatus = "".join(str(x) for x in statusstok)
            statusblending, coal1, coal2, biomassa, persenc1, persenc2, persenbiomass = blending.calculate_blending(
                targetkalor, TMRC=TMRC, TLRC=TLRC, CMRC=CMRC, CLRC=CLRC, biomassa=Biomass,
                persen_biomass=persenbiomassa)
            if statusblending:
                #boilersetting = BoilerSetting.objects.get(pk=1) #get boilersetting base on unit
                #parameterblending = ParameterBlending.objects.get(pk=1)
                parameterblending = get_object_or_404(ParameterBlending, unit=unit)
                status = True
                cofiring = None
                try:
                    instance = ParameterBlending.objects.get(unit=unit)
                    cofiring = CoFiring(coal1, coal2, biomassa, persenc1, persenc2, persenbiomass, parameterblending)
                except ParameterBlending.DoesNotExist:
                    form.ValidationError()
            parameterblending = {
                'statusstok': strstatus,
                'targetkalor': targetkalor,
                'cofiring': cofiring,
                'status': status,
            }
            # redirect('boilersettingunit_view',unit_pk = pk)

    else:
        form = BlendingForm()
    context = {
        'form': form,
        'coals': coals,
        'parameterblending': parameterblending
    }
    return render(request, 'blending/blending.html', context)
def coalspec_list(request):
    coalspecs = CoalSpec.objects.all()
    #create Coal object and append to list
    coals =[]
    for item in coalspecs:
        coal = Coal(item.coalspecdata)
        coals.append(coal)
        #print(coal.jsoninshortformat())
    #
    return render(request,'blending/coalstock.html',{'coalspecs':coalspecs, 'coals':coals})




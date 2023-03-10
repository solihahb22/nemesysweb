from setparam.models import ParameterOptPembebanan
class OptimasiBebanUnit:
    def __init__(self,unit,punit,bea_pembangkit,nphr,beaprod,rk):
        setattr(self, 'unit', unit)
        setattr(self,'punit',punit)
        setattr(self,'bea_pembangkit',bea_pembangkit)
        setattr(self,'nphr',nphr)
        setattr(self,'beaprod',beaprod)
        setattr(self,'rk',rk)


def get_koef_rekomendasi_kalor(prmOptBlist):
   koef_rek_kal =[]
   for i in range(len(prmOptBlist)):
       d = float(prmOptBlist[i].koef_d_rek_kalor)
       e = float(prmOptBlist[i].koef_e_rek_kalor)
       f = float(prmOptBlist[i].koef_f_rek_kalor)
       rk = (d,e,f)
       koef_rek_kal.append(rk)
   return koef_rek_kal




def get_koef_ic(prmOptBlist):
   koef_ic =[]

   for i in range(len(prmOptBlist)):
        a = float(prmOptBlist[i].koef_a_opt_beban)
        b = float(prmOptBlist[i].koef_b_opt_beban)
        c = float(prmOptBlist[i].koef_c_opt_beban)
        ic = (a,b,c)
        koef_ic.append(ic)
   return koef_ic

def get_daya_net_units(prmOptBlist):
    daya_net =[]

    for i in range(len(prmOptBlist)):
        a = prmOptBlist[i].daya_min
        b = prmOptBlist[i].daya_max
        pi = (a, b)
        daya_net.append(pi)
    return daya_net

def optimasi_beban_unit(Preq,prmOptBlist):
    koef_ic = get_koef_ic(prmOptBlist)
    daya_net = get_daya_net_units(prmOptBlist)
    koef_lambda = 400000
    d_lam = 0
    loop = True
    iterasike = 0;
    while loop:
       #getparam koef_ic
        P = calculate_beban_each_unit(koef_lambda, koef_ic)
        dP = delta_P_unit(Preq, P)
        #print(f'dP:{dP}')
        #print(f'P: {P}')
        P = cek_kesesuaian_beban_unit(P,daya_net)
        #print(f'P penyesuaian:{P}')
        dP = delta_P_unit(Preq, P)
        #print(f'dP:{dP}')
        if (dP == 0):
            break
        d_lam_pre = d_lam
        d_lam = delta_lambda(dP, koef_ic)
        if d_lam_pre == d_lam :
            loop = False
        koef_lambda = koef_lambda + d_lam
        #print(f'koefisien lamda:{koef_lambda}')
        iterasike += 1
        if iterasike == 1000000:
           loop = False
        #print(f'iterasi ke{iterasike}')
    return P

def calculate_beban_each_unit(koef_lambda, koef_ic):
    P = []
    for koefisien in koef_ic:
        a, b, c = koefisien
        # print(f'a:{a} b:{b} c:{c}')
        bebanunit= round((koef_lambda - b) / (2 * float(a)))
        P.append(bebanunit)
        # print(f'koef lambda: {koef_lambda} beban unit:{bebanunit}')
    return P



def delta_P_unit(P_beban,Punit):
    dP=P_beban
    for v in Punit:
       dP=dP-v
    return dP

def delta_lambda(deltaPunit,koef_ic):
    pembagi=0
    for koef in koef_ic:
        a,b,c = koef
        pembagi += 1/(2*float(a))
        print(f'a:{a}, {1/(2*a)}')
    if pembagi >0:
        d_l = deltaPunit/pembagi
    else:
        d_l = deltaPunit
    return d_l

def cek_kesesuaian_beban_unit(P, daya_net):
    for i in range(len(daya_net)):
       min_dn = daya_net[i][0]
       max_dn = daya_net[i][1]
       for idx,v in enumerate(P):
        #print(f'{idx},{v}')
          if v < min_dn:
              P[idx]= min_dn   #dn: daya unit
          elif v> max_dn:
              P[idx]= max_dn
          else:
              P[idx]=v
    return P

def hitung_bpu(poptb: ParameterOptPembebanan, punit):
    cost = poptb.koef_a_opt_beban* punit* punit + poptb.koef_b_opt_beban*punit + poptb.koef_c_opt_beban
    return cost

def hitung_biaya_pembangkitan(Punit:[], koef_ic):
    costApp = []
    for i in range(len(Punit)):
       costs = float(koef_ic[i][0])* Punit[i]* Punit[i] + float(koef_ic[i][1])*Punit[i] + float(koef_ic[i][2])
       costApp.append(costs)
    return costApp
def hitungnphru(punit, bpu,harga_bb):
    nphr = bpu/ (punit * 1000 * harga_bb)
    return nphr

def hitungnphrunit(Punit:[],biaya_pembangkitan:[],harga_bb_perkcal):
    nphrunit =[]
    for i in range(len(Punit)):
        nphr = biaya_pembangkitan[i]/(Punit[i]*1000*harga_bb_perkcal)
        nphrunit.append(nphr)
    return nphrunit

def hitungbiayaproduksi(Punit,biaya_pembangkitan_unit):
    biaya = []
    for i in range(len(Punit)):
        b_unit =  biaya_pembangkitan_unit[i]/(Punit[i]*1000)
        biaya.append(b_unit)
    return biaya

def hitung_rekomendasi_kalor(Punit, nphr_unit,koef_rk):

    rk =[]
    for i in range(len(Punit)):
        rki = koef_rk[i][0]+koef_rk[i][1]*Punit[i] + koef_rk[i][2]*nphr_unit[i]
        rk.append(rki)
    return rk

def hitung_rk(punit, nphr_unit,koef_rk):
    rki = koef_rk[0]+koef_rk[1]*punit+ koef_rk[2]*nphr_unit

    return rki


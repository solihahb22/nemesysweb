import json
from .ga import GA, print_cromosom
from .gacofiring import GACofiring
from scipy import interpolate
from numpy import interp
from setparam.models import ParameterBlending
from .models import BlendingOnUnit
from operator import itemgetter


class Coal:
    """
    coal.properties ==> Pemasok,Kalori, TM (total_Moisture), TS (total_Sulfur),ASH,IDTReducing,SiO2,
                            Al2O3,Fe2O3,CaO,MgO,Na2O,K2O, TiO2,SO,HTmax",JenisAbu,SI, Slagging
                            C (Carbon_content), H(Hydrogen_content), N (Nitrogen_content),O(Oxygen_content)
     contoh data coal dalam format json:
            {"Pemasok":"Bukit Asam", "Kalori": 4732, "TM": 29.19, "TS": 0.36, "ASH": 5.76,
            "IDTReducing": 1270, "SiO2": 57.96, "Al2O3": 26.85, "Fe2O3": 5.19, "CaO": 3.24,
            "MgO": 1.43, "Na2O": 1.2, "K2O": 0.59, "TiO2": 1.02, "SO3": 1.95,
            "HTmax": 1400, "JenisAbu": "Bituminous", "SI": 2268.8, "Slagging": "Low",
            "C": 61.28, "H": 4.02, "N": 0.92, "O": 13.29 }
    daftar coalproperties digunakan sebagai acuan dalam pembentukan obyek coal
    """
    coalproperties = ['pemasok', 'tm', 'ts', 'ash', 'idtreducing', 'sio2', 'al2o3', 'fe2o3', 'cao', 'mgo', 'na2o',
                      'k2o', \
                      'tio2', 'so3', 'htmax', 'jenisabu', 'si', 'slagging', 'c', 'h', 'n', 'o']

    def __init__(self, datacoal):
        jsondt = json.loads(datacoal)
        for key, value in jsondt.items():
            setattr(self, key, value)

    def check_for_blending(self):
        atribut = [ "Pemasok", "Kategori", "Kalori", "TM", "TS", "ASH", "IDTReducing", \
                    "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                    "HTmax", "JenisAbu", "SI","Slagging", "C", "H", "N", "O", "statusalat" ]

    """
    get coal properties in json format
    """

    def jsoninlongformat(self):

        return {
            'Pemasok': self.Pemasok,
            'Kategori': self.Kategori,
            'Kalori': self.Kalori,
            'TM': self.TM,
            'TS': self.TS,
            'ASH': self.ASH,
            'IDTReducing': self.IDTReducing,
            'SiO2': self.SiO2,
            'Al2O3': self.Al2O3,
            'Fe2O3': self.Fe2O3,
            'CaO': self.CaO,
            'MgO': self.MgO,
            'Na2O': self.Na2O,
            'K2O': self.K2O,
            'TiO2': self.TiO2,
            'SO3': self.SO3,
            'HTmax': self.HTmax,
            'JenisAbu': self.JenisAbu,
            'SI': self.SI,
            'Slagging': self.Slagging,
            'C': self.C,
            'H': self.H,
            'N': self.N,
            'O': self.O,
            'statusalat': self.statusalat
        }

    """
        get coal properties in json format
        """

    def jsonforblendingformat(self):
        return {
            'Kalori': self.Kalori,
            'TM': self.TM,
            'TS': self.TS,
            'ASH': self.ASH,
            'IDTReducing': self.IDTReducing,
            'SiO2': self.SiO2,
            'Al2O3': self.Al2O3,
            'Fe2O3': self.Fe2O3,
            'CaO': self.CaO,
            'MgO': self.MgO,
            'Na2O': self.Na2O,
            'K2O': self.K2O,
            'TiO2': self.TiO2,
            'SO3': self.SO3,
            'HTmax': self.HTmax,
            'SI': self.SI,
            'C': self.C,
            'H': self.H,
            'N': self.N,
            'O': self.O,
        }

    """
    get coal in json in short format
    it is used in coal blending calculation
    """

    def jsoninshortformat(self):
        short = {
            'Pemasok': self.Pemasok,
            'Kategori': self.Kategori,
            'Kalori': self.Kalori,
            'TM': self.TM,
            'TS': self.TS,
            'ASH': self.ASH,
        }
        # print (short)
        return short



class Blending:
    """
    konstruktor kosong
    """
    def __init__(self):
        pass

    """
    load data for blending
    """
    def load_data_from_json_file(self, file_path):
        # f = open('../data/data_siap_blending.json')
        coallist = []
        f = open(file_path)
        coal_data = json.load(f)
        for data_item in coal_data:
            c = Coal(data_item)
            coallist.append(c)
        f.close()
        return coallist


    """
    split coal menjadi mrc, lrc dan biomass

    """

    def split_coal_by_category(self, coallist: [Coal], kalor_threshold):
        MRC = []
        LRC = []
        Biomass = []
        for coal in coallist:
            if coal.statusalat == 1:
                if coal.Kategori == 'batubara':
                    if coal.Kalori < kalor_threshold:
                        # LRC.append(coal.jsoninshortformat())
                        LRC.append(coal.jsoninlongformat())
                        # LRC.append(coal)
                    else:
                        # MRC.append(coal.jsoninshortformat())
                        MRC.append(coal.jsoninlongformat())
                        # MRC.append(coal)
                elif coal.Kategori == 'biomass':
                    Biomass.append(coal.jsoninlongformat())
        return MRC, LRC, Biomass

    """
            split coal by tag category
         """

    def split_coal_by_tag_category(self, coallist: [Coal]):
        TMRC = []
        TLRC = []
        CMRC =[]
        CLRC = []
        Biomass = []
        for coal in coallist:
            if coal.statusalat != 0:
                if (coal.Kategori).lower() == 'biomass' or (coal.Kategori).lower() == 'biomassa':
                    Biomass.append(coal.jsoninlongformat())
                elif (coal.sumberpasokan).lower() == 'coalyard':
                    if (coal.Kategori).lower() == 'batubara lrc':
                        CLRC.append(coal.jsoninlongformat())
                    else:
                        CMRC.append(coal.jsoninlongformat())
                elif (coal.sumberpasokan).lower() == 'tongkang':
                    if (coal.Kategori).lower() == 'batubara lrc':
                        TLRC.append(coal.jsoninlongformat())
                    else:
                        TMRC.append(coal.jsoninlongformat())
        return TMRC, TLRC, CMRC, CLRC, Biomass

    """
    listofcoaltojson
    """

    def json_rep_of_coal(self, XRC):
        new_rep_xrc = []
        for coal in XRC:
            new_rep_xrc.append(coal.jsoninshortformat())

    """

    """
    """
    select coal from coal list to blend using ga
    input: 
        n_pop: jumlah populasi
        laju_mutasi
        tar
    """

    def blend_using_ga(self, target_kalor, MRC, LRC, n_pop=1000, laju_mutasi=0.6):
        # new_rep_mrc = self.json_rep_of_coal(MRC)
        # new_rep_lrc = self.json_rep_of_coal(LRC)
        model_ga = GA()
        # cromosom = ga.ga(n_pop, laju_mutasi, target_kalor, new_rep_mrc, new_rep_lrc)
        cromosom = model_ga.ga(n_pop, laju_mutasi, target_kalor, MRC, LRC)
        # return yang diharapkan adalah coal hasil blending
        coal1 = LRC[cromosom[1]]
        coal1_prosentase = cromosom[0]
        coal2 = MRC[cromosom[7]]
        coal2_prosentase = cromosom[6]
        # cb = CoalBlending(coal1,coal2,coal1_prosentase,coal2_prosentase)
        return coal1, coal2, coal1_prosentase, coal2_prosentase






    """
    bending dengan gacofiring
    """

    def blend_using_gacofiring(self, target_kalor, MRC, LRC, biomassa, persen_biomass, n_pop=1000, laju_mutasi=0.6,
                               iterasi=100):
        # new_rep_mrc = self.json_rep_of_coal(MRC)
        # new_rep_lrc = self.json_rep_of_coal(LRC)
        model_ga = GACofiring()
        # cromosom = ga.ga(n_pop, laju_mutasi, target_kalor, new_rep_mrc, new_rep_lrc)
        cromosom = model_ga.ga_cofiring(n_pop, iterasi, laju_mutasi, target_kalor, MRC, LRC, biomassa, persen_biomass)
        # return yang diharapkan adalah coal hasil blending
        print('cromosom hasil cofiring:')
        print_cromosom(cromosom)
        coal1 = LRC[cromosom[1]]
        coal1_prosentase = cromosom[0]
        coal2 = MRC[cromosom[7]]
        coal2_prosentase = cromosom[6]
        #biomass = biomassa[int(cromosom[17])]
        biomass = biomassa[0]
        # persen_biomass = persen_biomass
        # cb = CoalBlending(coal1,coal2,coal1_prosentase,coal2_prosentase)
        return coal1, coal2, biomass, coal1_prosentase, coal2_prosentase, persen_biomass


    """
    status 11
    """
    def coal_stock_status(self,TMRC, TLRC,CMRC, CLRC, biomassa):
        status = [0,0,0,0,0]
        if len(TMRC) > 0:
            status[0] = 1
        if len (TLRC) > 0:
            status[1]=1
        if len(CMRC) > 0:
            status[2] =1
        if len (CLRC) > 0:
            status[3]=1
        if len(biomassa) > 0:
            status[4]=1
        return status

    def calculate_blending_update(self, target_kalor, TMRC, TLRC,CMRC, CLRC, biomass, persen_biomass,
                           n_pop=1000, laju_mutasi=0.6,iterasi=100):
        status = self.coal_stock_status(TMRC, TLRC, CMRC, CLRC, biomass)

        MRC = []
        LRC = []
        biomassa = []
        statusblending = 'nonblending'
        coal1 = None
        coal2 = None

        coal1_prosentase = 0
        coal2_prosentase = 0
        statusmrc =0
        statuslrc=0
        statusbiomassa =0

        if status[0]==1:
            MRC = TMRC
            statusmrc =1
        elif status[0]==0 and status[2]==1:
            MRC = CMRC
            statusmrc = 1
        if status[1]==1:
            LRC = TLRC
            statuslrc = 1
        elif status[1]==0 and status[3]==1:
            LRC = CLRC
            statuslrc = 1
        if status[4]==1:
            biomassa = biomass
            statusbiomassa = 1

        if statusbiomassa ==1 and statusmrc ==1 and statuslrc ==1 and persen_biomass>0:
            coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass = \
                self.blend_using_gacofiring(target_kalor, MRC, LRC, biomassa, persen_biomass)
            statusblending = 'cofiring'

        elif statusmrc ==1 and statuslrc ==1 and persen_biomass == 0:
            coal1, coal2,  coal1_prosentase, coal2_prosentase = \
                self.blend_using_ga(target_kalor, MRC, LRC)
            print(f'blending using ga,{coal1_prosentase}:{coal2_prosentase}')
            biomassa = None
            persen_biomass = 0
            statusblending = 'coalblending'
        return statusblending, coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass

    def calculate_blending(self,target_kalor, TMRC, TLRC,CMRC, CLRC, biomassa, persen_biomass,
                           n_pop=1000, laju_mutasi=0.6,iterasi=100):
        status = self.coal_stock_status(TMRC,TLRC,CMRC,CLRC,biomassa)
        statusblending = False
        if status [0] == status [1]==status[4]==1:
            coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass = \
                self.blend_using_gacofiring(target_kalor, TMRC, TLRC, biomassa, persen_biomass)
            statusblending = True
        elif status[0]==status[3]==status[4]==1:
            coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass = \
                self.blend_using_gacofiring(target_kalor, MRC=TMRC, LRC=CLRC, biomassa=biomassa, persen_biomass=persen_biomass)
            statusblending = True
        elif status[1]==status[2]==status[4]==1:
            coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass = \
                self.blend_using_gacofiring(target_kalor, LRC=TLRC, MRC=CMRC, biomassa=biomassa, persen_biomass=persen_biomass)
            statusblending = True
        elif status[2]==status[3]==status[4]==1:
            coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass = \
                self.blend_using_gacofiring(target_kalor, MRC=CMRC, LRC=TLRC, biomassa=biomassa, persen_biomass=persen_biomass)
            statusblending = True

        else:
            coal1=coal2=biomassa= None
            coal1_prosentase = coal2_prosentase = persen_biomass = 0


        return statusblending, coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass


class CoalBlending:
    """
    :parameter blending:
            Komposisi, Nilai Kalor, Total Moisture, Total Sulfur, Ash Content,
            Potensi slagging, Excess Air, AFR, MOT, Tilting burner,


    """

    damperlist = ['damper1AA', 'damper2AA', 'damper3AA', 'damper4AA',
                  'damper1AB', 'damper2AB', 'damper3AB', 'damper4AB',
                  'damper1CD', 'damper2CD', 'damper3CD', 'damper4CD',
                  'damper1EF', 'damper2EF', 'damper3EF', 'damper4EF',
                  'damper1FF', 'damper2FF', 'damper3FF', 'damper4FF',]

    def __init__(self, coal1: Coal, coal2: Coal, x1, x2,unitsetting: ParameterBlending):
        self.coal1 = coal1
        self.coal2 = coal2
        self.komposisicoal1 = x1
        self.komposisicoal2 = x2
        self.unitsetting = unitsetting
        self.calculate_blending_properties()

    """
    
    """

    def coalblendinginlongformat(self):
        return {
            'Kategori': 'coal blending',
            'Komposisic1': self.komposisicoal1,
            'Komposisic2': self.komposisicoal2,
            'Kalori': self.Kalori,
            'TM': self.TM,
            'TS': self.TS,
            'ASH': self.ASH,
            'IDTReducing': self.IDTReducing,
            'SiO2': self.SiO2,
            'Al2O3': self.Al2O3,
            'Fe2O3': self.Fe2O3,
            'CaO': self.CaO,
            'MgO': self.MgO,
            'Na2O': self.Na2O,
            'K2O': self.K2O,
            'TiO2': self.TiO2,
            'SO3': self.SO3,
            'HTmax': self.HTmax,
            'JenisAbu': self.JenisAbu,
            'SI': self.SI,
            'Slagging': self.Slagging,
            'C': self.C,
            'H': self.H,
            'N': self.N,
            'O': self.O,
            'AFR': self.AFR,
            'ExcessAir':self.ExcessAir,
            'MOT':self.MOT,
            'Tilting': self.Tilting,
            'damper1AA': self.damper1AA,
            'damper2AA': self.damper2AA,
            'damper3AA': self.damper3AA,
            'damper4AA': self.damper4AA,
            'damper1AB': self.damper1AB,
            'damper2AB': self.damper2AB,
            'damper3AB':self.damper3AB,
            'damper4AB': self.damper4AB,
            'damper1CD': self.damper1CD,
            'damper2CD': self.damper2CD,
            'damper3CD': self.damper3CD,
            'damper4CD': self.damper4CD,
            'damper1EF': self.damper1EF,
            'damper2EF': self.damper2EF,
            'damper3EF':self.damper3EF,
            'damper4EF': self.damper4EF


        }
    """
    """
    def __str__(self):
        longformat = self.coalblendinginlongformat()
        [print(key, ':', value) for key, value in longformat.items()]

    """
        apa yang dimaksud AH
        bagaimana nilai AH? apakah konstan atau ditentukan oleh karakteristik tertentu?
        """
    def define_ash_type(self):
        if (self.CaO + self.MgO) < self.Fe2O3:
            jenisAbu = "bituminous"
        else:
            jenisAbu = "lignite"
        setattr(self,'JenisAbu',jenisAbu)

    def calculate_slagging_index(self):
        if self.JenisAbu == "bituminous":
            devisor = self.SiO2 + self.Al2O3 + self.TiO2 + self.TS
            if devisor != 0:
                slagging_index = (self.CaO + self.MgO + self.Fe2O3 + self.Na2O + self.K2O) / devisor
            else:
                slagging_index = None
                #raise ZeroDivisionError("Devisor in slagging index calculation cann't be zero")

        else:
            slagging_index = (((self.HTmax * 9 / 5) + 32) + 4 * ((self.IDTReducing * 9 / 5) + 32)) / 5
        setattr(self,'SI',slagging_index)


    def define_slagging_category(self):
        if self.JenisAbu == "Bituminous":
            if self.SI < 0.6:
                slagging = "low"
            elif self.SI < 2:
                slagging = "medium"
            else:
                slagging = "high"
        else:
            if self.SI < 2100:
                slagging = "severe"
            elif self.SI < 2250:
                slagging = "high"
            elif self.SI < 2450:
                slagging = "medium"
            else:
                slagging = "low"
        setattr(self, 'Slagging', slagging)

    def calculate_excess_air_and_afr(self):
        air_theory = 0.01 * (11.51 * self.C + 4.31 * self.TS + 3.43 * self.H - 4.32 * self.O)
        moles_theory = air_theory / 28.966
        moles_dry = self.C/100/12.011+self.TS/100/32.066+self.N/100/28.013
        #moles_dry = 0.12011 * self.C + 0.32066 * self.TS + 0.28013 * self.N
        devisor = moles_theory * (20.95 - self.unitsetting.AH)
        if devisor != 0:
            excess_air = 100 * (self.unitsetting.AH * (moles_dry + 0.7905 * moles_theory) / devisor)
            afr = (1 + excess_air / 100) * air_theory
        else:
            excess_air = None
            afr = None
            #raise ZeroDivisionError("Devisor in excess air can;t be zero")

        #excess_air = 100 * self.unitsetting.AH * (moles_dry + 0.7905 * moles_theory) / devisor

        setattr(self, 'ExcessAir', excess_air)
        setattr(self, 'AFR', afr)

    def calculate_MOT(self):
        tm = self.TM
        if tm < 30:
            MOT = 56
        elif tm < 32:
            MOT = 58
        elif tm < 34:
            MOT = 60
        else:
            MOT = 62
        setattr(self, 'MOT', MOT)

    """
        definition of vm is still confuse. what is the meaning of vm?
    """

    def calculate_tilting(self):
        vm = self.unitsetting.VM
        if vm <= 26:
            tilting = -50
        elif vm <= 28:
            tilting = 50
        elif vm <= 30:
            tilting = 25
        elif vm <= 32:
            tilting = 0
        else:
            tilting = -25
        key = 'Tilting'
        setattr(self, key, tilting)

    def calculate_damper_value(self):
        cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA',\
                      'corner1AB', 'corner2AB', 'corner3AB', 'corner4AB',\
                      'corner1CD', 'corner2CD', 'corner3CD', 'corner4CD',\
                      'corner1EF', 'corner2EF', 'corner3EF', 'corner4EF',\
                      'corner1FF', 'corner2FF', 'corner3FF', 'corner4FF', ]

        nkunit = [int(x) for x in (self.unitsetting.nk_unit).split(sep=',')]
        corner =[]
        corner.append(list([float(x) for x in (self.unitsetting.corner1AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4CD).split(sep=',')]))
        corner.append(list( [float(x) for x in (self.unitsetting.corner1EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4FF).split(sep=',')]))
        for i in range(len(corner)):
            key = cornerlist[i]
            damper_key = 'damper' + key[-3:]
            interpvalue = interp(self.Kalori, nkunit, corner[i])
            setattr(self, damper_key, interpvalue)


    def calculate_blending_properties(self):
        blending_attribute = ["Kalori", "TM", "TS", "ASH", "IDTReducing", \
                   "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                   "HTmax", "SI",  "C", "H", "N", "O", ]
        #data_coal1 = self.coal1.jsonforblendingformat()
        #data_coal2 = self.coal2.jsonforblendingformat()
        data_coal1 = self.coal1
        data_coal2 = self.coal2
        for key, val in data_coal1.items():
            if key in blending_attribute:
                blend_value = self.komposisicoal1 * data_coal1[key] + self.komposisicoal2 * data_coal2[key]
                setattr(self, key, blend_value)

        self.define_ash_type()
        self.calculate_tilting()
        self.calculate_slagging_index()
        self.define_slagging_category()
        self.calculate_excess_air_and_afr()
        self.calculate_MOT()
        self.calculate_damper_value()

    def cbinjasonformat(self):
        return {
            'Kalori': self.Kalori,
            'TM': self.TM,
            'TS': self.TS,
            'ASH': self.ASH,
            'IDTReducing': self.IDTReducing,
            'SiO2': self.SiO2,
            'Al2O3': self.Al2O3,
            'Fe2O3': self.Fe2O3,
            'CaO': self.CaO,
            'MgO': self.MgO,
            'Na2O': self.Na2O,
            'K2O': self.K2O,
            'TiO2': self.TiO2,
            'SO3': self.SO3,
            'HTmax': self.HTmax,
            'JenisAbu': self.JenisAbu,
            'SI': self.SI,
            'Slagging': self.Slagging,
            'C': self.C,
            'H': self.H,
            'N': self.N,
            'O': self.O,
            'Tilting': self.Tilting,
            'MOT': self.MOT,
            'ExcessAir': self.ExcessAir,
            'AFR': self.AFR,
            'MOT': self.MOT
        }

    def __str__(self):
        cbinjson = self.cbinjasonformat()
        return json.dumps(cbinjson)


class UnitBoiler:
    """
    corner : pasangan key value corner_number, list(value)
    kalor: list kalor
    corner: dictionary
    cornerlist =['corner1AA','corner2AA','corner3AA','corner4AA',
                 'corner1AB','corner2AB','corner3AB','corner4AB',
                 'corner1CD','corner2CD','corner3CD','corner4CD',
                 'corner1EF','corner2EF','corner3EF','corner4EF',]

    """
    cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA', ]

    damperlist = ['damper1AA', 'damper2AA', 'damper3AA', 'damper4AA',
                  'damper1AB', 'damper2AB', 'damper3AB', 'damper4AB',
                  'damper1CD', 'damper2CD', 'damper3CD', 'damper4CD',
                  'damper1EF', 'damper2EF', 'damper3EF', 'damper4EF', ]

    def __init__(self, kalor, corner):
        self.kalor_unit = kalor
        for key, value in corner.items():
            if self.cornerlist.count(key) > 0:
                setattr(self, key, value)

    def get_attrs(self):
        return [k for k in self.__dict__.keys()
                if not k.startswith('__')
                and not k.endswith('__')]


class CoFiring(CoalBlending):


    """
    :parameter blending:
            Komposisi, Nilai Kalor, Total Moisture, Total Sulfur, Ash Content,
            Potensi slagging, Excess Air, AFR, MOT, Tilting burner,


    """
    cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA',
                  'corner1AB', 'corner2AB', 'corner3AB', 'corner4AB',
                  'corner1CD', 'corner2CD', 'corner3CD', 'corner4CD',
                  'corner1EF', 'corner2EF', 'corner3EF', 'corner4EF', ]

    def __init__(self, coal1: Coal, coal2: Coal, biomass, persen_c1, persen_c2, persen_b,unitspec:ParameterBlending):
        super(CoFiring,self).__init__(coal1, coal2, persen_c1, persen_c2,unitspec)
        self.biomass = biomass
        self.komposisibiomass = persen_b

        self.calculate_cofiring_properties()

    def set_cornerattribute(self):
        corner = self.unitsetting.corner



    """
        apa yang dimaksud AH
        bagaimana nilai AH? apakah konstan atau ditentukan oleh karakteristik tertentu?
        """

    def calculate_cofiring_properties(self):
        cofiring_attribute = ["Kalori", "TM", "TS", "ASH", "IDTReducing", \
                              "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                              "HTmax", "SI", "C", "H", "N", "O", ]
        #data_coal1 = self.coal1.jsonforblendingformat()
        data_coal1 = self.coal1
        #data_coal2 = self.coal2.jsonforblendingformat()
        data_coal2 = self.coal2
        #data_biomass = self.biomass.jsonforblendingformat()
        data_biomass = self.biomass
        #print(f' tipe data biomass: {type(data_biomass)}')

        for key in data_coal1:
            if key in cofiring_attribute:
                blend_value = self.komposisicoal1 * data_coal1.get(key)+ self.komposisicoal2 * data_coal2.get(key) + (self.komposisibiomass * data_biomass.get(key))/100
                setattr(self, key, blend_value)
                #print(f'{key}: {data_coal2.get(key)}' )
        super().define_ash_type()
        super().calculate_tilting()
        super().calculate_slagging_index()
        super().define_slagging_category()
        super().calculate_excess_air_and_afr()
        super().calculate_MOT()
        super().calculate_damper_value()

    def cofiringinjsonformat(self):
        return {
                'Kategori': 'cofiring',
                'Komposisic1': self.komposisicoal1,
                'Komposisic2': self.komposisicoal2,
                'Komposisibio': self.komposisibiomass,
                'Kalori': self.Kalori,
                'TM': self.TM,
                'TS': self.TS,
                'ASH': self.ASH,
                'IDTReducing': self.IDTReducing,
                'SiO2': self.SiO2,
                'Al2O3': self.Al2O3,
                'Fe2O3': self.Fe2O3,
                'CaO': self.CaO,
                'MgO': self.MgO,
                'Na2O': self.Na2O,
                'K2O': self.K2O,
                'TiO2': self.TiO2,
                'SO3': self.SO3,
                'HTmax': self.HTmax,
                'JenisAbu': self.JenisAbu,
                'SI': self.SI,
                'Slagging': self.Slagging,
                'C': self.C,
                'H': self.H,
                'N': self.N,
                'O': self.O,
                'AFR': self.AFR,
                'ExcessAir': self.ExcessAir,
                'MOT': self.MOT,
                'Tilting': self.Tilting,
                'damper1AA': self.damper1AA,
                'damper2AA': self.damper2AA,
                'damper3AA': self.damper3AA,
                'damper4AA': self.damper4AA,
                'damper1AB': self.damper1AB,
                'damper2AB': self.damper2AB,
                'damper3AB': self.damper3AB,
                'damper4AB': self.damper4AB,
                'damper1CD': self.damper1CD,
                'damper2CD': self.damper2CD,
                'damper3CD': self.damper3CD,
                'damper4CD': self.damper4CD,
                'damper1EF': self.damper1EF,
                'damper2EF': self.damper2EF,
                'damper3EF': self.damper3EF,
                'damper4EF': self.damper4EF

            }

    def __str__(self):
        cbinjson = self.cbinjasonformat()
        return json.dumps(cbinjson)


class CofiringWithoutGA:
    def __init__(self,coal1: Coal, biomass, persen_b,unitspec:ParameterBlending):
        self.coal1 = coal1
        self.komposisicoal1 = (100 -persen_b)/100

        self.komposisibiomass = persen_b/100
        self.biomass = biomass
        self.unitsetting = unitspec
        self.calculate_cofiring_properties()

    def calculate_cofiring_properties(self):
        cofiring_attribute = ["Kalori", "TM", "TS", "ASH", "IDTReducing", \
                              "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "Na2O", "K2O", "TiO2", "SO3", \
                              "HTmax", "SI", "C", "H", "N", "O", ]
        #data_coal1 = self.coal1.jsonforblendingformat()
        data_coal1 = self.coal1
        #data_biomass = self.biomass.jsonforblendingformat()

        data_biomass = self.biomass
        #print(f' tipe data biomass: {type(data_biomass)}')
        if self.komposisibiomass == 0:
            # hitung cofiring tanpa biomass
            for key in cofiring_attribute:
                blend_value = getattr(data_coal1,key)
                setattr(self, key, blend_value)
            setattr(self,"biomass",None)

        else:
            for key in cofiring_attribute:
                blend_value = self.komposisicoal1 * getattr(data_coal1,key) + self.komposisibiomass * getattr(data_biomass, key)
                setattr(self, key, blend_value)
                    #print(f'{key}: {data_coal1.get(key)}' )
        self.define_ash_type()
        self.calculate_tilting()
        self.calculate_slagging_index()
        self.define_slagging_category()
        self.calculate_excess_air_and_afr()
        self.calculate_MOT()
        self.calculate_damper_value()

    def define_ash_type(self):
        if (self.CaO + self.MgO) < self.Fe2O3:
            jenisAbu = "bituminous"
        else:
            jenisAbu = "lignite"
        setattr(self,'JenisAbu',jenisAbu)

    def calculate_slagging_index(self):
        if self.JenisAbu == "bituminous":
            devisor = self.SiO2 + self.Al2O3 + self.TiO2 + self.TS
            if devisor != 0:
                slagging_index = (self.CaO + self.MgO + self.Fe2O3 + self.Na2O + self.K2O) / devisor
            else:
                slagging_index = None
                #raise ZeroDivisionError("Devisor in slagging index calculation cann't be zero")

        else:
            slagging_index = (((self.HTmax * 9 / 5) + 32) + 4 * ((self.IDTReducing * 9 / 5) + 32)) / 5
        setattr(self,'SI',slagging_index)


    def define_slagging_category(self):
        if self.JenisAbu == "Bituminous":
            if self.SI < 0.6:
                slagging = "low"
            elif self.SI < 2:
                slagging = "medium"
            else:
                slagging = "high"
        else:
            if self.SI < 2100:
                slagging = "severe"
            elif self.SI < 2250:
                slagging = "high"
            elif self.SI < 2450:
                slagging = "medium"
            else:
                slagging = "low"
        setattr(self, 'Slagging', slagging)

    def calculate_excess_air_and_afr(self):
        air_theory = 0.01 * (11.51 * self.C + 4.31 * self.TS + 3.43 * self.H - 4.32 * self.O)
        moles_theory = air_theory / 28.966
        moles_dry = self.C/100/12.011+self.TS/100/32.066+self.N/100/28.013
        #moles_dry = 0.12011 * self.C + 0.32066 * self.TS + 0.28013 * self.N
        devisor = moles_theory * (20.95 - self.unitsetting.AH)
        if devisor != 0:
            excess_air = 100 * (self.unitsetting.AH * (moles_dry + 0.7905 * moles_theory) / devisor)
            afr = (1 + excess_air / 100) * air_theory
        else:
            excess_air = None
            afr = None
            #raise ZeroDivisionError("Devisor in excess air can;t be zero")

        #excess_air = 100 * self.unitsetting.AH * (moles_dry + 0.7905 * moles_theory) / devisor

        setattr(self, 'ExcessAir', excess_air)
        setattr(self, 'AFR', afr)

    def calculate_MOT(self):
        tm = self.TM
        if tm < 30:
            MOT = 56
        elif tm < 32:
            MOT = 58
        elif tm < 34:
            MOT = 60
        else:
            MOT = 62
        setattr(self, 'MOT', MOT)

    """
        definition of vm is still confuse. what is the meaning of vm?
    """

    def calculate_tilting(self):
        vm = self.unitsetting.VM
        if vm <= 26:
            tilting = -50
        elif vm <= 28:
            tilting = 50
        elif vm <= 30:
            tilting = 25
        elif vm <= 32:
            tilting = 0
        else:
            tilting = -25
        key = 'Tilting'
        setattr(self, key, tilting)

    def calculate_damper_value(self):
        cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA',\
                      'corner1AB', 'corner2AB', 'corner3AB', 'corner4AB',\
                      'corner1CD', 'corner2CD', 'corner3CD', 'corner4CD',\
                      'corner1EF', 'corner2EF', 'corner3EF', 'corner4EF',\
                      'corner1FF', 'corner2FF', 'corner3FF', 'corner4FF', ]

        nkunit = [int(x) for x in (self.unitsetting.nk_unit).split(sep=',')]
        corner =[]
        corner.append(list([float(x) for x in (self.unitsetting.corner1AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4AA).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4AB).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3CD).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4CD).split(sep=',')]))
        corner.append(list( [float(x) for x in (self.unitsetting.corner1EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4EF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner1FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner2FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner3FF).split(sep=',')]))
        corner.append(list([float(x) for x in (self.unitsetting.corner4FF).split(sep=',')]))
        for i in range(len(corner)):
            key = cornerlist[i]
            damper_key = 'damper' + key[-3:]
            interpvalue = interp(self.Kalori, nkunit, corner[i])
            setattr(self, damper_key, interpvalue)



class BlendingHistories:
    def __init__(self,bou:BlendingOnUnit):
        self.waktu_pengisian = bou.tanggal
        self.operator = bou.user
        self.pemasok1 = self.get_pemasok_from_coal_data(bou.coal1)
        self.pemasok2 = self.get_pemasok_from_coal_data(bou.coal2)
        self.komposisic1 = self.get_komposisic1(bou.cofiring)
        self.komposisic2 = self.get_komposisic2(bou.cofiring)
        self.nilaikalor = self.get_kalori(bou.cofiring)
        self.afr = self.get_afr(bou.cofiring)
        self.kategori = self.get_kategori(bou.cofiring)
        if self.kategori == 'cofiring':
            self.komposisibio = self.get_komposisibio(bou.cofiring)
            self.pemasokbio = self.get_pemasok_from_coal_data(bou.biomass)
            
    def get_pemasok_from_coal_data(self,data_coal):
        coal = Coal(data_coal)
        return coal.Pemasok

    def get_komposisic1(self,data_coal_blending):
        """
        'Kategori': 'coal blending',
            'Komposisic1': self.komposisicoal1,
            'Komposisic2': self.komposisicoal2,
        """
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("Komposisic1")
    
    def get_komposisic2(self,data_coal_blending):
        """
        'Kategori': 'coal blending',
            'Komposisic1': self.komposisicoal1,
            'Komposisic2': self.komposisicoal2,
        """
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("Komposisic2")
    
    def get_komposisibio(self, data_coal_blending):
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("Komposisibio")

    def get_kalori(self,data_coal_blending):
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("Kalori")

    def get_kategori(self,data_coal_blending):
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("Kategori")


    def get_afr(self, data_coal_blending):
        jsondtcb = json.loads(data_coal_blending)
        return jsondtcb.get("AFR")


        
        

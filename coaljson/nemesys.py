import json
from .ga import GA
from .ga_cofiring import GACofiring
from numpy import interp



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

        #jsondt = json.loads(datacoal)
        for key, value in datacoal.items():
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

    def __str__(self):
        longformat = self.jsoninlongformat()
        [print(key, ':', value) for key, value in longformat.items()]


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
        MRC = []
        LRC = []
        Biomass = []
        for coal in coallist:
            if coal.statusalat != 0:
                if coal.Kategori.lower() == 'biomass':
                    Biomass.append(coal.jsoninlongformat())
                elif coal.Kategori.lower() == 'batubara lrc':
                    LRC.append(coal.jsoninlongformat())
                else:
                    MRC.append(coal.jsoninlongformat())
        return MRC, LRC, Biomass

    """
    listofcoaltojson
    """

    def json_rep_of_coal(self, XRC):
        new_rep_xrc = []
        for coal in XRC:
            new_rep_xrc.append(coal.jsoninshortformat())


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
        coal1 = LRC[cromosom[1]]
        coal1_prosentase = cromosom[0]
        coal2 = MRC[cromosom[7]]
        coal2_prosentase = cromosom[6]
        # biomass = biomassa
        # persen_biomass = persen_biomass
        # cb = CoalBlending(coal1,coal2,coal1_prosentase,coal2_prosentase)
        return coal1, coal2, biomassa, coal1_prosentase, coal2_prosentase, persen_biomass




class CoalBlending:
    """
    :parameter blending:
            Komposisi, Nilai Kalor, Total Moisture, Total Sulfur, Ash Content,
            Potensi slagging, Excess Air, AFR, MOT, Tilting burner,


    """
    AH = 2.91

    def __init__(self, coal1: Coal, coal2: Coal, x1, x2):
        self.coal1 = coal1
        self.coal2 = coal2
        self.komposisicoal1 = x1
        self.komposisicoal2 = x2
        self.calculate_blending_properties()

    """
        apa yang dimaksud AH
        bagaimana nilai AH? apakah konstan atau ditentukan oleh karakteristik tertentu?
        """

    def define_ash_type(self):
        if (self.CaO + self.MgO) < self.Fe2O3:
            self.JenisAbu = "bituminous"
        else:
            self.JenisAbu = "lignite"

    def calculate_slagging_index(self):
        if self.JenisAbu == "bituminous":
            devisor = self.SiO2 + self.Al2O3 + self.TiO2 + self.TS
            if devisor == 0:
                raise ZeroDivisionError("Devisor in slagging index calculation cann't be zero")
            self.SI = (self.CaO + self.MgO + self.Fe2O3 + self.Na2O + self.K2O) / devisor
        else:
            self.slagging_index = (((self.HTmax * 9 / 5) + 32) + 4 * ((self.IDTReducing * 9 / 5) + 32)) / 5

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
        moles_dry = 0.12011 * self.C + 0.32066 * self.TS + 0.28013 * self.N
        devisor = moles_theory * (20.95 - CoalBlending.AH)
        if devisor == 0:
            raise ZeroDivisionError("Devisor in excess air can;t be zero")
        excess_air = 100 * CoalBlending.AH * (moles_dry + 0.7905 * moles_theory) / devisor
        afr = (1 + 0.01 * excess_air) * air_theory
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

    def calculate_tilting(self, vm):
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

    def calculate_blending_properties(self):
        data_coal1 = self.coal1.jsonforblendingformat()
        data_coal2 = self.coal2.jsonforblendingformat()
        for key, val in data_coal1.items():
            blend_value = self.komposisicoal1 * data_coal1[key] + self.komposisicoal2 * data_coal2[key]
            setattr(self, key, blend_value)
        self.define_ash_type()
        self.calculate_tilting(30)
        self.calculate_slagging_index()
        self.define_slagging_category()
        self.calculate_excess_air_and_afr()
        self.calculate_MOT()

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
    cornerlist = ['corner1AA', 'corner2AA', 'corner3AA', 'corner4AA',
                  'corner1AB', 'corner2AB', 'corner3AB', 'corner4AB',
                  'corner1CD', 'corner2CD', 'corner3CD', 'corner4CD',
                  'corner1EF', 'corner2EF', 'corner3EF', 'corner4EF', ]


    damperlist = ['damper1AA', 'damper2AA', 'damper3AA', 'damper4AA',
                  'damper1AB', 'damper2AB', 'damper3AB', 'damper4AB',
                  'damper1CD', 'damper2CD', 'damper3CD', 'damper4CD',
                  'damper1EF', 'damper2EF', 'damper3EF', 'damper4EF', ]

    def __init__(self, kalor, corner):
        self.kalor_unit = kalor
        for key, value in corner.items():
            if self.cornerlist.count(key) > 0:
                setattr(self, key, value)

    def calculate_damper_value(self, kalor_rekomendasi):
        if len(self.kalor_unit) == 0:
            raise AttributeError("parameter kalor unit belum diset")
        # hitung nilai bukaan damper dengan fungsi spline untuk setiap corner yang bersesuaian
        for key in self.cornerlist:
            damper_key = 'damper' + key[-3:]
            corner = getattr(self, key)
            if len(corner) != 0:
                interpvalue = interp(kalor_rekomendasi, self.kalor_unit, corner)
                setattr(self, damper_key, interpvalue)


class CoFiring(CoalBlending):
    """
    :parameter blending:
            Komposisi, Nilai Kalor, Total Moisture, Total Sulfur, Ash Content,
            Potensi slagging, Excess Air, AFR, MOT, Tilting burner,


    """

    def __init__(self, coal1: Coal, coal2: Coal, biomass, persen_c1, persen_c2, persen_b):
        super().__init__(coal1, coal2, persen_c1, persen_c2)
        self.biomass = biomass
        self.komposisibiomass = persen_b
        self.calculate_cofiring_properties()

    """
        apa yang dimaksud AH
        bagaimana nilai AH? apakah konstan atau ditentukan oleh karakteristik tertentu?
        """

    def calculate_cofiring_properties(self):
        data_coal1 = self.coal1.jsonforblendingformat()
        data_coal2 = self.coal2.jsonforblendingformat()
        data_biomass = self.biomass.jsonforblendingformat()
        for key, val in data_coal1.items():
            blend_value = self.komposisicoal1 * data_coal1[key] + self.komposisicoal2 * data_coal2[
                key] + self.komposisibiomass * data_biomass[key]
            setattr(self, key, blend_value)
        super().define_ash_type()
        super().calculate_tilting(30)
        super().calculate_slagging_index()
        super().define_slagging_category()
        super().calculate_excess_air_and_afr()
        super().calculate_MOT()


    def cofiringinjasonformat(self):
        return {
            'Kalori': self.Kalori,
            'Kategori': "cofiring",
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
        }

    def __str__(self):
        cbinjson = self.cbinjasonformat()
        return json.dumps(cbinjson)


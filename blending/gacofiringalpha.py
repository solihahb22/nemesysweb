from .nemesys import Coal
import numpy as np
import copy
import datetime



class GACofiringAlpha:
    def __init__(self):
        pass

    def get_coal_opposite_category(tongkang: Coal, coal_list):
        kategori = tongkang.kategori;
        coalyard = [coal for coal in enumerate(coal_list) if coal.Kategori != kategori]
        return coalyard

    def define_jenis_abu(coal1: Coal, coal2: Coal, persen_coal1, persen_coal2):
        # CaO MgO Fe2O3 Na2O K2O SiO2 Al2O3 TiO2 TS IDTReducing HTmax
        CaO_mix = persen_coal1 * coal1.CaO + persen_coal2 * coal2.CaO
        MgO_mix = persen_coal1 * coal1.MgO + persen_coal2 * coal2.MgO
        Fe2O3_mix = persen_coal1 * coal1.Fe2O3 + persen_coal2 * coal2.Fe2O3
        if CaO_mix + MgO_mix < Fe2O3_mix:
            jenis_abu = 'Bituminous'
            Na2O_mix = persen_coal1 * coal1.Na2O + persen_coal2 * coal2.Na2O
            K2O_mix = persen_coal1 * coal1.K2O + persen_coal2 * coal2.K2O
            SiO2_mix = persen_coal1 * coal1.SiO2 + persen_coal2 * coal2.SiO2
            Al2O3_mix = persen_coal1 * coal1.Al2O3 + persen_coal2 * coal2.Al2O3
            TiO2_mix = persen_coal1 * coal1.TiO2 + persen_coal2 * coal2.TiO2
            TS_mix = persen_coal1 * coal1.TS + persen_coal2 * coal2.TS
            slagging_index = (CaO_mix + MgO_mix + Fe2O3_mix + Na2O_mix + K2O_mix) / (
                        SiO2_mix + Al2O3_mix + TiO2_mix + TS_mix)
            if slagging_index < 0.6:
                slagging = 'low'
            elif slagging_index < 2:
                slagging = 'medium'
            else:
                slagging = 'high'
        else:
            jenis_abu = 'Lignite'
            IDTReducing_mix = persen_coal1 * coal1.IDTReducing + persen_coal2 * coal2.IDTReducing
            HTmax_mix = persen_coal1 * coal1.HTmax + persen_coal2 * coal2.HTmax
            slagging_index = (((HTmax_mix * 9 / 5) + 32) + 4 * ((IDTReducing_mix * 9 / 5) + 32)) / 5
            if slagging_index < 2100:
                slagging = 'severe';
            elif slagging_index < 2250:
                slagging = 'high';
            elif slagging_index < 2450:
                slagging = 'medium';
            else:
                slagging = 'low';
        return jenis_abu, slagging_index, slagging

    # normalisasi tm, ash, ts tergantung kepada kondisi di masing masing unit sehingga perlu di lakukan pengaturan ulang
    def set_fitness(self, cromosom, tongkang, coalyard, target_kalor, tm_max=34.68, ash_max=5.82, ts_max=0.36):
        # fitnes mempertimbangkan ketercapaian target_kalor
        # meminimalkan jarak target_kalor ke target_kalor di cromosom
        # normalisasi ke 0 ... 1
        # norm_x = (x - xmin)/(xmax - xmin)

        norm_deviasi_kalor = (abs(cromosom[0] - target_kalor) / target_kalor) / 0.02
        # slagging index : low, medium, high, severe
        # encode slagging : severe = 3; high = 2; medium=1; low =0
        # norm_es = (slagging-low)/3

        jenis_abu, slagging_index, slagging = self.define_jenis_abu(tongkang, coalyard[cromosom[1]],
                                                               persen_coal1=cromosom[2], persen_coal2=cromosom[3])
        num_slagging = 0
        if slagging == "severe":
            num_slagging = 3
        elif slagging == "high":
            num_slagging = 2
        elif slagging == "medium":
            num_slagging = 1
        else:
            num_slagging = 0
        norm_encode_slagging = (num_slagging) / 3
        # normalisasi sisa pembakaran berdasarkan data didalam database
        # contoh pada JPR:
        # {min_tm: 0.00; max_tm: 34.68; min_ash: 0.00; max_as: 5.82; min_ts: 0.00; max_ts: 0.36
        norm_tm = (tongkang.TM * cromosom[2] + coalyard[cromosom[1]].TM * cromosom[3]) / tm_max
        norm_ash = (tongkang.ASH * cromosom[2] + coalyard[cromosom[1]].ASH * cromosom[3]) / ash_max
        norm_ts = (tongkang.TS * cromosom[2] + coalyard[cromosom[1]].TS * cromosom[3]) / ts_max
        rerata = (norm_deviasi_kalor + norm_encode_slagging + norm_tm + norm_ash + norm_ts) / 5
        # print(f'dev_k: {norm_deviasi_kalor}, sl: {norm_encode_slagging},tm: {norm_tm}, ash: {norm_ash}, ts: {norm_ts}')
        return (1 - rerata)

    def hitung_komposisi(kalor_tongkang, kalor_coalyard, kalor_bio, persen_bio, kalor_target):
        k = kalor_target - kalor_tongkang + persen_bio * (kalor_tongkang - kalor_bio)
        b = k / (kalor_coalyard - kalor_tongkang)
        a = 1 - b - persen_bio
        target = a * kalor_tongkang + b * kalor_coalyard + persen_bio * kalor_bio
        # print (f'{a}*{kalor_tongkang} + {b}*{kalor_coalyard} + {persen_bio}*{kalor_bio}= {target}')
        return a, b

    def create_cromosom(self, target_kalor_in_range, target_kalor, tongkang, coalyard, id_coalyard, biomass,
                        persen_biomass=1):
        #cromosom[0]: target_kalor_in_range
        #cromosom[1]: id coal pada list coalyard
        #cromosom[2]: proporsi coal tongkang
        #cromosom[3]: proporsi coal di coalyard
        #cromosom[4]: proporsi biomass (dlm persen)
        cromosom = [0, 0, 0, 0, 0, 0]
        cromosom[0] = target_kalor_in_range
        cromosom[1] = id_coalyard
        a, b = self.hitung_komposisi(tongkang.Kalori, coalyard[cromosom[1]].Kalori, biomass.Kalori, persen_biomass,
                                cromosom[0])
        cromosom[2] = a  # proporsi tongkang
        cromosom[3] = b  # proporsi coalyard
        cromosom[4] = persen_biomass
        cromosom[5] = self.set_fitness(cromosom, tongkang, coalyard, target_kalor)
        # print(cromosom)
        return cromosom

    def best_cromosom_update(best_cromosom, cromosom):
        if len(best_cromosom) == 0:
            best_cromosom.append(cromosom)
        else:
            idx_best = [i for i, v in enumerate(best_cromosom) if v[1] == cromosom[1]]
            # print(f'idx_best: {idx_best}')
            if len(idx_best) == 0:
                best_cromosom.append(cromosom)
            else:
                for i, val in enumerate(idx_best):
                    # print(f'i: {i} val: {val}')
                    if (best_cromosom[val][1] == cromosom[1]) and (best_cromosom[val][5] < cromosom[5]):
                        best_cromosom[val] = cromosom
                        break

    def create_population(self,target_kalor, tongkang, coalyard, biomass, persen_biomass, total_pop):
        # populasi target_kalor_in_range dibuat terdistribusi normal
        min_val_kalor_target = 0.98 * target_kalor
        max_val_kalor_target = 1.02 * target_kalor
        list_coal_id = np.random.randint(low=0, high=len(coalyard), size=total_pop)
        # best_cromosom diisi dengan cromosom terbaik dari setiap kombinasi tongkang dgn coal di coalyard
        best_cromosom = []
        pop = []
        for i in range(total_pop):
            target_kalor_in_range = np.random.randint(min_val_kalor_target, max_val_kalor_target + 1)
            coalyard_coal_id = list_coal_id[i]
            cromosom = self.create_cromosom(target_kalor_in_range, target_kalor, tongkang, coalyard, coalyard_coal_id,
                                       biomass, persen_biomass)
            self.best_cromosom_update(best_cromosom, cromosom)
            pop.append(cromosom)
        return pop, best_cromosom

    # pada proses mutasi yang dimungkinkan untuk berubah adalah bagian target kalor dan bagian coal di coalyard
    def mutate(self, cromosom, laju_mutasi, target_kalor, tongkang, coalyard, biomass, persen_biomass):
        newcromosom = copy.deepcopy(cromosom)
        flag_mutation = np.random.rand() <= laju_mutasi

        if flag_mutation:
            # yang berubah adalah cromosom 0
            min_val_target = 0.98 * target_kalor
            max_val_target = 1.02 * target_kalor
            newcromosom[0] = np.random.randint(min_val_target, max_val_target + 1)
            # cromosom yang berubah adalah 2: 3: 5:
            a, b = self.hitung_komposisi(tongkang.Kalori, coalyard[cromosom[1]].Kalori, biomass.Kalori, persen_biomass,
                                    cromosom[0])
            newcromosom[2] = a
            newcromosom[3] = b
        else:
            # yang berubah adalah cromosom 1 : coal pada coalyard
            newcromosom[1] = np.random.randint(len(coalyard))
            a, b = self.hitung_komposisi(tongkang.Kalori, coalyard[cromosom[1]].Kalori, biomass.Kalori, persen_biomass,
                                    cromosom[0])
            newcromosom[2] = a
            newcromosom[3] = b
        newcromosom[5] = self.set_fitness(newcromosom, tongkang, coalyard, target_kalor)
        return newcromosom

    def get_idx_fitness_min(pop):
        fitness = [c[5] for c in pop]
        min_fitness = min(fitness)
        idx_min_fitness = [i for i, x in enumerate(fitness) if x == min_fitness]
        return idx_min_fitness[0]

    def regeneration(self, children, pop, best_cromosom):
        for i, val in enumerate(children):
            idx_min_fitness = self.get_idx_fitness_min(pop)
            if pop[idx_min_fitness][5] < val[5]:
                pop[idx_min_fitness] = copy.deepcopy(val)
                self.best_cromosom_update(best_cromosom, pop[idx_min_fitness])
            # print(f'pop replaced at idx:{idx_min_fitness}')

    # https://stackoverflow.com/questions/24719368/syntaxerror-non-default-argument-follows-default-argument
    # def ga_cofiring(n_pop, iter=30, laju_mutasi,target_kalor, tongkang,coalyard, biomassa, persen_biomassa): urutan seperti ini tidak diijinkan di python
    def ga_cofiring(self,  target_kalor, tongkang, coalyard, biomassa, persen_biomassa,n_pop=1000, laju_mutasi=0.6, iter=30):
        pop, best_cromosom = self.create_population(target_kalor, tongkang, coalyard, biomassa, persen_biomassa, n_pop)
        #idx_min_fitness = self.get_idx_fitness_min(pop)
        # print(f'idx_min_fitness:{idx_min_fitness}')
        # iter = 10
        for i in range(iter):
            q = np.random.permutation(n_pop)
            # print(q)
            parent_1 = pop[q[0]]
            parent_2 = pop[q[1]]
            # print('parent')
            # print_cromosom(parent_1)
            # print_cromosom(parent_2)
            child_1, child_2 = self.crossover(parent_1, parent_2, tongkang, coalyard, biomassa, persen_biomassa, target_kalor)
            # mutasi
            # print('cromosom crossover')
            # print_cromosom(child_1)
            # print_cromosom(child_2)
            mutan_c1 = self.mutate(child_1, laju_mutasi, target_kalor, tongkang, coalyard, persen_biomassa)
            mutan_c2 = self.mutate(child_2, laju_mutasi, target_kalor, tongkang, coalyard, persen_biomassa)
            children = [mutan_c1, mutan_c2]
            # regenerasi
            self.regeneration(children, pop, best_cromosom)
        sorted_best_cromosom = self.sort_best_cromosom(best_cromosom,coalyard)
        return best_cromosom

    def sort_best_cromosom(best_cromosom, coalyard):
        # cromosom[1]: id coal pada list coalyard
        # buat list id_best_cromosom [idx 0] dan tanggal pada coalyard [idx 1]
        list_bc=[]
        for id, val in enumerate(best_cromosom):
            coal = coalyard[best_cromosom[id][1]]
            tanggal = coal.__getattribute__('tanggal')
            list = [id, tanggal]
            list_bc.append(list)
        # urutkan list
        sorter = sorted(list_bc, key=lambda t: datetime.datetime.strptime(t[1], '%d/%m/%Y'))
        sorted_best_cromosom = [x for _, x in sorted(zip(sorter, best_cromosom))]
        return sorted_best_cromosom


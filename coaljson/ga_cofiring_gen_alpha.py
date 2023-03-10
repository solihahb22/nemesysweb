import numpy as np
import os
import json
import copy
import random
from .nemesys import Coal



def print_cromosom(cromosom):
    print(f'cromosom: {cromosom[0]},{cromosom[1]},{cromosom[2]},{cromosom[3]},\
                    {cromosom[4]},{cromosom[5]},{cromosom[6]},{cromosom[7]},{cromosom[8]},\
                    {cromosom[9]},{cromosom[10]},{cromosom[11]}, {cromosom[12]},\
                    {cromosom[13]},{cromosom[14]},{cromosom[15]}, {cromosom[16]} ')

def cromosom_to_str(cromosom):
    cromosom_str = f'cromosom: {cromosom[0]},{cromosom[1]},{cromosom[2]},{cromosom[3]},\
                    {cromosom[4]},{cromosom[5]},{cromosom[6]},{cromosom[7]},{cromosom[8]},\
                    {cromosom[9]},{cromosom[10]},{cromosom[11]}, {cromosom[12]},\
                    {cromosom[13]},{cromosom[14]},{cromosom[15]}, {cromosom[16]} '
    return cromosom_str

class GACofiringAlpha:
    def __init__(self):
        pass

    def set_fitnes(self,cromosom, persen_biomassa):
        #update fungsi fitness
        # sisa pembakaran dan slagging indekx harus minimum
        # normalisasi nilai sisa pembakaran ke [0..1] dilakukan berdasarkan data coal yang tersedia
        # slagging indeks dinormalisasi ke [0 ..1]

        #old version
        kalor_blending = cromosom[0] * cromosom[2] + cromosom[6] * cromosom[8] + cromosom[12] * persen_biomassa/100
        sisa_pembakaran = cromosom[0] * (cromosom[3] + cromosom[4] + cromosom[5]) \
                          + cromosom[6] * (cromosom[9] + cromosom[10] + cromosom[11])\
                            + persen_biomassa*(cromosom[13] + cromosom[14] + cromosom[15])
        if sisa_pembakaran != 0:
            fitnes = kalor_blending / sisa_pembakaran
        else:
            fitnes = 0
        # print(f'fitnes:{fitnes}')

        return fitnes

    def create_population(self,target_kalor,Tongkang,Coalyard,biomass, persen_biomass,total_pop):
        # untuk jumlah total populasi yang diinginkan
        # pembuatan populasi maka komposisi dari coal di tongkang dibuat terdistribusi normal
        # untuk setiap coal di coalyard dipasangkan dengan coal_tongkang dengan prosentase menyesuaikan sehingga total = 100% - %biomassa


        #old version
        #print('create populasi')
        if len(Tongkang)==len(Coalyard)==0:
            raise Exception ('Tongkang dan Coalyard tidak boleh kosong')
        #kalor dari biomas 1 persen
        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0]
        best_cromosom = cromosom
        pop=[]
        for i in range(total_pop):
            if len(MRC)==0:
                MRC = LRC
            elif len(LRC)==0:
                LRC = MRC
            #cromosom = self.create_cromosom_from_coal(target_kalor, MRC,LRC)
            cromosom = self.create_cromosom_from_coal(target_kalor,MRC,LRC,biomass,persen_biomass)
            if best_cromosom[16]<cromosom[16]:
                best_cromosom = copy.deepcopy(cromosom)
            pop.append(cromosom)
            #print_cromosom(cromosom)
            #print(f'{cromosom[0]}: {cromosom[2]}, {cromosom[6]}:{cromosom[8]}, fitness={cromosom[16]}')
            #print(f'fitness best cromosom: {best_cromosom[16]}')
        return pop, best_cromosom

    def ga_cofiring(self, n_pop, iter,laju_mutasi,target_kalor, tongkang,coalyard, biomassa, persen_biomassa):
        pop, best_cromosom = self.create_population(target_kalor,MRC,LRC,biomassa,persen_biomassa,n_pop)

        idx_min_fitness = self.get_idx_fitness_min(pop)
        #print(f'idx_min_fitness:{idx_min_fitness}')
        #iter = 10
        for i in range(iter):
            q = np.random.permutation(n_pop)
            # print(q)
            #print(f'fitness best cromosom iterasi ke {i}: {best_cromosom[16]}')
            #print_cromosom(best_cromosom)
            parent_1 = pop[q[0]]
            parent_2 = pop[q[1]]
            #print('parent')
            #print_cromosom(parent_1)
            #print_cromosom(parent_2)
            child_1, child_2 = self.crossover(parent_1, parent_2,persen_biomassa)
            # mutasi
            #print('cromosom crossover')
            #print_cromosom(child_1)
            #print_cromosom(child_2)
            mutan_c1 = self.mutate(child_1, laju_mutasi,target_kalor,persen_biomassa)
            mutan_c2 = self.mutate(child_2, laju_mutasi,target_kalor,persen_biomassa)
            children = [mutan_c1, mutan_c2]
            # regenerasi
            pop, new_best_cromosom = self.regeneration(children, pop, best_cromosom)
            # terminasi
            #if (new_best_cromosom != []):
            best_cromosom = new_best_cromosom
            #print(best_cromosom[16])
            #print(f'fitness best cromosom iterasi ke {i}: {best_cromosom[16]}')
        #print_cromosom(best_cromosom)
            print(f'{best_cromosom[0]}: {best_cromosom[2]}, {best_cromosom[6]}:{best_cromosom[8]}, fitness={best_cromosom[16]}')
        return best_cromosom

    def regeneration(self, children,pop,best_cromosom):
        new_best_cromosom = []
        for i in range(len(children)):
            idx_min_fitness = self.get_idx_fitness_min(pop)
            pop[idx_min_fitness]=[]
            pop[idx_min_fitness]=copy.deepcopy(children[i])
            new_fitness = pop[idx_min_fitness][16]
            if best_cromosom[16] < new_fitness:
                #new_best_cromosom=copy.deepcopy(pop[idx_min_fitness])
                best_cromosom = pop[idx_min_fitness]
        #print(f'pop replaced at idx:{idx_min_fitness}')
        #print(f'fitnes: {pop[idx_min_fitness][16]}')
        return pop, best_cromosom

    def mutate(self, cromosom,laju_mutasi,target_kalor,persen_biomass):
        newcromosom = copy.deepcopy(cromosom)
        flag_mutation = np.random.rand() <= laju_mutasi
        target_kalor_baru = target_kalor - cromosom[12] * persen_biomass/100
        if flag_mutation:
            #yang berubah adalah cromosom 0
            newcromosom[0] =  random.uniform(0.1, 0.8)
            newcromosom[6] = (target_kalor_baru - newcromosom[0] * newcromosom[2]) / newcromosom[8]
        else:
            # yang berubah adalah cromosom 6
            #newcromosom[6] = np.random.randint(0, 50)/100
            newcromosom[6] =  random.uniform(0.1, 0.8)
            newcromosom[0] = (target_kalor_baru - newcromosom[6] * newcromosom[8]) / newcromosom[2]
        newcromosom[16]= self.set_fitnes(newcromosom,persen_biomass)

        #print('cromosom mutasi:')
        #print_cromosom(newcromosom)
        #print(f'{cromosom[0]}: {cromosom[2]}, {cromosom[6]}:{cromosom[8]}, fitness={cromosom[16]}')
        return newcromosom

    def get_fitness(self, cromosom):
        return cromosom[16]

    def get_idx_fitness_min(self,pop):
        fitness= [c[16] for c in pop ]
        min_fitness = min(fitness)
        idx_min_fitness = [i for i, x in enumerate(fitness) if x==min_fitness]
        return idx_min_fitness[0]

    def crossover(self,parent1, parent2,persen_biomass):
        #cross over --> parent1 dan parent 2

        #old version
        #print(f'parent1: {parent1}')
        #print(f'parent2:{parent2}')
        child_1_l = self.get_part1_of_cromosom(parent1)
        child_1 = child_1_l+ self.get_part2_of_cromosom(parent2)
        child_1 = child_1 + self.get_part3_of_cromosom(parent1)
        #print(f'child1:{child_1}')
        child_1.append(self.set_fitnes(child_1,persen_biomass))
        child_2_l = self.get_part1_of_cromosom(parent2)
        child_2 = child_2_l+ self.get_part2_of_cromosom(parent1)
        child_2 = child_2 + self.get_part3_of_cromosom(parent2)
        child_2.append(self.set_fitnes(child_2,persen_biomass))
        return child_1, child_2

    def get_part1_of_cromosom(self,cromosom):
        copy_cromosom = copy.deepcopy(cromosom[:6])
        #print(f'panjang sub cromosom kiri:{copy_cromosom}')
        return copy_cromosom

    def get_part2_of_cromosom(self,cromosom):
        copy_cromosom = copy.deepcopy(cromosom[6:12])
        #print(f'panjang sub cromosom kanan:{copy_cromosom}')
        return copy_cromosom

    def get_part3_of_cromosom(self,cromosom):
        copy_cromosom = copy.deepcopy(cromosom[12:16])
        #print(f'panjang sub cromosom kanan:{copy_cromosom}')
        return copy_cromosom




    def define_jenis_abu(coal1: Coal, coal2: Coal, persen_coal1, persen_coal2):
        # CaO MgO Fe2O3 Na2O K2O SiO2 Al2O3 TiO2 TS IDTReducing HTmax
        CaO_mix = persen_coal1* coal1.CaO + persen_coal2* coal2.CaO
        MgO_mix = persen_coal1* coal1.MgO + persen_coal2* coal2.MgO
        Fe2O3_mix = persen_coal1* coal1.Fe2O3 + persen_coal2* coal2.Fe2O3
        if CaO_mix + MgO_mix < Fe2O3_mix :
            jenis_abu = 'Bituminous'
            Na2O_mix = persen_coal1 * coal1.Na2O + persen_coal2 * coal2.Na2O
            K2O_mix = persen_coal1 * coal1.K2O + persen_coal2 * coal2.K2O
            SiO2_mix = persen_coal1 * coal1.SiO2 + persen_coal2 * coal2.SiO2
            Al2O3_mix = persen_coal1 * coal1.Al2O3 + persen_coal2 * coal2.Al2O3
            TiO2_mix = persen_coal1 * coal1.TiO2 + persen_coal2 * coal2.TiO2
            TS_mix = persen_coal1 * coal1.TS + persen_coal2 * coal2.TS
            slagging_index = (CaO_mix + MgO_mix + Fe2O3_mix + Na2O_mix + K2O_mix)/(SiO2_mix + Al2O3_mix + TiO2_mix + TS_mix)
            if slagging_index < 0.6 :
                slagging = 'Low'
            elif slagging_index < 2 :
                slagging = 'Medium'
            else :
                slagging = 'High'
        else:
            jenis_abu = 'Lignite'
            IDTReducing_mix = persen_coal1* coal1.IDTReducing + persen_coal2* coal2.IDTReducing
            HTmax_mix = persen_coal1* coal1.HTmax + persen_coal2* coal2.HTmax
            slagging_index = (((HTmax_mix*9/5)+32)+4*((IDTReducing_mix*9/5)+32))/5
            if slagging_index < 2100 :
                slagging = 'Severe';
            elif slagging_index < 2250:
                slagging = 'High';
            elif slagging_index < 2450:
                slagging = 'Medium';
            else :
                slagging = 'Low';
        return jenis_abu, slagging_index, slagging

    def hitung_komposisi(kalor_tongkang, kalor_coalyard, kalor_bio, persen_bio, kalor_target):
        k = kalor_target - kalor_tongkang + persen_bio * (kalor_tongkang - kalor_bio)
        b = k / (kalor_coalyard - kalor_tongkang)
        a = 1 - b - persen_bio
        target = a * kalor_tongkang + b * kalor_coalyard + persen_bio * kalor_bio
        #print(f'{a}*{kalor_tongkang} + {b}*{kalor_coalyard} + {persen_bio}*{kalor_bio}= {target}')
        return a, b

    def create_cromosom_from_coal(self, target_kalor, coal_tongkang, coalyard_id,coal_coalyard, biomass, persen_biomass=1):
        # bag 1: coal tongkang, bag 2: coal coalyard, bag 3: biomass
        # prosentase biomass ditentukan diawal

        # perubahan desain cromosom
        # cromosom1: target kalor (dalam range nilai yang diijinkan) --> bisa diubah melalui mutasi
        # cromosom2: id_coal coalyard
        # cromosom3: persen kalor tongkang
        # cromosom4: persen kalor coalyard
        # cromosom5: persen biomassa
        # cromosom6: kalor tongkang
        # cromosom7: kalor coalyard

        # cross over hanya diijinkan ambil dari bagian belakang ditukar posisi (perlu dipikirkan komposisi dan nilai kalor)

        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0]
        #idx_tongkang hanya ada 1 coal di tongkang
        # coal di coalyard yang dimasukkan diatur di fungsi generate populasi, dimana setiap coal di coalyard adalah bagian dari populasi
        #persen_coal = 100 - persen_biomass

        cromosom[0] = random.uniform(0.3, 0.9) # persen kalori coal 1
        cromosom[1] = coal_tongkang.kalori
        # jumlahan kalori keduanya harus sama dengan target kalor

        #print(f'target_kalor_baru: {target_kalor_baru}')
        persen2 = (target_kalor - (persen_biomass/100)* biomass.kalori) - (target_kalor_baru - cromosom[0] * cromosom[1]) / MRC[idx_mrc]['Kalori']
        cromosom[1] = persen2
        cromosom[2] = coalyard_id
        cromosom[8] = coal_coalyard['Kalori']
        cromosom[9] = MRC[idx_mrc]['TM']
        cromosom[10] = MRC[idx_mrc]['TS']
        cromosom[11] = MRC[idx_mrc]['ASH']
        cromosom[12] = biomass['Kalori']
        cromosom[13] = biomass['TM']
        cromosom[14] = biomass['TS']
        cromosom[15] = biomass['ASH']
        cromosom[16] = self.set_fitnes(cromosom,persen_biomass)
        return cromosom


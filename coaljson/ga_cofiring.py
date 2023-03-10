import numpy as np
import os
import json
import copy
import random




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

class GACofiring:
    def __init__(self):
        pass

    def set_fitnes(self,cromosom, persen_biomassa):
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

    def create_population(self,target_kalor,MRC,LRC,biomass, persen_biomass,total_pop):
        #print('create populasi')
        if len(MRC)==len(LRC)==0:
            raise Exception ('MRC dan LRC tidak boleh kosong')
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

    def ga_cofiring(self, n_pop, iter,laju_mutasi,target_kalor, MRC,LRC, biomassa, persen_biomassa):
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
           # newcromosom[0] = np.random.randint(0, 90) / 100

            #newcromosom[0] = round(100*random.uniform(0.3,0.9))/100
            newcromosom[0] =  random.uniform(0.3, 0.9)
            newcromosom[6] = (target_kalor_baru - newcromosom[0] * newcromosom[2]) / newcromosom[8]
        else:
            # yang berubah adalah cromosom 6
            #newcromosom[6] = np.random.randint(0, 50)/100
            newcromosom[6] =  random.uniform(0.2, 0.5)
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


    def create_cromosom_from_coal(self, target_kalor, MRC,LRC,biomass, persen_biomass=1):
        # bag 1: coal 1, bag 2: coal 2, bag 3: biomass
        #prosentase biomass ditentukan diawal
        # persen yang diambil adalah persen total dikurangi persen biomass
        # target kalor = persen1* kalor1 + persen2*kalor2 + persen_biomass*kalorb/100
        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0]
        idx_mrc = np.random.randint(0, len(MRC))
        idx_lrc = np.random.randint(0, len(LRC))
        #persen_coal = 100 - persen_biomass
        # cromosom[0]= np.random.randint(0,90)/100
        cromosom[0] = random.uniform(0.3, 0.9)
        cromosom[1] = idx_lrc
        cromosom[2] = LRC[idx_lrc]['Kalori']
        cromosom[3] = LRC[idx_lrc]['TM']
        cromosom[4] = LRC[idx_lrc]['TS']
        cromosom[5] = LRC[idx_lrc]['ASH']
        # jumlahan kalori keduanya harus sama dengan target kalor
        target_kalor_baru = target_kalor - (persen_biomass/100)* biomass['Kalori']
        #print(f'target_kalor_baru: {target_kalor_baru}')
        persen2 = (target_kalor_baru - cromosom[0] * cromosom[2]) / MRC[idx_mrc]['Kalori']
        cromosom[6] = persen2
        cromosom[7] = idx_mrc
        cromosom[8] = MRC[idx_mrc]['Kalori']
        cromosom[9] = MRC[idx_mrc]['TM']
        cromosom[10] = MRC[idx_mrc]['TS']
        cromosom[11] = MRC[idx_mrc]['ASH']
        cromosom[12] = biomass['Kalori']
        cromosom[13] = biomass['TM']
        cromosom[14] = biomass['TS']
        cromosom[15] = biomass['ASH']
        cromosom[16] = self.set_fitnes(cromosom,persen_biomass)
        return cromosom


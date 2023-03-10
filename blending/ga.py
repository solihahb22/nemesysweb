import numpy as np
import os
import json
import copy
import random


def set_fitnes(cromosom):
    kalor_blending = cromosom[0] * cromosom[2] + cromosom[6] * cromosom[8]
    sisa_pembakaran = cromosom[0] * (cromosom[3] + cromosom[4] + cromosom[5]) \
                      + cromosom[6] * (cromosom[9] + cromosom[10] + cromosom[11])
    if sisa_pembakaran != 0:
        fitnes = kalor_blending / sisa_pembakaran
    else:
        fitnes = 0
    #print(f'fitnes:{fitnes}')

    return fitnes


def print_cromosom(cromosom):
    print( f'cromosom: {cromosom[0]},{cromosom[1]},{cromosom[2]},{cromosom[3]},{cromosom[4]},{cromosom[5]},{cromosom[6]},{cromosom[7]},{cromosom[8]},{cromosom[9]},{cromosom[10]},{cromosom[11]}, {cromosom[12]} ')

def cromosom_to_str(cromosom):
    cromosom_str = f'cromosom: {cromosom[0]},{cromosom[1]},{cromosom[2]},{cromosom[3]},{cromosom[4]},{cromosom[5]},{cromosom[6]},{cromosom[7]},{cromosom[8]},{cromosom[9]},{cromosom[10]},{cromosom[11]}, {cromosom[12]} '
    return cromosom_str

class GA:
    def __init__(self):
        pass

    def create_population(self,target_kalor,MRC,LRC,total_pop):
        if len(MRC)==len(LRC)==0:
            raise Exception ('MRC dan LRC tidak boleh kosong')
        #kalor dari biomas 1 persen
        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        best_cromosom = cromosom
        pop=[]
        for i in range(total_pop):
            if len(MRC)==0:
                MRC = LRC
            elif len(LRC)==0:
                LRC = MRC
            cromosom = self.create_cromosom_from_coal(target_kalor, MRC,LRC)
            if best_cromosom[12]<cromosom[12]:
                best_cromosom = copy.deepcopy(cromosom)
            pop.append(cromosom)
            #print_cromosom(cromosom)
            #print(f'{cromosom[0]}: {cromosom[2]}, {cromosom[6]}:{cromosom[8]}, fitness={cromosom[11]}')

        return pop, best_cromosom

    def ga(self, n_pop, laju_mutasi,target_kalor, MRC,LRC):
        pop, best_cromosom = self.create_population(target_kalor, MRC, LRC, n_pop)

        idx_min_fitness = self.get_idx_fitness_min(pop)
        #print(f'idx_min_fitness:{idx_min_fitness}')
        iter = 200
        for i in range(iter):
            q = np.random.permutation(n_pop)
            # print(q)
            #print(f'best cromosom iterasi ke {i}')
            #print_cromosom(best_cromosom)
            parent_1 = pop[q[0]]
            parent_2 = pop[q[1]]
            #print('parent')
            #print_cromosom(parent_1)
            #print_cromosom(parent_2)
            child_1, child_2 = self.crossover(parent_1, parent_2)
            # mutasi
            #print('cromosom crossover')
            #print_cromosom(child_1)
            #print_cromosom(child_2)
            mutan_c1 = self.mutate(child_1, laju_mutasi,target_kalor)
            mutan_c2 = self.mutate(child_2, laju_mutasi,target_kalor)
            children = [mutan_c1, mutan_c2]
            # regenerasi
            pop, new_best_cromosom = self.regeneration(children, pop, best_cromosom)
            # terminasi
            if (new_best_cromosom != []):
                best_cromosom = new_best_cromosom
        print_cromosom(best_cromosom)
        return best_cromosom

    def regeneration(self, children,pop,best_cromosom):
        new_best_cromosom = []
        for i in range(len(children)):
            idx_min_fitness = self.get_idx_fitness_min(pop)
            pop[idx_min_fitness]=[]
            pop[idx_min_fitness]=copy.deepcopy(children[i])
            new_fitness = pop[idx_min_fitness][12]
            if best_cromosom[12] < new_fitness:
                new_best_cromosom=copy.deepcopy(pop[idx_min_fitness])
            #print(f'pop replaced at idx:{idx_min_fitness}')
        return pop, new_best_cromosom

    def mutate(self, cromosom,laju_mutasi,target_kalor):
        newcromosom = copy.deepcopy(cromosom)
        flag_mutation = np.random.rand() <= laju_mutasi
        if flag_mutation:
            #yang berubah adalah cromosom 0
           # newcromosom[0] = np.random.randint(0, 90) / 100
            newcromosom[0] = round(100*random.uniform(0.3,0.9))/100
            newcromosom[6] = (round(100 * (target_kalor - cromosom[0] * cromosom[2]) / newcromosom[8])) / 100
        else:
            # yang berubah adalah cromosom 6
            #newcromosom[6] = np.random.randint(0, 50)/100
            newcromosom[6] = round(100 * random.uniform(0.2, 0.5)) / 100
            newcromosom[0] = (round(100 * (target_kalor - cromosom[6] * cromosom[8]) / newcromosom[2])) / 100
        newcromosom[12]= set_fitnes(newcromosom)

        #print('cromosom mutasi:')
        #print_cromosom(newcromosom)
        return newcromosom

    def get_fitness(self, cromosom):
        return cromosom[12]

    def get_idx_fitness_min(self,pop):
        fitness= [v[12] for v in pop ]
        min_fitness = min(fitness)
        idx_min_fitness = [i for i, x in enumerate(fitness) if x==min_fitness]
        return idx_min_fitness[0]

    def crossover(self,parent1, parent2):
        #print(f'parent1: {parent1}')
        #print(f'parent2:{parent2}')
        child_1_l = self.get_left_part_of_cromosom(parent1)
        child_1 = child_1_l+ self.get_right_part_of_cromosom(parent2)
        #print(f'child1:{child_1}')
        child_1.append(set_fitnes(child_1))
        child_2_l = self.get_left_part_of_cromosom(parent2)
        child_2 = child_2_l+ self.get_right_part_of_cromosom(parent1)
        child_2.append(set_fitnes(child_2))
        return child_1, child_2

    def get_left_part_of_cromosom(self,cromosom):
        copy_cromosom = copy.deepcopy(cromosom[:len(cromosom)//2])
        #print(f'panjang sub cromosom kiri:{copy_cromosom}')
        return copy_cromosom

    def get_right_part_of_cromosom(self,cromosom):
        copy_cromosom = copy.deepcopy(cromosom[len(cromosom)//2:len(cromosom)-1])
        #print(f'panjang sub cromosom kanan:{copy_cromosom}')
        return copy_cromosom
    def create_cromosom_from_MRC_LRC(self,target_kalor, MRC,LRC):
        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        idx_mrc = np.random.randint(0, len(MRC))
        idx_lrc = np.random.randint(0, len(LRC))
        # cromosom[0]= np.random.randint(0,90)/100
        cromosom[0] = round(100 * random.uniform(0.3, 0.9)) / 100
        cromosom[1] = LRC[idx_lrc].No
        cromosom[2] = LRC[idx_lrc].Kalori
        cromosom[3] = LRC[idx_lrc].TM
        cromosom[4] = LRC[idx_lrc].TS
        cromosom[5] = LRC[idx_lrc].ASH
        # jumlahan kalori keduanya harus sama dengan target kalor
        # target kalor = persen1* kalor1 + persen2*kalor2
        persen2 = (round(100 * (target_kalor - cromosom[0] * cromosom[2]) / MRC[idx_mrc].Kalori)) / 100
        cromosom[6] = persen2
        cromosom[7] = MRC[idx_mrc].No
        cromosom[8] = MRC[idx_mrc].Kalori
        cromosom[9] = MRC[idx_mrc].TM
        cromosom[10] = MRC[idx_mrc].TS
        cromosom[11] = MRC[idx_mrc].ASH
        cromosom[12] = set_fitnes(cromosom)
        return cromosom

    def create_cromosom_from_coal(self, target_kalor, MRC,LRC):
        cromosom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        idx_mrc = np.random.randint(0, len(MRC))
        idx_lrc = np.random.randint(0, len(LRC))
        # cromosom[0]= np.random.randint(0,90)/100
        cromosom[0] = round(100 * random.uniform(0.3, 0.9)) / 100
        cromosom[1] = idx_lrc
        cromosom[2] = LRC[idx_lrc]['Kalori']
        cromosom[3] = LRC[idx_lrc]['TM']
        cromosom[4] = LRC[idx_lrc]['TS']
        cromosom[5] = LRC[idx_lrc]['ASH']
        # jumlahan kalori keduanya harus sama dengan target kalor
        # target kalor = persen1* kalor1 + persen2*kalor2
        #target = 4400
        # lrc didapatkan kalor 0.5*4200 = 2100
        #mrc = 4400-2100 = 2300 dari 4500
        persen2 = (round(100 * (target_kalor - cromosom[0] * cromosom[2]) / MRC[idx_mrc]['Kalori'])) / 100
        cromosom[6] = persen2
        cromosom[7] = idx_mrc
        cromosom[8] = MRC[idx_mrc]['Kalori']
        cromosom[9] = MRC[idx_mrc]['TM']
        cromosom[10] = MRC[idx_mrc]['TS']
        cromosom[11] = MRC[idx_mrc]['ASH']
        cromosom[12] = set_fitnes(cromosom)
        return cromosom


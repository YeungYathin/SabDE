from input import getData
import numpy as np
import heapq
import sys
import random
import time
import copy
import statistics

f = None

class Main:

    # Basic attribute of the UFLP problem
    m = None
    n = None
    f = None
    c = None

    population_size = None
    LP = None
    generation = None
    fk = None
    crk = None
    pk = None
    goal_generation = 250
    individual_list = None
    best_individual = None
    value_list = None
    time_start = None
    epsilon = None
    chaotic_var = None
    Fki_success_heap = None # 与下面的东西配合来使用，是一个堆，存着近LP次里面成功的Fki
    Fki_success_list = None # 里面有6个数组对应每一个strategy，每一个大数组里面有有LP个小数组，存着近LP次里面成功的Fki
    CRki_success_heap = None # 与下面的东西配合来使用，是一个堆，存着近LP次里面成功的CRki
    CRki_success_list = None # 里面有6个数组对应每一个strategy，每一个大数组里面有有LP个小数组，存着近LP次里面成功的CRki
    strategy_list = None
    strategy_success_num_list = None

    def __init__(self, goal_generation = 250, epsilon = 0.0000000000000000000000001):
        Main.population_size = Main.m
        Main.LP = Main.population_size
        Main.goal_generation = goal_generation
        Main.epsilon = epsilon
        
    def SabDE(self):
        self.initialize()
        self.update_best_individual()
        while Main.generation < Main.goal_generation:
            print(Main.pk)
            print(f'{Main.generation} {Main.best_individual.value} {np.mean(Main.value_list)} {np.var(Main.value_list)} {time.time() - Main.time_start}')
            print(f'{Main.generation} {Main.best_individual.value} {np.mean(Main.value_list)} {np.var(Main.value_list)} {time.time() - Main.time_start}', file=f)
            if Main.generation > Main.LP:
                for k in range(0, 6):
                    # Update pk 
                    strategy_success_num_sum = sum([sum(arr) for arr in Main.strategy_success_num_list])
                    Main.pk[k] = sum(Main.strategy_success_num_list[k])/strategy_success_num_sum
                    if len(Main.Fki_success_heap[k]) != 0:
                        Main.fk[k] = statistics.median(Main.Fki_success_heap[k])
                    else:
                        Main.fk[k] = random.random() * 0.9 + 0.1
                    if len(Main.CRki_success_heap[k]) != 0:
                        Main.crk[k] = statistics.median(Main.CRki_success_heap[k])
                    else:
                        Main.crk[k] = random.random() * 0.9 + 0.1
            max_p = max(Main.pk)
            min_indexes = [i for i, val in enumerate(Main.pk) if val == max_p]
            strategy_index = random.choice(min_indexes)
            print(strategy_index)
            print(Main.Fki_success_list)
            self.generate_Fki_CRki(strategy_index=strategy_index)
            for j in range(0, Main.population_size):
                Main.strategy_list[strategy_index](Main.individual_list[j])
                self.crossover(Main.individual_list[j])
            self.greedy_selection(strategy_index=strategy_index)
            Main.generation += 1
        return Main.best_individual.vector, Main.best_individual.value

    def initialize(self):
        Main.time_start = time.time()
        Main.generation = 0
        Main.individual_list = []
        Main.value_list = []
        Main.fk = []
        Main.crk = []
        Main.pk = []
        Main.Fki_success_heap = []
        Main.Fki_success_list = []
        Main.CRki_success_heap = []
        Main.CRki_success_list = []
        Main.strategy_success_num_list = []
        for i in range(6):
            Main.strategy_success_num_list.append(np.zeros(Main.LP))
        
        for index in range(6):
            Main.fk.append(random.random() * 0.9 + 0.1) # Choose fk from (0.1,1)
            Main.crk.append(0.5)
            Main.pk.append(1/6)
            
            median_heap_1 = []
            Main.Fki_success_heap.append(median_heap_1)
            big_array_Fki = [[] for _ in range(Main.LP)]
            Main.Fki_success_list.append(big_array_Fki)
            
            median_heap_2 = []
            Main.CRki_success_heap.append(median_heap_2)
            big_array_CRki = [[] for _ in range(Main.LP)]
            Main.CRki_success_list.append(big_array_CRki)
        for j in range(0, Main.population_size):
            initial_individual = individual()
            Main.individual_list.append(initial_individual)
            Main.value_list.append(initial_individual.value)
        Main.strategy_list = [strategy_1, strategy_2, strategy_3, strategy_4, strategy_5, strategy_6]
        
    def update_best_individual(self):
        temp = individual()
        temp.value = sys.maxsize
        for ind in Main.individual_list:
            if ind.value < temp.value:
                temp = ind
        Main.best_individual = temp
        
    def generate_Fki_CRki(self, strategy_index):
        if Main.chaotic_var is None:
            exclude = [0.25, 0.5, 0.75]
            Main.chaotic_var = 0
            while Main.chaotic_var in exclude or Main.chaotic_var == 0:
                Main.chaotic_var = random.random()
        for j in range(0, Main.population_size):
            Main.chaotic_var = 4*Main.chaotic_var*(1-Main.chaotic_var)
            Main.individual_list[j].Fki = Main.fk[strategy_index]+0.2*(Main.chaotic_var-0.5)
            # print(Main.c)
            while Main.individual_list[j].Fki > 1.5 or Main.individual_list[j].Fki < 0:
                Main.chaotic_var = 4*Main.chaotic_var*(1-Main.chaotic_var)
                Main.individual_list[j].Fki = Main.fk[strategy_index]+0.2*(Main.chaotic_var-0.5)
        for j in range(0, Main.population_size):
            Main.chaotic_var = 4*Main.chaotic_var*(1-Main.chaotic_var)
            Main.individual_list[j].CRki = Main.fk[strategy_index]+0.1*(Main.chaotic_var-0.5)
            while Main.individual_list[j].CRki > 1 or Main.individual_list[j].CRki < 0:
                Main.chaotic_var = 4*Main.chaotic_var*(1-Main.chaotic_var)
                Main.individual_list[j].CRki = Main.fk[strategy_index]+0.1*(Main.chaotic_var-0.5)
    
    def crossover(self, ind):
        rand_num = random.randint(0, Main.m-1)
        ui = ind.vector
        for k in range(Main.m):
            if random.random() < ind.CRki or k == rand_num:
                ui[k] = ind.vi[k]
        ind.ui = ui

    def greedy_selection(self, strategy_index):
        Main.value_list = []
        Main.strategy_success_num_list[strategy_index][Main.generation%Main.LP] = 0

        # 把前LP代的记录删掉
        Fki_del_list = copy.deepcopy(Main.Fki_success_list[strategy_index][Main.generation%Main.LP])
        CRki_del_list = copy.deepcopy(Main.CRki_success_list[strategy_index][Main.generation%Main.LP])
        
        Main.Fki_success_list[strategy_index][Main.generation%Main.LP] = []
        Main.CRki_success_list[strategy_index][Main.generation%Main.LP] = []
        for i in range(len(Fki_del_list)):
            Main.Fki_success_heap[strategy_index].remove(Fki_del_list[i])
            Main.CRki_success_heap[strategy_index].remove(CRki_del_list[i])
        
        for j in range(Main.population_size):
            ind:individual = Main.individual_list[j]
            if self.calculate_value(ind.ui) < ind.value:
                ind.vector = ind.ui
                ind.calculate_value()
                Main.Fki_success_heap[strategy_index].append(ind.Fki)
                Main.Fki_success_list[strategy_index][Main.generation%Main.LP].append(ind.Fki)
                Main.CRki_success_heap[strategy_index].append(ind.CRki)
                Main.CRki_success_list[strategy_index][Main.generation%Main.LP].append(ind.CRki)
                Main.strategy_success_num_list[strategy_index][Main.generation%Main.LP]+=1
            if ind.value < Main.best_individual.value: # Update Best
                Main.best_individual = ind
            Main.value_list.append(ind.value)
    
    def calculate_value(self, vector):
        result = 0
        
        # Calculate the opening cost
        result += np.inner(vector, Main.f)
        
        # Calculate the facility-customer cost
        for i in range(0, Main.n):
            temp = int(sys.maxsize)
            for j in range(0, Main.m):
                if vector[j] and Main.c[i][j] < temp:
                    temp = Main.c[i][j]
            result += temp
        return result
            
    def test(self):  # This is just a test for correctness verify
        print(Main.m, Main.n, Main.f, Main.c)

class individual:
    
    def __init__(self):
        self.vector = np.random.randint(0, 2, Main.m)
        self.value = None
        self.calculate_value()
        self.vi = None
        self.ui = None
        self.Fki = None
        self.CRki = None
        
    def calculate_value(self):
        result = 0
        
        # Calculate the opening cost
        result += np.inner(self.vector, Main.f)
        
        # Calculate the facility-customer cost
        for i in range(0, Main.n):
            temp = int(sys.maxsize)
            for j in range(0, Main.m):
                if self.vector[j] and Main.c[i][j] < temp:
                    temp = Main.c[i][j]
            result += temp
        
        self.value = result

def strategy_1(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 3:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2, r3 = rand_nums
    vi1 = np.logical_xor(Main.individual_list[r2].vector, Main.individual_list[r3].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi = np.logical_xor(vi1, Main.individual_list[r1].vector)
    ind.vi = vi

def strategy_2(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 2:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2 = rand_nums
    vi1 = np.logical_xor(Main.individual_list[r1].vector, Main.individual_list[r2].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi = np.logical_xor(vi1, Main.best_individual.vector)
    ind.vi = vi

def strategy_3(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 5:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2, r3, r4, r5 = rand_nums
    vi1 = np.logical_xor(Main.individual_list[r2].vector, Main.individual_list[r3].vector)
    vi2 = np.logical_xor(Main.individual_list[r4].vector, Main.individual_list[r5].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi2 = np.logical_and(vi2, Ii)
    vi = np.logical_or(vi1, vi2)
    vi = np.logical_xor(vi, Main.individual_list[r1].vector)
    ind.vi = vi

def strategy_4(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 4:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2, r3, r4 = rand_nums
    vi1 = np.logical_xor(Main.individual_list[r1].vector, Main.individual_list[r2].vector)
    vi2 = np.logical_xor(Main.individual_list[r3].vector, Main.individual_list[r4].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi2 = np.logical_and(vi2, Ii)
    vi = np.logical_or(vi1, vi2)
    vi = np.logical_xor(vi, Main.best_individual.vector)
    ind.vi = vi

def strategy_5(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 2:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2 = rand_nums
    vi1 = np.logical_xor(Main.best_individual.vector, ind.vector)
    vi2 = np.logical_xor(Main.individual_list[r1].vector, Main.individual_list[r2].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi2 = np.logical_and(vi2, Ii)
    vi = np.logical_or(vi1, vi2)
    vi = np.logical_xor(vi, ind.vector)
    ind.vi = vi

def strategy_6(ind:individual):
    rand_nums = set()
    while len(rand_nums) < 4:
        rand_num = random.randint(0, Main.population_size-1)
        rand_nums.add(rand_num)
    r1, r2, r3, r4 = rand_nums
    vi1 = np.logical_xor(Main.best_individual.vector, ind.vector)
    vi2 = np.logical_xor(Main.individual_list[r1].vector, Main.individual_list[r2].vector)
    vi3 = np.logical_xor(Main.individual_list[r3].vector, Main.individual_list[r4].vector)
    Ii = np.zeros(Main.m)
    for j in range(0, Main.m):
        if random.random() < ind.Fki:
            Ii[j] = 1
    vi1 = np.logical_and(vi1, Ii)
    vi2 = np.logical_and(vi2, Ii)
    vi3 = np.logical_and(vi3, Ii)
    vi = np.logical_or(vi1, vi2)
    vi = np.logical_or(vi, vi3)
    vi = np.logical_xor(vi, ind.vector)
    ind.vi = vi

def read_data(datapath):
        Main.m, Main.n, Main.f, Main.c = getData(datapath=datapath)

def run():
    # datapath_list = ['/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO1',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO2',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO3',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO4',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO5',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/Q/MQ1',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/Q/MQ2',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/Q/MQ3',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/Q/MQ4',
    #                  '/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/Q/MQ5']
    
    datapath_list = ['/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/O/MO1']
    
    for datapath in datapath_list:
        read_data(datapath=datapath)
        instance = datapath.split('/')[-1].strip()
        output_filename = f'/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/OUTPUT_0/{instance}_result.txt'
        f = open(output_filename, 'w+')
        print(f'INSTANCE: {instance}\n')
        print(f'TOTAL GENERATION IS: {Main.goal_generation}\n')
        print(f'INSTANCE: {instance}\n', file=f)
        print(f'TOTAL GENERATION IS: {Main.goal_generation}\n', file=f)
        
        of = open(f'/Users/YeungYathin/Desktop/创新实践/复现代码/SabDE/M/{instance[1]}/{instance}.opt', 'r')
        optimum_value = of.read().split(' ')[-1]
        
        for i in range(3):
            print(f'-------------------------------------------------------------------------------------------------------------------------\n')
            print(f'-------------------------------------------------------------------------------------------------------------------------\n', file=f)
            print(f'ROUND {i+1}:')
            print(f'ROUND {i+1}:', file=f)
            print(f'Generation, best, average, variance, time(s)')
            print(f'Generation, best, average, variance, time(s)', file=f)

            main_instance = Main()
            found_best_vector, found_best_value = main_instance.SabDE()

            print(f'The optimum value should be {optimum_value}')
            print(f'The optimum value should be {optimum_value}',file=f)
            print(f'{found_best_value} {time.time()-Main.time_start}\n')
            print(f'{found_best_value} {time.time()-Main.time_start}\n', file=f)
if __name__ == '__main__':
    run()
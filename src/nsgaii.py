import random as rn
import numpy as np
import matplotlib.pyplot as plt
import math
 
#_____________________________________________________________________________
def random_population(nv,n,lb,ub):
    # nv = número de variables
    # n = número de soluciones aleatorias
    # lb = límiter inferior (lower bound)
    # ub = límiter superior (upper bound)
    pop=np.zeros((n, nv)) 
    for i in range(n):
        pop[i,:] = np.random.uniform(lb,ub)
 
    return pop
#_____________________________________________________________________________
def crossover(pop, crossover_rate):
    offspring = np.zeros((crossover_rate, pop.shape[1]))
    for i in range(int(crossover_rate/2)):
        r1=np.random.randint(0, pop.shape[0])
        r2 = np.random.randint(0, pop.shape[0])
        while r1 == r2:
            r1 = np.random.randint(0, pop.shape[0])
            r2 = np.random.randint(0, pop.shape[0])
        cutting_point = np.random.randint(1, pop.shape[1])
        offspring[2*i, 0:cutting_point] = pop[r1, 0:cutting_point]
        offspring[2*i, cutting_point:] = pop[r2, cutting_point:]
        offspring[2*i+1, 0:cutting_point] = pop[r2, 0:cutting_point]
        offspring[2*i+1, cutting_point:] = pop[r1, cutting_point:]
 
    return offspring
#_____________________________________________________________________________
def mutation(pop, mutation_rate):
    offspring = np.zeros((mutation_rate, pop.shape[1]))
    for i in range(int(mutation_rate/2)):
        r1=np.random.randint(0, pop.shape[0])
        r2 = np.random.randint(0, pop.shape[0])
        while r1 == r2:
            r1 = np.random.randint(0, pop.shape[0])
            r2 = np.random.randint(0, pop.shape[0])
        cutting_point = np.random.randint(0, pop.shape[1])
        offspring[2*i] = pop[r1]
        offspring[2*i,cutting_point] = pop[r2,cutting_point]
        offspring[2*i+1] = pop[r2]
        offspring[2*i+1, cutting_point] = pop[r1, cutting_point]
 
    return offspring
#_____________________________________________________________________________
def local_search(pop, n, step_size, problem):
    offspring = np.zeros((n, pop.shape[1]))
    for i in range(n):
        r1 = np.random.randint(0, pop.shape[0])
        chromosome = pop[r1, :].copy()
        perturb = np.random.uniform(-step_size, step_size, size=chromosome.shape)
        #chromosome += perturb
        chromosome = np.clip(chromosome + perturb, problem.xl, problem.xu)
        offspring[i, :] = chromosome
    return offspring
#_____________________________________________________________________________
def evaluation(pop, problem):
    return problem.evaluate(pop, return_values_of=["F"])
#_____________________________________________________________________________
def crowding_calculation(fitness_values):
    pop_size = len(fitness_values[:, 0])
    fitness_value_number = fitness_values.shape[1]
    matrix_for_crowding = np.zeros((pop_size, fitness_value_number))
    
    for m in range(fitness_value_number):
        sorted_index = np.argsort(fitness_values[:, m])
        matrix_for_crowding[sorted_index[0], m] = np.inf
        matrix_for_crowding[sorted_index[-1], m] = np.inf
        f_min = fitness_values[sorted_index[0], m]
        f_max = fitness_values[sorted_index[-1], m]
        for i in range(1, pop_size - 1):
            if f_max - f_min == 0:
                matrix_for_crowding[sorted_index[i], m] = 0
            else:
                matrix_for_crowding[sorted_index[i], m] = (
                    fitness_values[sorted_index[i + 1], m] - fitness_values[sorted_index[i - 1], m]
                ) / (f_max - f_min)
    return np.sum(matrix_for_crowding, axis=1)
#_____________________________________________________________________________
def remove_using_crowding(fitness_values, number_solutions_needed):
    pop_index = np.arange(fitness_values.shape[0])
    crowding_distance = crowding_calculation(fitness_values)
    sorted_index = np.argsort(-crowding_distance)  # Se ordena en orden descendiente
    selected_pop_index = sorted_index[:number_solutions_needed]
    return selected_pop_index
#_____________________________________________________________________________
def pareto_front_finding(fitness_values, pop_index):
    pop_size = fitness_values.shape[0]
    pareto_front = np.ones(pop_size, dtype=bool)
    for i in range(pop_size):
        for j in range(pop_size):
            if all(fitness_values[j] <= fitness_values[i]) and any(fitness_values[j] < fitness_values[i]):
                pareto_front[i] = False
                break
    return pareto_front
#_____________________________________________________________________________
def selection(pop, fitness_values, pop_size):
    new_pop = []
    new_fitness = []
    pop_index = np.arange(len(pop))
    remaining = pop_index.copy()
    
    while len(new_pop) < pop_size:
        current_fitness = fitness_values[remaining]
        pareto_mask = pareto_front_finding(current_fitness, remaining)
        pareto_indices = remaining[pareto_mask]
        if len(new_pop) + len(pareto_indices) <= pop_size:
            new_pop.extend(pop[pareto_indices])
            new_fitness.extend(fitness_values[pareto_indices])
            remaining = np.setdiff1d(remaining, pareto_indices)
        else:
            needed = pop_size - len(new_pop)
            reduced_indices = remove_using_crowding(fitness_values[pareto_indices], needed)
            new_pop.extend(pop[pareto_indices[reduced_indices]])
            new_fitness.extend(fitness_values[pareto_indices[reduced_indices]])
            break
    return np.array(new_pop), np.array(new_fitness)

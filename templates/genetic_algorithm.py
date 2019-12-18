import numpy

def cal_pop_fitness(equation_inputs, pop):
    fitness = numpy.sum(pop*equation_inputs, axis=1)
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    crossover_point = numpy.uint8(offspring_size[1]/2)
    for k in range(offspring_size[0]):
        parent1_idx = k%parents.shape[0]
        parent2_idx = (k+1)%parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring
def mutation(offspring_crossover, num_mutations):
    for idx in range(offspring_crossover.shape[0]):
        gene_idx = 1
        for mutation_num in range(num_mutations):
            random_value = numpy.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx, gene_idx] = offspring_crossover[idx, gene_idx] + random_value
            gene_idx = gene_idx + 4
    return offspring_crossover
equation_inputs = [-3.5,2,1,-1.5,3.8,11]
num_weights = len(equation_inputs)

sol_per_pop = 10
num_parents_mating = 5
pop_size = (sol_per_pop,num_weights)
new_population = numpy.random.uniform(low=-5, high=5.0, size=pop_size)
print(new_population)

best_outputs = []
num_generations = 5
for generation in range(num_generations):
    print("Generation : ", generation)
   
    fitness = cal_pop_fitness(equation_inputs, new_population)
    print("Fitness")
    print(fitness)
    best_outputs.append(numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))
    print("Best result : ", numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))
    parents =select_mating_pool(new_population, fitness,
                                      num_parents_mating)
    print("Parents")
    print(parents)
    offspring_crossover = crossover(parents,
                                       offspring_size=(pop_size[0]-parents.shape[0], num_weights))
    print("Crossover")
    print(offspring_crossover)
    offspring_mutation =mutation(offspring_crossover, num_mutations=2)
    print("Mutation")
    print(offspring_mutation)
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
   
    print("New Population")
    print(new_population)
fitness =cal_pop_fitness(equation_inputs, new_population)
best_match_idx = numpy.where(fitness == numpy.max(fitness))

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])


import matplotlib.pyplot
matplotlib.pyplot.plot(best_outputs)
matplotlib.pyplot.xlabel("Iteration")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.show()
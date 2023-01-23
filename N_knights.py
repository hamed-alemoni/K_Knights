import random

# ------------------------------------------------------ PRIMARY POPULATION

def generate_primary_population(population_size, n):
    primary_population = []
    
    for _ in range(population_size):
        new_member = create_new_member(n)
        
        # add new created member
        primary_population.append(new_member)
    
    return primary_population


def create_new_member(n):
    new_member = {}
    counter = 0
    while counter != n:
            # generate random row and column
            random_row = random.randint(1,n)
            random_column = random.randint(1,n)
            
            # new row was added
            if random_row not in new_member.keys():
                new_member[random_row] = []
                new_member[random_row].append(random_column)
                counter += 1
                continue

            # to doesn't add repetitious column    
            if random_row in new_member.keys() and random_column in new_member[random_row]:
                continue

            # add new column to existed row
            new_member[random_row].append(random_column)
            counter += 1

                
                
            
        
        # add a new place to put value of fitness function later
    new_member['fitness'] = -1

    return new_member




# ------------------------------------------------------ CROSSOVER

def crossover(population):
    index = -1, -1
    for i in range(0, len(population), 2):
        # determine parents
        first_parent = population[i]
        second_parent = population[i + 1]

        # get copy from parents
        child1 = first_parent.copy()
        child2 = second_parent.copy()

        for _ in range(2):

            try:
            
                first_chromosome_index, second_chromosome_index = find_chromosome_indexes(first_parent, second_parent, index)

                # for next substitution we shouldn't get same indexes
                index = first_chromosome_index, second_chromosome_index
                # substitution chromosomes
                child1[first_chromosome_index], child2[second_chromosome_index] = child2[second_chromosome_index], child1[first_chromosome_index]
            except TypeError:
                pass
        # create children and add fitness attribute
        child1['fitness'] = -1
        child2['fitness'] = -1

        # add new children
        population.append(child1)
        population.append(child2)


        

    return population

# find chromosomes of two parents to swap them
def find_chromosome_indexes(first_parent, second_parent, index):
    for i in first_parent.keys():
        for j in second_parent.keys():
            # doesn't check fitness key
            # length of values should be equal
            # new indexes should't be repetitious
            if i != 'fitness' and j != 'fitness' and len(first_parent[i]) == len(second_parent[j]) and index[0] not in (i, j) and index[1] not in (i, j):
                return i, j

# ------------------------------------------------------ MUTATION

def mutation(population, mutation_rate, n):
    # separate children from their parents 
    children_indexes = [i for i in range(len(population) // 2 , len(population))]
    # shuffle children
    random.shuffle(children_indexes)
    # keep new children based on mutation rate
    children_indexes = children_indexes[: int(len(children_indexes) * mutation_rate)]
    
    # use SWAP way for mutation
    for child_index in children_indexes:

        child_rows = list(population[child_index].keys())

        # remove fitness key
        child_rows = child_rows[:len(child_rows) - 1]
        
        random.shuffle(child_rows)

        # choose random keys(rows)
        index1 = random.choice(child_rows)
        index2 = random.choice(child_rows)

        # swap values(columns) of two keys(rows)
        population[child_index][index1], population[child_index][index2] = population[child_index][index2], population[child_index][index1]
        
        

        

    
    return population
        

# ------------------------------------------------------ FITNESS
def fitness(population, n):
    
    for i in range(len(population)):
        conflict = 0
        gene = population[i]
        for row in gene.keys():
            if row == 'fitness':
                continue
            for column in gene[row]:

                # all one is because indexes are started from 0
                if (row + 2 in gene.keys() and column + 1 in gene[row + 2]) \
                    or (row + 1 in gene.keys() and column + 2 in gene[row + 1]) \
                    or (row - 1 in gene.keys() and column + 2 in gene[row - 1]) \
                    or (row - 2 in gene.keys() and column + 1 in gene[row - 2]):

                        conflict += 1
        
        population[i]['fitness'] = conflict
        conflict = 0
    
    return population

            

# ------------------------------------------------------ ELIMINATION

def elimination(population):
    population = population[0:len(population) // 2]
    return population


# ------------------------------------------------------ SORT

def sort(population):
    # sort base on fitness attribute
    population.sort(key = lambda element:element['fitness'] )
    return population

# ------------------------------------------------------ SOLUTION
def find_solution(population, solutions):
    for i in population:
        if i['fitness'] == 0:
            solutions.add(str(i))
    
    return solutions

# ------------------------------------------------------ FILE

def write_solutions(solutions):
    with open('solutions.txt', 'w') as file:
        file.write(''.join(i + '\n' for i in solutions))


def read_solutions():
    solutions = ''
    with open('solutions.txt', 'r') as file:
        solutions = file.readlines()
    
    return solutions

def main():

    population_size = 200

    n = 8

    mutation_rate = 0.01

    mutation_epoch = random.randint(5,10)

    epoch = 200

    solutions = set()

    population = generate_primary_population(population_size, n)
    
    population = fitness(population, n)

    population = sort(population)

    solutions = find_solution(population, solutions)

    for i in range(epoch):

        population = crossover(population)

        if i % mutation_epoch == 0:
            population = mutation(population, mutation_rate, n)

        population = fitness(population, n)

        population = sort(population)

        population = elimination(population)

        solutions = find_solution(population, solutions)

    write_solutions(solutions)


if __name__ == '__main__':
    main()
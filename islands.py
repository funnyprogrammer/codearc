from multiprocessing import Pool
from random import randint
from ast import literal_eval
import cycle as cycle

def nonblank_lines(f):   # Joon
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland):   # Joon
    for i in range(int((len(population))*percentageOfBestIndividualsForMigrationPerIsland)):
        allBests = []
        with open('island_files/broadcast_{0}.txt'.format(islandNumber), 'r') as broad1:
            for line in nonblank_lines(broad1):
                allBests.append(literal_eval(line))
        broad1.close()
        allBests.append(population[sortedEvaluatedPopulation[i][5]])
        with open('island_files/broadcast_{0}.txt'.format(islandNumber), 'w') as broad2:
            for ini in range(len(allBests)):
                broad2.write(str(allBests[ini]) + '\n')
        allEVA = []
        with open('island_files/evaluationB_{0}.txt'.format(islandNumber), 'r') as broad1:
            for line in nonblank_lines(broad1):
                allEVA.append(literal_eval(line))
        broad1.close()
        allEVA.append(sortedEvaluatedPopulation[i][0])
        with open('island_files/evaluationB_{0}.txt'.format(islandNumber), 'w') as broad2:
            for ini in range(len(allEVA)):
                broad2.write(str(allEVA[ini]) + '\n')

def set_broadcast2(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland):   # Joon
    for i in range(int((len(population))*percentageOfBestIndividualsForMigrationPerIsland)):
        allBests = []
        allBests.append([population[sortedEvaluatedPopulation[i][5]], [sortedEvaluatedPopulation[i][0]]])
        with open('island_files/broadcast_{0}.txt'.format(islandNumber), 'w') as broad2:
            for ini in range(len(allBests)):
                broad2.write(str(allBests[ini]) + '\n')

def ins_broadcast(num_threads):
    #zerar o broadcast
    broad = open('island_files/broadcast.txt', 'w')
    broad.close()

    for each in range(num_threads):  # att o número para uma variável
        allBests = []
        with open('island_files/broadcast_{0}.txt'.format(each), 'r') as broad1:
            for line in nonblank_lines(broad1):
                allBests.append(literal_eval(line))
        broad1.close()
        prevBests = []
        with open('island_files/broadcast.txt', 'r') as broad2:
            for line in nonblank_lines(broad2):
                prevBests.append(literal_eval(line))
        broad2.close()
        prevBests.extend(allBests)
        with open('island_files/broadcast.txt', 'w') as broad:
            for ini in range(len(prevBests)):
                broad.write(str(prevBests[ini]) + '\n')
        broad.close()
    return

def creator(var):
    broad = open('island_files/broadcast_{0}.txt'.format(var), 'w')
    broad.close()
    plot = open('island_files/plotting_{0}.txt'.format(var), 'w')
    plot.close()

def create_island(num_islands, num_threads):
    broad = open('island_files/broadcast.txt', 'w')
    broad.close()
    migra = open('island_files/migrationN.txt', 'w')
    migra.write(str(1) + '\n')
    migra.close()
    p = Pool(num_threads)
    p.map(creator, num_islands)
    p.close()

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
                yield line

def evaluateIndividualB(cromossome):
    eva = []
    with open('island_files/broadcastEVA.txt', 'r') as f:
        for line in f:
            eva.append(literal_eval(line))
    return eva[cromossome]

def evaluateIndividual(island, cromossome):
    eva = []
    with open('island_files/evaluation_{0}.txt'.format(island), 'r') as f:
        for line in f:
            eva.append(literal_eval(line))
    return eva[cromossome]

def evaluateIndividualC(cromossome):
    eva = []
    with open('island_files/broadcast.txt', 'r') as f:
        for line in f:
            eva.append(literal_eval(line))
    return eva[cromossome][1]

def isMigrationNeed():
    migraNeed = []
    with open('island_files/migrationN.txt', 'r') as f:
        for line in f:
            migraNeed.append(literal_eval(line))
    return migraNeed[0]

def do_migration(num_threads, mig_policy_size):
    if isMigrationNeed() == 0:
        return
    else:
        myTests = []
        myTestsEva = []
        for each in range(num_threads):
            allBests = []
            with open('island_files/broadcast_{0}.txt'.format(each), 'r') as broad1:
                for line in nonblank_lines(broad1):
                    allBests.append(literal_eval(line))
            broad1.close()
            myTests.extend(allBests)
            allEVA = []
            with open('island_files/evaluationB_{0}.txt'.format(each), 'r') as eva1:
                for line in nonblank_lines(eva1):
                    allEVA.append(literal_eval(line))
            eva1.close()
            myTestsEva.extend(allEVA)
            prevBests = []
            with open('island_files/broadcast.txt', 'r') as broad2:
                for line in nonblank_lines(broad2):
                    prevBests.append(literal_eval(line))
            broad2.close()
            prevBests.extend(allBests)
            with open('island_files/broadcast.txt', 'w') as broad:
                for ini in range(len(prevBests)):
                    broad.write(str(prevBests[ini]) + '\n')
            broad.close()
            prevBestsE = []
            with open('island_files/broadcastEVA.txt', 'r') as broad3:
                for line in nonblank_lines(broad3):
                    prevBestsE.append(literal_eval(line))
            broad3.close()
            prevBestsE.extend(allEVA)
            with open('island_files/broadcastEVA.txt', 'w') as broad:
                for ini in range(len(prevBests)):
                    broad.write(str(prevBestsE[ini]) + '\n')
            broad.close()
        print('---------- Migrating ----------')
        for island_number in range(num_threads):
            island = open('island_files/island_{0}.txt'.format(island_number), 'r')
            island_content = []
            for line in island:
                island_content.append(literal_eval(line))
            broad = open('island_files/broadcast.txt', 'r')
            best_gen_list = []
            for line in broad:
                best_gen_list.append(literal_eval(line))
            broad.close()
            broad = open('island_files/evaluation_{0}.txt'.format(island_number), 'r')
            worst_gen_list = []
            count = 0
            for line in broad:
                value = [literal_eval(line), count]
                worst_gen_list.append(value)
                count = count + 1
            sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
            broad.close()
            iter = 0
            while iter < mig_policy_size*(len(island_content)):
                random_best_gen = randint(0, len(best_gen_list)-1)
                if sorted_worst_gen_list[iter][0] < evaluateIndividualB(random_best_gen):
                    island_content[sorted_worst_gen_list[iter][1]] = best_gen_list[random_best_gen]
                iter = iter + 1
            island.close()
            with open('island_files/island_{0}.txt'.format(island_number), 'w') as new_island:
                for ini in range(len(island_content)):
                    new_island.write(str(island_content[ini]) + '\n')
            new_island.close()
            broad.close()
        broad = open('island_files/broadcast.txt', 'w')
        broad.close()
        broadEVA = open('island_files/broadcastEVA.txt', 'w')
        broadEVA.close()
        for i in range(num_threads): #att o número para uma variável
            broad = open('island_files/broadcast_{0}.txt'.format(i), 'w')
            broad.close()
            eva = open('island_files/evaluationB_{0}.txt'.format(i), 'w')
            eva.close()
            eva2 = open('island_files/evaluation_{0}.txt'.format(i), 'w')
            eva2.close()
        return

def do_migration2(island_content, island_number, island_fitness, mig_policy_size):
    if isMigrationNeed() == 0:
        return
    else:
        best_gen_list = []
        with open('island_files/broadcast.txt', 'r') as broad2:
               for line in nonblank_lines(broad2):
                best_gen_list.append(literal_eval(line))
        broad2.close()
        worst_gen_list = []
        count = 0
        for individuo in range(len(island_fitness)):
            worst_gen_list.append([island_fitness[individuo], count])
            count += 1
        print('Migrating', island_number)
        sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
        iter = 0
        while iter < mig_policy_size*(len(island_content)):
            random_best_gen = randint(0, len(best_gen_list)-1)
            worst_fit = sorted_worst_gen_list[iter][0]
            best_fit = best_gen_list[random_best_gen][1]
            if worst_fit < best_fit[0]:
                island_content[sorted_worst_gen_list[iter][1]] = best_gen_list[random_best_gen][0]
            iter = iter + 1
        broad = open('island_files/broadcast_{0}.txt'.format(island_number), 'w')
        broad.close()
        print('Migration', island_number, 'concluded')
        return
# -*- coding=utf8 -*-
from GraphUtils import *
import math
from random import random, randint, choice


class GeneticColoring:
    """Given graph as dictionary of adjacencies, returns coloring
    recieved by genetic algorithm"""

    def __init__(self, graph, population_size=10, generations_nr=10,
                 mutation_rate=1.0
                 ):
        self.naive_coloring = color_greedy(graph)
        self.max_colors = nr_of_colors(self.naive_coloring)

        self.adjlist = graph.adjlist
        self.vertex_nr = len(self.adjlist)

        self.allel_size = math.ceil(math.log(self.max_colors, 2))
        self.allels_nr = max(self.adjlist.keys())
        self.chromosome_size = (self.allels_nr + 1) * self.allel_size

        self.population_size = population_size
        self.generations_nr = generations_nr
        self.mutation_rate = mutation_rate
        self.population = [{v: randint(0, self.max_colors)
                            for v in self.adjlist}
                           for i in range(self.population_size)
                           ]
        self.population[0] = self.naive_coloring  # cheat a little

    def crossover(self, chromosome1, chromosome2):
        '''Return child - crossover of two specimens, provided as dicts'''
        if not len(chromosome1) == len(chromosome2) == self.vertex_nr:
            raise ValueError('chromosomes of length %d, %d instead of %d' %
                             (len(chromosome1),
                              len(chromosome2),
                              self.vertex_nr)
                             )
        splice_point = randint(0, self.vertex_nr)

        if splice_point < self.vertex_nr / 2:  # add 2nd splicing point
            second_splice = randint(splice_point, self.chromosome_size)
        else:
            second_splice = self.vertex_nr

        child = {i: chromosome1[i] for i in chromosome1.keys()}
        for i in range(splice_point, second_splice):
            if i in chromosome1.keys():
                child[i] = chromosome2[i]  # replace #1 allels with #2 allels

        return child

    def mutate(self, chromosome):
        '''random SNP mutation on chromosome, with proper rate'''
        mutate = random()
        if mutate < self.mutation_rate:
            if isinstance(chromosome, dict):   # specimen as dictionary
                snp = choice(list(chromosome.keys()))
                new_val = randint(0, self.max_colors)
                chromosome[snp] = new_val
                return chromosome
            # and for encoded specimen
            snp = randint(0, len(chromosome) - 1)
            if chromosome[snp] == '0':
                chromosome = chromosome[:snp] + '1' + chromosome[(snp + 1):]
            elif chromosome[snp] == '1':
                chromosome = chromosome[:snp] + '0' + chromosome[(snp + 1):]
        return chromosome

    def eval_fitness(self, coloring):
        '''return chromatic number of specimen and whether coloring is valid'''
        if isinstance(coloring, str):
            coloring = self.decode(coloring)
        if is_coloring_good(self, coloring):
            return nr_of_colors(coloring), True
        else:  # silly large int for sorting to work, as coloring is invalid
            return self.vertex_nr**2, False

    def select_parents(self):
        pass

    def breed_next_generation(self):
        pass

#==============================================================================
# for specimens encoded as strings
    def encode(self, coloring):
        '''Return chromosome for given specimen-graph coloring,
        if none given - return randomly initiated coloring'''
        graph_nodes = self.adjlist.keys()
        chromosome = ''
        for i in range(self.allels_nr + 1):
            if i in graph_nodes:
                if coloring:
                    allel = bin(coloring[i])[2:]
                else:
                    allel = bin(randint(0, self.max_colors-1))[2:]
                while len(allel) < self.allel_size:
                    allel = '0' + allel
                chromosome += allel
            else:
                chromosome += '-' * self.allel_size
        return chromosome

    def decode(self, chromosome):
        'Return coloring encoded by recieved chromosome'
        specimen = {}
        pos = 0
        while pos < len(chromosome):
            try:
                allel = int(chromosome[pos: pos + self.allel_size], 2)
                specimen[int(pos/self.allel_size)] = allel
            except ValueError:   # empty '---' allel encountered
                pass             # 'trash DNA'
            finally:
                pos += self.allel_size
        return specimen

    def str_crossover(self, chromosome1, chromosome2):
        '''Return child - crossover of two specimens'''
        if not len(chromosome1) == len(chromosome2) == self.chromosome_size:
            import pdb
            pdb.set_trace()
            raise ValueError('chromosomes of length %d, %d instead of %d' %
                             (len(chromosome1),
                              len(chromosome2),
                              self.chromosome_size)
                             )
        if not (isinstance(chromosome1, str) and isinstance(chromosome2, str)):
            raise KeyError("chromosomes should be passed encoded as strings")
        splicing_point = randint(0, self.chromosome_size)
        child = chromosome1[:splicing_point] + chromosome2[splicing_point:]

        if splicing_point < self.chromosome_size / 2:  # add 2nd splicing point
            second_splice = randint(splicing_point, self.chromosome_size)
            child = child[:second_splice] + chromosome1[second_splice:]
        return child

    def breed_generations_of_encoded(self, generations_nr=None):
        '''Select best specimens from population,
        use them to breed next generation.
        Working on specimens as (bite) string'''
        if not generations_nr:
            generations_nr = self.generations_nr
        # initiate population if none is present
        self.population = [self.encode(False)
                           for i in range(self.population_size)]
            # cheat a little
        self.population[0] = self.encode(self.naive_coloring)

        for i in range(generations_nr):  # breed number of generations
            # choose the size of selected best fitted subpopulation
            bps = randint(int(self.population_size/5),
                          int(self.population_size/3)
                          )
            parents = sorted(self.population,
                             key=lambda x: self.eval_fitness(x)[0]
                             )[:bps]
            # create next generation replacing old population
            self.population = []
            # let in a few best fitted from previous
            self.population = [one for one in parents[:5] if one[1]]
            # and fill with children of random specimens
            while len(self.population) < self.population_size:
                mother = parents[randint(0, bps-1)]
                father = parents[randint(0, bps-1)]
                child = self.mutate(self.str_crossover(mother, father))
                self.population.append(child)
        # select the best specimen
        best_gene = sorted(self.population,
                           key=lambda x: self.eval_fitness(x)[0]
                           )[0]
        best_specimen = self.decode(best_gene)
        # return the best one if it works
        if self.eval_fitness(best_specimen)[1]:
            return best_specimen
        else:
            return None  # no valid solution was breed

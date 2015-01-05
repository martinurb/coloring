# -*- coding=utf8 -*-
from GraphUtils import *
import math
from random import random, randint, choice


class GeneticColoring:
    """Given graph as dictionary of adjacencies, returns coloring
    recieved by genetic algorithm"""

    def __init__(self, graph, population_size=10, nr_of_generations=10,
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
        self.nr_of_generations = nr_of_generations
        self.mutation_rate = mutation_rate
        self.population = []

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

    def initialize_population(self):
        self.population = [{v: randint(0, self.max_colors)
                           for v in self.adjlist}
                           for i in range(self.population_size)
                           ]
        self.population[0] = self.naive_coloring  # cheat a little

    def select_parents(self):
        # choose the size of selected best fitted subpopulation
        bps = randint(int(self.population_size/5),
                      int(self.population_size/3)
                      )
        parents = sorted(self.population,
                         key=lambda x: self.eval_fitness(x)[0]
                         )[:bps]
        return parents, bps

    def breed_next_generation(self, parents, bps):
        # purge population
        self.population = []
        # let in a few best fitted from previous
        self.population = [one for one in parents[:5] if one[1]]
        # and fill with children of random specimens; dumb but works
        while len(self.population) < self.population_size:
            mother = parents[randint(0, bps-1)]
            father = parents[randint(0, bps-1)]
            child = self.mutate(self.crossover(mother, father))
            self.population.append(child)

    def breed_generations(self, nr_of_generations=None):
        '''Select best specimens from population,
        use them to breed next generation.'''
        self.initialize_population()
        if not nr_of_generations:
            nr_of_generations = self.nr_of_generations
        for i in range(nr_of_generations):  # breed number of generations
            # select parents for next generation
            parents, bps = self.select_parents()
            self.breed_next_generation(parents, bps)
        # finally select the best specimen
        best_in_final_gen = sorted(self.population,
                                   key=lambda x: self.eval_fitness(x)[0]
                                   )
        best_specimen = best_in_final_gen[0]
        # return the best one if it works
        if self.eval_fitness(best_specimen)[1]:
            return best_specimen

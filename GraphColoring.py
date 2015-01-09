#! /usr/bin/python3
# -*- coding=utf8 -*-
import random
import time
import argparse
from GraphUtils import *
from GeneticColoring import GeneticColoring
from NN import NetworkColoring
import numpy as np


class RandomGraph(object):
    """Generates random graph of specified vertex number and filling
    represented as adjacency list"""
    def __init__(self, vertex_nr, filling, seed):
        random.seed(seed)
        self.vertex_nr = vertex_nr
        self.adjlist = {vertex: [] for vertex in range(1, vertex_nr + 1)}

        self.adjmatrix = np.array([[0 for _ in range(self.vertex_nr)]
                                  for _ in range(self.vertex_nr)])
            # vertex in test instances started from 1, so we too wont use 0
        for x in range(vertex_nr):
            for y in range(int(vertex_nr / 2)):
                if random.random() <= filling and x != y:
                    if x in self.adjlist:
                        if y not in self.adjlist[x]:
                            self.adjlist[x].append(y)
                    else:
                        self.adjlist[x] = [y]

                    if y in self.adjlist:
                        if x not in self.adjlist[y]:
                            self.adjlist[y].append(x)
                    else:
                        self.adjlist[y] = [x]

                    self.adjmatrix[x-1][y-1] = 1
                    self.adjmatrix[y-1][x-1] = 1
        if len(self.adjlist) != self.vertex_nr:
            raise ValueError("Graph not loaded properly. %d nodes of %d" %
                             (len(self.adjlist), self.vertex_nr)
                             )

    def print_graph(self):
        for vertex in self.adjlist:
            print(vertex, self.adjlist[vertex])

    def neighbours(self, vertex):
        return self.adjlist[vertex]

    def is_coloring_good(self, coloring):
        return is_coloring_good(self, coloring)

    def print_coloring(self, coloring, time, algorithm=None):
        if algorithm:
            print(algorithm)
        if self.is_coloring_good(coloring):
            print(nr_of_colors(coloring), 'colors, properly.', time, '[s]')
        else:
            print(nr_of_colors(coloring), 'colors', time, '[s], but \
something went wrong')
            # import pdb; pdb.set_trace()

    def color_greedy(self):
        "greedy alghoritm for graph coloring"
        coloring = {vertex: 0 for vertex in self.adjlist}
        for vtx in coloring:
            neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
            while coloring[vtx] in neigh_colors:
                coloring[vtx] += 1
        return coloring

    def color_bruteforce(self, aware=False):
        '''Bruteforce graph coloring'''
        nodes = sorted(list(self.adjlist.keys()))
        n = len(nodes)
        coloring = {vertex: 0 for vertex in nodes}  # empty

        if n >= 8 and aware:
            decision = input('Attepting to color large graph, it can take few \
hundred years. Continue? (y/n)').lower()
            if 'n' in decision:
                return {}  # not having free few hundred years apparently
        k_min = n
        counter = 0  # more readable than catching IndexError
        while counter < n ** n:  # now iterate over n**n possibilities
            if is_coloring_good(self, coloring):
                if nr_of_colors(coloring) < k_min:
                    best_coloring = {k: v for k, v in coloring.items()}
                    k_min = nr_of_colors(best_coloring)
            counter += 1
            inc_w_carryout(coloring, 0, n, nodes)
        return best_coloring

    def color_branch_bound(self, aware=False):
        '''Another attempt to bruteforce coloring,
        more efficient for sparse graphs'''
        best_coloring = color_greedy(self)       # for good start
        max_colors = nr_of_colors(best_coloring)  # ceilling for nr of colors

        nodes = sorted(list(self.adjlist.keys()))
        n = len(nodes)
        coloring = {vertex: 0 for vertex in nodes}  # empty

        if n > 8 and aware:
            decision = input('Attepting to color large graph, it can take few \
hundred years. Continue? (y/n)').lower()
            if 'n' in decision:
                return {}  # what a pity

        counter = 0  # more readable than catching IndexError
        while counter < max_colors ** n:  # now iterate over k**n possibilities
            if is_coloring_good(self, coloring):
                if nr_of_colors(coloring) < max_colors:
                    best_coloring = {k: v for k, v in coloring.items()}
                    max_colors = nr_of_colors(coloring)
            counter += 1
            inc_w_carryout(coloring, 0, max_colors, nodes)
        return best_coloring

    def color_lf(self):
        """Largest First algorithm for graph coloring"""
        coloring = {v: 0 for v in self.adjlist}
        nodes_by_deg = sorted(self.adjlist.items(), key=lambda x: len(x[1]))
        largest_first = [vtx[0] for vtx in nodes_by_deg[::-1]]
        for vtx in largest_first:
            neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
            while coloring[vtx] in neigh_colors:
                coloring[vtx] += 1
        return coloring


class TestInstance(RandomGraph):
    """Loads graph from specified file to adjacency list"""
    def __init__(self, filename):
        with open(filename, "r") as instance_file:
            instance_file = instance_file.readlines()

            nr = int(instance_file[0])
            super(TestInstance, self).__init__(nr, 0, 0)

            self.adjmatrix = np.array([[0 for _ in range(nr)]
                                       for _ in range(nr)])

            for line in instance_file[1:]:
                try:
                    x, y = (int(i) for i in line.split())

                    if x in self.adjlist:
                        self.adjlist[x].append(y)
                    else:
                        self.adjlist[x] = [y]

                    if y in self.adjlist:
                        self.adjlist[y].append(x)
                    else:
                        self.adjlist[y] = [x]

                    self.adjmatrix[x-1][y-1] = 1
                    self.adjmatrix[y-1][x-1] = 1
                except ValueError:
                    print("Invalid value in line %d : <%s>" %
                          (instance_file.index(line), line)
                          )
                except IndexError:
                    print("Invalid value [too large] on line %d : <%s>" %
                          (instance_file.index(line), line)
                          )


if __name__ == "__main__":

    argvparser = argparse.ArgumentParser(description="Testing algorithms for\
                                         graph coloring problem"
                                         )
    argvparser.add_argument("filename", metavar="filename", type=str,
                            nargs="+", help="test instance file name",
                            default=None)
    argvparser.add_argument('-a', action='store_true',
                            help='be aware of exact algorithms complexity. \
ask for confirmation before processing large graphs.')
    parsed_args = argvparser.parse_args()

    for filename in argvparser.parse_args().filename:
        aware = parsed_args.a
        graph = TestInstance(filename)
        graph_gen = GeneticColoring(graph,
                                    graph.vertex_nr*50,   # change to adjust
                                    graph.vertex_nr*50   # speed and precision
                                    )
        graph_nn = NetworkColoring(graph)
        graph.print_graph()
        print('')

        timer_start = time.clock()
        coloring_gr = graph.color_greedy()
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_gr, timer_stop, "Greedy algorithm")

        timer_start = time.clock()
        coloring_bb = graph.color_branch_bound(aware)
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_bb, timer_stop, "Branch and bound")

        timer_start = time.clock()
        coloring_bf = graph.color_bruteforce(aware)
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_bf, timer_stop, "Simple bruteforce")

        timer_start = time.clock()
        coloring_lf = graph.color_lf()
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_lf, timer_stop, "LF algorithm")

        timer_start = time.clock()
        coloring_gen = graph_gen.breed_generations()
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_gen, timer_stop, "Genetic algorithm")

        timer_start = time.clock()
        coloring_nn = graph_nn.outer_loop(10, .75)
        timer_stop = time.clock() - timer_start

        graph.print_coloring(coloring_nn, timer_stop, "Network algorithm")

specs = '''\n\nKolorowanie grafów. Możliwe algorytmy:
    -genetyczny
    -Browna
    -LF...
Wymagania: Pseudokod. Schemat: przykładowy prosty graf,\
z optymalnym pokolorowaniem (uzyskany np bruteforce)
dla reszty algorytmów - schemat kolejnego kroku na tym samym grafie\
i finalny wynik (inny optymalny? suboptymalny)

Nie zamieszczać tabel, wykresy proste liniowe \nPorównywać zbliżonej klasy
algorytmy: czas dokładnych, dokładność przybliżonych

instancje sprawdzające http://www.cs.put.poznan.pl/mmachowiak/instances/
    myciel4.txt
    queen6.txt - symetrycznie
1. liczba  - liczba wierzchołków
'''

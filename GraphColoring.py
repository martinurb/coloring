#! /usr/bin/python3
# -*- coding=utf8 -*-
import random
import time
import argparse
from GraphUtils import *
from GeneticColoring import GeneticColoring


class RandomGraph:
    """Generates random graph of specified vertex number and filling
    represented as adjacency list"""
    def __init__(self, vertex_nr, filling, seed):
        random.seed(seed)
        self.vertex_nr = vertex_nr
        self.adjlist = {vertex: [] for vertex in range(1, vertex_nr + 1)}
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
        if len(self.adjlist) != self.vertex_nr:
            raise ValueError("Graph not loaded properly. %d nodes of %d" %
                             (len(self.adjlist), self.vertex_nr)
                             )

    def printm(self):
        for vertex in self.adjlist:
            print(vertex, self.adjlist[vertex])

    def neighbours(self, vertex):
        return self.adjlist[vertex]

    def is_coloring_good(self, coloring):
        return is_coloring_good(self, coloring)

    def print_coloring(self, coloring, time=None):
        if time:
            print('Properly:', self.is_coloring_good(coloring), coloring,
                  time, '[s]')
        else:
            print('Properly:', self.is_coloring_good(coloring), coloring)

    def color_greedy(self):
        "greedy alghoritm for graph coloring"
        coloring = {vertex: 0 for vertex in self.adjlist}
        for vtx in coloring:
            neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
            while coloring[vtx] in neigh_colors:
                coloring[vtx] += 1
                neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
        return coloring

    def max_nr_of_colors(self):
        naive_coloring = self.color_greedy()
        return nr_of_colors(naive_coloring)

    def color_bf(self):
        '''another attempt to bruteforce coloring,
        more efficient for sparse graphs'''
        best_coloring = color_greedy(self)       # for good start
        max_colors = nr_of_colors(best_coloring)  # ceilling for nr of colors
        cur_colors = max_colors

        nodes = sorted(list(self.adjlist.keys()))
        n = len(nodes)
        coloring = {vertex: 0 for vertex in nodes}  # empty

        if n > 8:
            decision = input('Attepting to color large self, it can take few\
                hundred years. Continue? (y/n)').lower()
            if 'n' in decision:
                return None  # not having free few hundred years apparently

        counter = 0  # more readable than catching IndexError
        while counter < max_colors ** n:  # now iterate over k**n possibilities
            if is_coloring_good(self, coloring):
                if nr_of_colors(coloring) < cur_colors:
                    best_coloring = {k: v for k, v in coloring.items()}
                    cur_colors = nr_of_colors(coloring)
            counter += 1
            inc_w_carryout(coloring, 0, max_colors, nodes)
        return best_coloring

    def old_color_bf(self):
        """bruteforce alghoritm for graph coloring
        time of execution noticeable for nodes > 6 on core i5"""
        coloring = {v: 0 for v in self.adjlist}
        minnr_of_colors = self.vertex_nr
        mincoloring = {k: v for k, v in coloring.items()}
        try:
            for x in range(minnr_of_colors ** minnr_of_colors):
                if nr_of_colors(coloring) < minnr_of_colors:
                    if is_coloring_good(self, coloring):
                        minnr_of_colors = nr_of_colors(coloring)
                        mincoloring = {k: v for k, v in coloring.items()}
                coloring = next_coloring(coloring, self.vertex_nr)
            return mincoloring
        except OverflowError:
            print("minnr_of_colors", minnr_of_colors)

    def color_lf(self):
        """Largest First algorithm for graph coloring"""
        coloring = {v: 0 for v in self.adjlist}
        nodes_by_deg = sorted(self.adjlist.items(), key=lambda x: len(x[1]))
        largest_first = [vtx[0] for vtx in nodes_by_deg[::-1]]
        for vtx in largest_first:
            neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
            while coloring[vtx] in neigh_colors:
                coloring[vtx] += 1
                neigh_colors = [coloring[v] for v in self.adjlist[vtx]]
#        import pdb; pdb.set_trace()
        return coloring


class TestInstance(RandomGraph):
    """Loads graph from specified file to adjacency list"""
    def __init__(self, filename):
        with open(filename, "r") as instance_file:
            instance_file = instance_file.readlines()

            super(TestInstance, self).__init__(int(instance_file[0]), 0, 0)

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
                except ValueError:
                    print("Invalid value in line %d : <%s>" %
                          (instance_file.index(line), line)
                          )
                except IndexError:
                    print("Invalid value [too large] on line %d : <%s>" %
                          (instance_file.index(line), line)
                          )


if __name__ == "__main__":
    argvparser = argparse.ArgumentParser(description="Testing alghoritms for\
                                         graph coloring problem"
                                         )
    argvparser.add_argument("filename", metavar="filename", type=str,
                            nargs="+", help="test instance file name",
                            default=None)

    for filename in argvparser.parse_args().filename:
        graph = TestInstance(filename)
        graph.printm()
        print('')

        timer_start = time.clock()
        coloring = graph.color_greedy()
        timer_stop = time.clock() - timer_start

        print("greedy:", nr_of_colors(coloring), 'colors')
        graph.print_coloring(coloring, timer_stop)

        timer_start = time.clock()
        coloring = graph.color_bf()
        timer_stop = time.clock() - timer_start

        print("bruteforce:", nr_of_colors(coloring), 'colors')
        graph.print_coloring(coloring, timer_stop)

        timer_start = time.clock()
        coloring = graph.color_lf()
        timer_stop = time.clock() - timer_start

        print("LF:", nr_of_colors(coloring), 'colors')
        graph.print_coloring(coloring, timer_stop)
# yada yada from now on
        # meh = GeneticColoring(graph)
        # code = meh.encode(meh.naive_coloring)
        # specimen = meh.decode(code)
        # random_code = meh.encode(None)

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

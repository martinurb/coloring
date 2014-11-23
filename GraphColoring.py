# -*- coding=utf8 -*-
import random
import time
import argparse


class RandomGraph:
    def __init__(self, vertex_nr, filling, seed):
        random.seed(seed)
        self.vertex_nr = vertex_nr
        self.adjmatrix = [[0 for x in xrange(vertex_nr)]
                          for x in xrange(vertex_nr)]
        for x in range(vertex_nr):
            for y in range(x + 1, vertex_nr):
                if random.random() > filling:
                    el = 0
                else:
                    el = 1
                self.adjmatrix[x][y] = el
                self.adjmatrix[y][x] = el

    def printm(self):
        for row in self.adjmatrix:
            print(row)


class TestInstance(RandomGraph):

    def __init__(self, filename):
        with open(filename, "r") as instance_file:
            instance_file = instance_file.readlines()

            self.vertex_nr = int(instance_file[0])
            self.adjmatrix = [[0 for i in range(0, self.vertex_nr + 1)]
                              for j in range(0, self.vertex_nr + 1)]

            for line in instance_file[1:]:
                try:
                    x, y = (int(i) for i in line.split())
                    self.adjmatrix[x][y] = 1
                    self.adjmatrix[y][x] = 1
                except ValueError:
                    print("Invalid value in line %d : <%s>" %
                          (instance_file.index(line), line)
                          )
                except IndexError:
                    print("Invalid value [too large] on line %d : <%s>" %
                          (instance_file.index(line), line)
                          )


def neighbors(node, adjmatrix):
    row = adjmatrix[node]
    list = []
    for x in range(len(row)):
        if row[x] == 1:
            list.append(x)
    return list


def q_good_coloring(adjmatrix, coloring):
    for node in range(len(adjmatrix)):
        neigh = neighbors(node, adjmatrix)
        for v in neigh:
            if coloring[v] == coloring[node]:
                return False
    return True


def next_coloring(coloring, kmax):
    """Return next, at most k-coloring"""
    for x in range(len(coloring)):
        if coloring[x] < kmax - 1:
            coloring[x] = coloring[x] + 1
            break
        else:
            coloring[x] = 0
    return coloring


def nr_of_colors(coloring):
    colorlist = []
    for c in coloring:
        if c in colorlist:
            continue
        else:
            colorlist.append(c)
    return len(colorlist)


def col_bf_k(adjmatrix, k):
    """Attempts to find k-coloring of given adjmatrix"""
    vertex_nr = len(adjmatrix)
    qgood = False
    coloring = [0 for x in range(vertex_nr)]
    for x in range(vertex_nr ** k):
        if q_good_coloring(adjmatrix, coloring):
            qgood = True
            break
        coloring = next_coloring(coloring, k)
    return [qgood, coloring]


def col_bf_k_all(adjmatrix):
    """Return min coloring"""
    vertex_nr = len(adjmatrix)
    for k in range(1, vertex_nr + 1):
        coloring = col_bf_k(adjmatrix, k)
        if coloring[0]:
            return coloring


def col_bf(adjmatrix):
    vertex_nr = len(adjmatrix)
    coloring = [0 for x in range(vertex_nr)]
    minnr_of_colors = vertex_nr
    mincoloring = list(range(minnr_of_colors))
    try:
        for x in range(minnr_of_colors ** minnr_of_colors):
            if nr_of_colors(coloring) < minnr_of_colors:
                if q_good_coloring(adjmatrix, coloring):
                    minnr_of_colors = nr_of_colors(coloring)
                    mincoloring = coloring[:]
            coloring = next_coloring(coloring, vertex_nr)
        return mincoloring
    except OverflowError:
        print("minnr_of_colors", minnr_of_colors)


def col_greedy(adjmatrix):
    coloring = [-1 for x in range(len(adjmatrix))]
    for node in range(len(adjmatrix)):
        for c in range(len(adjmatrix)):
            badcolor = False
            for n in neighbors(node, adjmatrix):
                if c == coloring[n]:
                    badcolor = True
            if badcolor:
                continue
            else:
                coloring[node] = c
                break

    return coloring


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

        timestart = time.clock()
        coloring = col_bf(graph.adjmatrix)
        print([q_good_coloring(graph.adjmatrix, coloring), coloring],
              time.clock() - timestart)

        timestart = time.clock()
        print(col_bf_k_all(graph.adjmatrix), time.clock() - timestart)

        timestart = time.clock()
        coloring = col_greedy(graph.adjmatrix)
        print([q_good_coloring(graph.adjmatrix, coloring),
              col_greedy(graph.adjmatrix)], time.clock() - timestart)

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

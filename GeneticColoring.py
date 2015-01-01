from GraphUtils import *
import math


class GeneticColoring:
    """Given graph as dictionary of adjacencies, returns coloring
    recieved by genetic algorithm"""

    def __init__(self, graph):
        self.naive_coloring = color_greedy(graph)
        self.max_colors = nr_of_colors(self.naive_coloring)
        self.allel_size = int(math.ceil(math.log(self.max_colors, 2)))

        self.vertex_nr = graph.vertex_nr
        self.adjlist = graph.adjlist

    def encode(self, coloring):
        'Return chromosome for given specimen-graph coloring'
        graph_nodes = sorted(coloring.keys())
        chromosome = ''
        for i in range(max(graph_nodes) + 1):
            if i in graph_nodes:
                chromosome += bin(coloring[i])[2:].rjust(self.allel_size, '0')
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
            except ValueError:   # empty '---' allel
                pass             # 'trash DNA'
            finally:
                pos += self.allel_size
        return specimen

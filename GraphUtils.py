def nr_of_colors(coloring):
    colorlist = []
    for c in coloring.values():
        if c not in colorlist:
            colorlist.append(c)
    return len(colorlist)


def is_coloring_good(graph, coloring):
    if graph.adjlist and not coloring:
        return False
    for node in graph.adjlist:
        neigh_colors = [coloring[v] for v in graph.adjlist[node]]
        if coloring[node] in neigh_colors:
            return False
    return True


def next_coloring(coloring, kmax):
    """Return next, at most k-coloring"""
    for x in range(1, len(coloring)+1):
        if coloring[x] < kmax - 1:
            coloring[x] += 1
            break
        else:
            coloring[x] = 0
    return coloring


def neighbors(node, adjmatrix):
    row = adjmatrix[node]
    list = []
    for x in range(len(row)):
        if row[x] == 1:
            list.append(x)
    return list


def color_greedy(graph):
    "greedy alghoritm for graph coloring"
    coloring = {vertex: 0 for vertex in graph.adjlist}
    for vtx in coloring:
        neigh_colors = [coloring[v] for v in graph.adjlist[vtx]]
        while coloring[vtx] in neigh_colors:
            coloring[vtx] += 1
            neigh_colors = [coloring[v] for v in graph.adjlist[vtx]]
    return coloring


def inc_w_carryout(coloring, i, max_colors, nodes=None):
    '''Increment i-th element of coloring, checking if values
    is not larger than max possible # of color.
    Pre-calculated nodes can be passed for performance.
    'Overflows' with IndexError after k**n iterations,
    can be catched or prevented by loop while counter < k**n '''
    if not nodes:
        nodes = sorted(list(coloring.keys()))
    coloring[nodes[i]] += 1
    if coloring[nodes[i]] > max_colors:  # 'carry out'
        coloring[nodes[i]] = 0
        i = inc_w_carryout(coloring, i+1, max_colors, nodes)
    return i

def nr_of_colors(coloring):
    colorlist = []
    for c in coloring.values():
        if c not in colorlist:
            colorlist.append(c)
    return len(colorlist)


def is_coloring_good(graph, coloring):
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


def q_good_coloring(adjmatrix, coloring):
    for node in range(len(adjmatrix)):
        neigh = neighbors(node, adjmatrix)
        for v in neigh:
            if coloring[v] == coloring[node]:
                return False
        return True


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


def color_greedy(graph):
    "greedy alghoritm for graph coloring"
    coloring = {vertex: 0 for vertex in graph.adjlist}
    for vtx in coloring:
        neigh_colors = [coloring[v] for v in graph.adjlist[vtx]]
        while coloring[vtx] in neigh_colors:
            coloring[vtx] += 1
            neigh_colors = [coloring[v] for v in graph.adjlist[vtx]]
    return coloring

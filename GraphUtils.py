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


def bruteforce(graph):
    "another attempt to bruteforce coloring"
    best_coloring = color_greedy(graph)       # for good start
    max_colors = nr_of_colors(best_coloring)  # ceilling for nr of colors
    cur_colors = max_colors

    nodes = sorted(list(graph.adjlist.keys()))
    n = len(nodes)
    coloring = {vertex: 0 for vertex in nodes}
    if n > 8:
        decision = input('Attepting to color large graph, it can take few\
            hundred years. Continue? (y/n)').lower()
        if 'n' in decision:
            return None  # not having free few hundred years apparently
    counter = 0
    while counter < max_colors ** n:  # now iterate over k**n possibilities
        if is_coloring_good(graph, coloring):
            if nr_of_colors(coloring) < cur_colors:
                best_coloring = {k: v for k, v in coloring.items()}
                cur_colors = nr_of_colors(coloring)
        counter += 1
        inc_w_carryout(coloring, 0, max_colors, nodes)
    return best_coloring


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

import random
import time

class RandomGraph:
    def __init__(self,vertex_nr,filling,seed):
        random.seed(seed)
        self.vertex_nr = vertex_nr
        self.adjmatrix = [[0 for x in xrange(vertex_nr)] for x in xrange(vertex_nr)] 
        for x in range(vertex_nr):
            for y in range(x+1,vertex_nr):
                if random.random() > filling:
                    el = 0
                else:
                    el = 1
                self.adjmatrix[x][y] = el
                self.adjmatrix[y][x] = el

def printm(matrix):
    for r in range(len(matrix)):
        print(matrix[r])

def neighbors(node, adjmatrix):
    row = adjmatrix[node]
    list = []
    for x in range(len(row)):
        if row[x] == 1:
            list.append(x)
    return list
    
def q_good_coloring(adjmatrix, coloring):
    for node in range(len(adjmatrix)):
        neigh = neighbors(node,adjmatrix)
        clist = []
        for v in neigh:
            if coloring[v] == coloring[node]:
                return False
    return True
    
def next_coloring(coloring):
    max = len(coloring)-1
    for x in range(len(coloring)):
        if coloring[x] < len(coloring)-1:
            coloring[x] = coloring[x]+1
            break
        else:
            coloring[x] = 0
    return coloring

def next_coloring(coloring,kmax):
    """Return next, at most k-coloring"""
    for x in range(len(coloring)):
        if coloring[x] < kmax-1:
            coloring[x] = coloring[x]+1
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

def col_bf_k(adjmatrix,k):
    """Attempts to find k-coloring of given adjmatrix"""
    vertex_nr = len(adjmatrix)
    qgood = False
    coloring = [0 for x in range(vertex_nr)]
    for x in range(vertex_nr**k):
        if q_good_coloring(adjmatrix,coloring):
            qgood = True
            break
        coloring = next_coloring(coloring,k)
    return [qgood,coloring]

def col_bf_k_all(adjmatrix):
    """Return min coloring"""
    vertex_nr = len(adjmatrix)
    for k in range(1,vertex_nr+1):
        coloring = col_bf_k(adjmatrix,k)
        if coloring[0]:
            return coloring

def col_bf(adjmatrix):
    vertex_nr = len(adjmatrix)
    coloring = [0 for x in range(vertex_nr)]
    minnr_of_colors = vertex_nr
    mincoloring = list(range(minnr_of_colors))
    for x in range(minnr_of_colors**minnr_of_colors):
        if nr_of_colors(coloring) < minnr_of_colors:
            if q_good_coloring(adjmatrix,coloring):
                minnr_of_colors = nr_of_colors(coloring)
                mincoloring = coloring[:]
        coloring = next_coloring(coloring,vertex_nr)
    return mincoloring

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
    
def q_safe(vertex, color,adjmatrix, coloring):
    """Check if color may be assigned to vertex under given coloring"""
    for n in neighbors(vertex,adjmatrix):
        if color == coloring[n]:
            return False
    return True

def q_col_util(adjmatrix,kmax,coloring,vertex):
    vertex_nr = len(adjmatrix)
    if vertex == vertex_nr:
        return True
    for color in range(kmax):
        if q_safe(vertex,color,adjmatrix,coloring):
            coloring[vertex] = color
            if q_col_util(adjmatrix, kmax, coloring, vertex+1) == True:
                return True
            coloring[vertex] = -1
    return False

def col_backtracking(adjmatrix, kmax):
    vertex_nr = len(adjmatrix)
    coloring = [-1 for _ in range(vertex_nr)]
    for k in range(kmax):
        coloring = [-1 for _ in range(vertex_nr)]
        if q_col_util(adjmatrix, k, coloring, 0) == True:
            return coloring
    return coloring




#graph = RandomGraph(5,.5,3)
        
#printm(graph.adjmatrix)
#print('')
#timestart=time.clock()
#coloring = col_bf(graph.adjmatrix)
#print([q_good_coloring(graph.adjmatrix,coloring),coloring],time.clock()-timestart)
#timestart=time.clock()
#print(col_bf_k_all(graph.adjmatrix),time.clock()-timestart)

#timestart=time.clock()
#coloring = col_backtracking(graph.adjmatrix,graph.vertex_nr)
#print([q_good_coloring(graph.adjmatrix,coloring),coloring],time.clock()-timestart)

#timestart=time.clock()
#coloring = col_greedy(graph.adjmatrix)
#print([q_good_coloring(graph.adjmatrix,coloring),coloring],time.clock()-timestart)

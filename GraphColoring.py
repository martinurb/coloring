import random
random.seed(2)

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
    
def goodColoring(adjmatrix, coloring):
    for node in range(len(adjmatrix)):
        neigh = neighbors(node,adjmatrix)
        clist = []
        for v in neigh:
            if coloring[v] == coloring[node]:
                return False
    return True
    
def nextColoring(coloring):
    max = len(coloring)-1
    for x in range(len(coloring)):
        if coloring[x] < len(coloring)-1:
            coloring[x] = coloring[x]+1
            break
        else:
            coloring[x] = 0
    return coloring

def colorNr(coloring):
    colorlist = []
    for c in coloring:
        if c in colorlist:
            continue
        else:
            colorlist.append(c)
    return len(colorlist)
    
def BFcoloring(adjmatrix):
    coloring = [0 for x in range(len(adjmatrix))]
    minColorNr = len(coloring)
    mincoloring = list(range(minColorNr))
    for x in range(minColorNr**minColorNr):
        if colorNr(coloring) < minColorNr:
            if goodColoring(adjmatrix,coloring):
                minColorNr = colorNr(coloring)
                mincoloring = coloring[:]
        coloring = nextColoring(coloring)
    return mincoloring

def GreedyColoring(adjmatrix):
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
    
adjmatrix  = [[0 for x in xrange(5)] for x in xrange(5)] 
coloring = [0,1,2,0,1]
for x in range(5):
    adjmatrix[x][x] = 0
    for y in range(x+1,5):
        el = random.randint(0,1)
        adjmatrix[x][y] = el
        adjmatrix[y][x] = el
        
#printm(adjmatrix)

#print(neighbors(0,adjmatrix))
#print(goodColoring(adjmatrix,coloring))
printm(adjmatrix)
print('')
print(BFcoloring(adjmatrix))
print(GreedyColoring(adjmatrix))
print(goodColoring(adjmatrix,GreedyColoring(adjmatrix)))
#print(goodColoring(adjmatrix,[2,1,0,1,0]))
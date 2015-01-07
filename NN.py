from sympy.functions.special.tensor_functions import KroneckerDelta
import numpy as np
import random
from copy import copy, deepcopy
import GraphColoring as gc
import time


def deltaE(vS,i,c,gamma):
    sum = 0
    for j in range(len(vS)):
        sum += A[i,j]*(KroneckerDelta(c,vS[j])-KroneckerDelta(vS[i],vS[j]))+\
            gamma*(c - vS[i])
    return sum

def delta2_Ei(i,vS_new,vS_old,gamma):
    sum = 0
    for j in range(len(vS_new)):
        sum += A[i,j]*(KroneckerDelta(vS_old[i],vS_new[j])\
            -KroneckerDelta(vS_new[i],vS_new[j]))+\
            gamma*(vS_old[i] - vS_new[i])
    return sum

def delta2_Ej(i,j,c,vS_new,vS_old,gamma):
    return KroneckerDelta(c,vS_new[i])\
        -KroneckerDelta(vS_new[j],vS_new[i])\
        -KroneckerDelta(c,vS_old[i])\
        +KroneckerDelta(vS_new[j],vS_old[i])\
    

def update_deltaE(i,c,vS_new,vS_old,dE,gamma,k):
    """updates dE and returns new dE as a result of color change in vS_new"""
    d2Ei = [delta2_Ei(i,vS_new,vS_old,gamma) for cp in range(1,k+1)]
    dEm = dE
    dEm[i] += np.array(d2Ei)
    neigh = gc.neighbors(i,A)
    for j in neigh:
        d2Ej = [delta2_Ej(i,j,cp,vS_new,vS_old,gamma) for cp in range(1,k+1)]
        dEm[j] += np.array(d2Ej)
    return dEm


def compute_DeltaE(vS,k,gamma):
    """returns matrix dE(i,c) of energy differences between vS and vS with 
    node i changed with color c"""
    N = len(vS)
    return np.array([[deltaE(vS,i,c,gamma) for c in range(1,k+1)]\
        for i in range(N)])
            

def f_greedy(dE,k):
    """returns [i - node,c - color] corresponding to min dE(i,c)<0. 
    If min dE(i,c) > 0 returns [-1,-1]"""
    [i,c] = [dE.argmin() // k, dE.argmin() % k + 1]
    if dE.min() >= -1e-10:
        return [-1,-1]
    else:
        return [i, c]

def inner_loop(vS, k, gamma):
    """returns feasible coloring corresponding 
    to local energy minimum. vS is starting coloring, k is max coloring nr,
    k = Delta(G)+1 where Delta(G) is maximum degree in the graph G, 
    gamma is a number gamma < 1/(Delta(G)*(Delta(G)+1)) to ensure that 
    all minima in the function are feasible solutions"""
    dE = compute_DeltaE(vS,k,gamma)
    [i, c] = f_greedy(dE,k)
    while i != -1:
        vS_old = vS.copy()
        vS[i] = c
        #dE = compute_DeltaE(vS,k,gamma) #slower
        dE = update_deltaE(i,c,vS,vS_old,dE,gamma,k) #faster
        [i, c] = f_greedy(dE,k)
    return vS

def annealing_loop(vS,k,gammaL,gammaH):
    vS = inner_loop(vS,k,gammaL)
    while True:
        vS_old = vS
        vS = inner_loop(vS,k,gammaH)
        vS = inner_loop(vS,k,gammaL)
        if energy(vS_old,gammaL) <= energy(vS,gammaL):
            break
    return vS_old


def gammaH_found(vS,vSbase,f):
    """gammaH is correct if nr of colors is <= f*nr of colors in feasible
    solution"""
    if len(set(vS)) <= len(set(vSbase))*f:
        return True
    else:
        return False

def randomS(k,N):
    return np.array([random.randrange(1,k+1) for _ in range(N)])

def find_gammaH(gammaL,k,f):
    vSbase = randomS(k,len(A))
    vS = randomS(k,len(A))
    gamma = gammaL
    deltaG = gammaL
    vSbase = inner_loop(vS,k,gamma).copy()
    while True:
        gamma += deltaG
        vS = inner_loop(vS,k,gamma)
        if gammaH_found(vS,vSbase,f):
            break
    return gamma

def max_degree(A):
    return max([row.sum() for row in A])

def energy(vS,gamma):
    sum = 0
    N = len(A)
    for i in range(N):
        for j in range(N):
            sum += A[i][j]*KroneckerDelta(vS[i],vS[j])
        sum += gamma*vS[i]
    return sum


def outer_loop(restarts,f):
    N = len(A)
    d = max_degree(A)
    k = d + 1
    vSbest = randomS(k,N).copy()
    gammaL = 1./(d*(d+1))
    gammaH = find_gammaH(gammaL,k,f)
    for r in range(restarts):
        vS = randomS(k,N)
        vS = annealing_loop(vS,k,gammaL,gammaH)
        if(energy(vS,gammaL) < energy(vSbest,gammaL)):
            vSbest = vS.copy()
        print(vS,vSbest)
    return vSbest


random.seed(1);
A = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
vS0 = [1,1,1,1]
graph = gc.RandomGraph(20,.7,1)
A = np.array(graph.adjmatrix)
d = max_degree(A)
k = d+1
gamma = 1./(d*(d+1))
vS0 = randomS(k,len(A))
print(gc.q_good_coloring(A,vS0),vS0)
timestart=time.clock()
vS = inner_loop(vS0,k,gamma)
print(gc.q_good_coloring(A,vS),vS,time.clock()-timestart)
timestart=time.clock()
vS = outer_loop(10,.75)
print(gc.q_good_coloring(A,vS),vS,time.clock()-timestart)
# -*- coding=utf8 -*-
from sympy.functions.special.tensor_functions import KroneckerDelta
from GraphUtils import *
import numpy as np
import random
from copy import copy, deepcopy
import time


class NetworkColoring:
    """Given graph as adj matrix, returns coloring
    recieved by Network algorithm"""
    def __init__(self, graph):
        self.naive_coloring = color_greedy(graph)
        self.max_colors = nr_of_colors(self.naive_coloring)

        self.adjlist = graph.adjlist
        self.adjmatrix = graph.adjmatrix
        self.A = self.adjmatrix
        self.vertex_nr = len(self.adjlist)
        self.max_degree = max([row.sum() for row in self.A])

    def deltaE(self,vS,i,c,gamma):
        sum = 0
        for j in range(self.vertex_nr):
            sum += self.A[i,j]*(KroneckerDelta(c,vS[j])-KroneckerDelta(vS[i],vS[j]))+\
                gamma*(c - vS[i])
        return sum

    def delta2_Ei(self,i,vS_new,vS_old,gamma):
        sum = 0
        for j in range(self.vertex_nr):
            sum += self.A[i,j]*(KroneckerDelta(vS_old[i],vS_new[j])\
                -KroneckerDelta(vS_new[i],vS_new[j]))+\
                gamma*(vS_old[i] - vS_new[i])
        return sum

    def delta2_Ej(self,i,j,c,vS_new,vS_old,gamma):
        return KroneckerDelta(c,vS_new[i])\
            -KroneckerDelta(vS_new[j],vS_new[i])\
            -KroneckerDelta(c,vS_old[i])\
            +KroneckerDelta(vS_new[j],vS_old[i])\
    
    def update_deltaE(self,i,c,vS_new,vS_old,dE,gamma,k):
        """updates dE and returns new dE as a result of color change in vS_new"""
        d2Ei = [self.delta2_Ei(i,vS_new,vS_old,gamma) for cp in range(1,k+1)]
        dEm = dE
        dEm[i] += np.array(d2Ei)
        neigh = neighbors(i,self.A)
        for j in neigh:
            d2Ej = [self.delta2_Ej(i,j,cp,vS_new,vS_old,gamma)\
                for cp in range(1,k+1)]
            dEm[j] += np.array(d2Ej)
        return dEm


    def compute_DeltaE(self,vS,k,gamma):
        """returns matrix dE(i,c) of energy differences between vS and vS with 
        node i changed with color c"""
        N = self.vertex_nr
        return np.array([[self.deltaE(vS,i,c,gamma) for c in range(1,k+1)]\
            for i in range(N)])
            

    def f_greedy(self,dE,k):
        """returns [i - node,c - color] corresponding to min dE(i,c)<0. 
        If min dE(i,c) > 0 returns [-1,-1]"""
        [i,c] = [dE.argmin() // k, dE.argmin() % k + 1]
        if dE.min() >= -1e-10:
            return [-1,-1]
        else:
            return [i, c]

    def inner_loop(self,vS, k, gamma):
        """returns feasible coloring corresponding 
        to local energy minimum. vS is starting coloring, k is max coloring nr,
        k = Delta(G)+1 where Delta(G) is maximum degree in the graph G, 
        gamma is a number gamma < 1/(Delta(G)*(Delta(G)+1)) to ensure that 
        all minima in the function are feasible solutions"""
        dE = self.compute_DeltaE(vS,k,gamma)
        [i, c] = self.f_greedy(dE,k)
        while i != -1:
            vS_old = vS.copy()
            vS[i] = c
            #dE = compute_DeltaE(vS,k,gamma) #slower
            dE = self.update_deltaE(i,c,vS,vS_old,dE,gamma,k) #faster
            [i, c] = self.f_greedy(dE,k)
        return vS

    def annealing_loop(self,vS,k,gammaL,gammaH):
        vS = self.inner_loop(vS,k,gammaL)
        while True:
            vS_old = vS
            vS = self.inner_loop(vS,k,gammaH)
            vS = self.inner_loop(vS,k,gammaL)
            if self.energy(vS_old,gammaL) <= self.energy(vS,gammaL):
                break
        return vS_old


    def gammaH_found(self,vS,vSbase,f):
        """gammaH is correct if nr of colors is <= f*nr of colors in feasible
        solution"""
        if len(set(vS)) <= len(set(vSbase))*f:
            return True
        else:
            return False

    def randomS(self,k,N):
        return np.array([random.randrange(1,k+1) for _ in range(N)])

    def find_gammaH(self,gammaL,k,f):
        vSbase = self.randomS(k,len(self.A))
        vS = self.randomS(k,len(self.A))
        gamma = gammaL
        deltaG = gammaL
        vSbase = self.inner_loop(vS,k,gamma).copy()
        while True:
            gamma += deltaG
            vS = self.inner_loop(vS,k,gamma)
            if self.gammaH_found(vS,vSbase,f):
                break
        return gamma

    def energy(self,vS,gamma):
        sum = 0
        N = len(self.A)
        for i in range(N):
            for j in range(N):
                sum += self.A[i][j]*KroneckerDelta(vS[i],vS[j])
            sum += gamma*vS[i]
        return sum

    def outer_loop(self,restarts,f):
        N = self.vertex_nr
        d = self.max_degree
        k = d + 1
        vSbest = self.randomS(k,N).copy()
        gammaL = 1./(d*(d+1))
        gammaH = self.find_gammaH(gammaL,k,f)
        for r in range(restarts):
            vS = self.randomS(k,N)
            vS = self.annealing_loop(vS,k,gammaL,gammaH)
            if(self.energy(vS,gammaL) < self.energy(vSbest,gammaL)):
                vSbest = vS.copy()
            #print("current:",vS,"best:",vSbest)
        return dict((i+1,vSbest[i]) for i in range(self.vertex_nr))


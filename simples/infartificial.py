import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()


numyears = 20000

eps = 0.01#eps 0.1/0.11 alpha 0.06

alpha = 0.06

T1 = 15
T2 = 14


L = 8
l = 3
deg = 1

method = 'killall'

landscape = nx.Graph()

rho = {}

for i in range(L + deg):
	rho.update({i:[]})

for i in range(L-1):
    landscape.add_node(i)

landscape.add_node(L-1)

for i in range(deg):
    landscape.add_node(L + i)

for i in range(L-1):
    landscape.add_edge(i, i + 1)
    
landscape.add_edge(0,0)

for i in range(L - l - 1):
    for j in range(deg):
        landscape.add_edge(i + l, L + j)

#nx.draw(landscape)
#plt.show()

population = [1.0 if k == 0 else 0 for k in range(L + deg)]


def printtofile():
    for i in range(L + deg):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()
    
def kill():
    for i in range(L + deg):
        population[i] *= (1.0 - alpha)


def divideboth(method):

    global population
    numorgs = 0.0


    
    nextpop = [0.0 for i in range(L + deg)]
    for g in range(L):
        for v in landscape.neighbors(g):
            nextpop[v] += population[g]*eps/len(landscape.neighbors(g))
        nextpop[g] += population[g]*(1 - eps)

    numorgs = sum(population) + sum(nextpop)
        
    matar = numorgs - 1.0 if numorgs > 1.0 else 0.0
        
    if method == 'killall':
        for k in range(L + deg):
            population[k] *= (1.0 - matar)
            

        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
            population[i] += nextpop[i]

        for k in range(L + deg):
            population[k] /= numorgs
            
    if method == 'fraction':
        empty = 1.0 - sum(population)
        frac = empty
        nextgen = [0.0 for j in range(L + deg)]
        
        for i in range(L + deg):
            nextgen[i] += nextpop[i]*frac

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        for i in range(L + deg):
            population[i] *= (1.0 - alpha)


def divide1(method):

    global population
    numorgs = 0.0
    
    nextpop = [0.0 for i in range(L + deg)]
    for g in range(L - 1):
        for v in landscape.neighbors(g):
            nextpop[v] += population[g]*eps/len(landscape.neighbors(g))
        nextpop[g] += population[g]*(1 - eps)

    numorgs = sum(population) + sum(nextpop)
        
    matar = numorgs - 1.0 if numorgs > 1.0 else 0.0
        
    if method == 'killall':
        for k in range(L + deg):
            population[k] *= (1.0 - matar)
            

        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
            population[i] += nextpop[i]


        for k in range(L + deg):
            population[k] /= numorgs
            
    if method == 'fraction':
        empty = 1.0 - sum(population)
        frac = empty
        nextgen = [0.0 for j in range(L + deg)]
        
        for i in range(L + deg):
            nextgen[i] += nextpop[i]*frac

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        for i in range(L + deg):
            population[i] *= (1.0 - alpha)


def divide2(method):

    global population
    numorgs = 0.0


    
    nextpop = [0.0 for i in range(L + deg)]

    for v in landscape.neighbors(L-1):
        nextpop[v] += population[L-1]*eps/len(landscape.neighbors(L-1))
    nextpop[L-1] += population[L-1]*(1 - eps)

    numorgs = sum(population) + sum(nextpop)
        
    matar = numorgs - 1.0 if numorgs > 1.0 else 0.0


    if method == 'killall':
        for k in range(L + deg):
            population[k] *= (1.0 - matar)
            

        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
            population[i] += nextpop[i]


        for k in range(L + deg):
            population[k] /= numorgs
            
    if method == 'fraction':
        empty = 1.0 - sum(population)
        frac = empty
        nextgen = [0.0 for j in range(L + deg)]
        
        for i in range(L + deg):
            nextgen[i] += nextpop[i]*frac

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        for i in range(L + deg):
            population[i] *= (1.0 - alpha)

def showplots():
    plt.plot(range(len(rho[0])), rho[0], '#0000ff')
    plt.plot(range(len(rho[1])), rho[1], '#bb00ee')
    plt.plot(range(len(rho[2])), rho[2], '#cc0044')
    plt.plot(range(len(rho[3])), rho[3], '#ee6600')
    plt.plot(range(len(rho[4])), rho[4], '#ff8800')
    plt.plot(range(len(rho[5])), rho[5], '#ffcc00')
    plt.plot(range(len(rho[6])), rho[6], '#ccee00')
    plt.plot(range(len(rho[7])), rho[7], '#00cc44')
    plt.plot(range(len(rho[8])), rho[8], '#000000')

    
##    plt.plot(range(len(rho[L-1])), rho[L-1])
##    plt.plot(range(len(rho[L-2])), rho[L-2])
##    for i in range(L + deg):
##        if i == L-1 or i == 0 or i == L-2:
##            continue
##        plt.plot(range(len(rho[i])), rho[i])
    plt.show()
            

def rhoupdate(population):
    for i in range(L + deg):
        rho[i].append(population[i])


def continuefor(numy, lastend):
   for t in [lastend + r for r in range(numy)]:
        rhoupdate(population)
        if (t+1)%1000 == 0:
            print 'ano = ' + str(t+1)
        if (t+1)%T1 == 0 and (t+1)%T2 == 0:
            divideboth(method)
            continue
        if (t+1)%T1 == 0:
            divide1(method)
            continue
        if (t+1)%T2 == 0:
            divide2(method)
            continue
        if method == 'fraction':
            kill()

for t in range(numyears):
    rhoupdate(population)
    if (t+1)%1000 == 0:
            print 'ano = ' + str(t+1)
    if (t+1)%T1 == 0 and (t+1)%T2 == 0:
        divideboth(method)
        continue
    if (t+1)%T1 == 0:
        divide1(method)
        continue
    if (t+1)%T2 == 0:
        divide2(method)
        continue
    if method == 'fraction':
        kill()
        


tb = time.time()

print 'tempo de execucao: ' + str(tb-ta)


showplots()

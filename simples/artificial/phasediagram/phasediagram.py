import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()


numyears = 20000



T1 = 4
T2 = 3

alpha = 0.01

method = 'fraction'



def printtofile():
    for i in range(2):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()

def nextstep(method, t):
    nextpop = [0.0 for l in range(2)]


    if method == 'killall':
        nextpop[0] += (population[0]*(1-eps) if t%T1 == 0 else 0.0)
        nextpop[0] += (population[1]*eps if t%T2 == 0 else 0.0)
        nextpop[1] += (population[1]*(1-eps) if t%T2 == 0 else 0.0)
        nextpop[1] += (population[0]*eps if t%T1 == 0 else 0.0)

        kill = nextpop[0] + nextpop[1]
        for i in range(2):
            population[i] = population[i]*(1-kill) + nextpop[i]

    elif method == 'fraction':
        nextpop[0] = population[0]
        nextpop[1] = population[1]
        frac = 1.0-population[0]-population[1]
        nextpop[0] += (population[0]*(1-eps)*frac if t%T1 == 0 else 0.0)
        nextpop[0] += (population[1]*eps*frac if t%T2 == 0 else 0.0)
        nextpop[1] += (population[1]*(1-eps)*frac if t%T2 == 0 else 0.0)
        nextpop[1] += (population[0]*eps*frac if t%T1 == 0 else 0.0)
            
        for i in range(2):
            population[i] = nextpop[i]*(1-alpha)
        
    else:
        nextpop[0] += (population[0]*(1-eps) if t%T1 == 0 else 0.0)
        nextpop[0] += (population[1]*eps if t%T2 == 0 else 0.0)
        nextpop[1] += (population[1]*(1-eps) if t%T2 == 0 else 0.0)
        nextpop[1] += (population[0]*eps if t%T1 == 0 else 0.0)
        
        kill = nextpop[0] + nextpop[1]
        for i in range(2):
            population[i] = (population[i] + nextpop[i])/(1+kill)

    

def showplots():
    for i in range(2):
        plt.plot(range(len(rho[i])), rho[i])
        plt.title('serie ' + str(i))
        plt.show()
            

def rhoupdate(population):
    for i in range(2):
        rho[i].append(population[i])


def plotall():
    for i in range(2):
        plt.plot(range(len(rho[i])), rho[i])
        
    plt.show()    


def nucleate(population):
    for t in range(numyears):
        rhoupdate(population)
        nextstep(method, t)
    if rho[1][-1] > 0.5:
        return True
    else:
        return False


step = 0.0005
fine = 0.0005

crit = []
flag = True
bc = 0.0

error = 0.3

lmin = 0.0
lmax = 0.3

emax = 0.032

for eps in [i*step for i in range(int(emax/step))]:
    print 'eps = ' + str(eps)
    while error > fine:
        b = (lmin + lmax)/2
        print 'bubble = ' + str(b)
        rho = {0:[],1:[]}
        population = [1-b, b]
        if nucleate(population):
            lmax = b
        else:
            lmin = b

        error = (lmax - lmin)/2


    crit.append((lmax + lmin)/2)
    flag = True
    error = 0.3
    lmin = 0.0
    lmax = 0.3


plt.plot([i*step for i in range(int(emax/step))],crit)
plt.show()


tb = time.time()

print 'tempo de execucao: ' + str(tb-ta)


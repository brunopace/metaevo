import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()


numyears = 20000


eps = 0.02    #0.0174

T1 = 5
T2 = 4

alpha = 0.01

method = 'fraction'

bolha = 0.0

rho = {0:[],1:[]}

population = [1-bolha if k == 0 else bolha for k in range(2)]



def printtofile():
    for i in range(2):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()

def kill():
    for i in range(2):
        population[i] = population[i]*(1-alpha)

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

    if method == 'fraction':
        nextpop[0] = population[0]
        nextpop[1] = population[1]
        frac = 1.0-population[0]-population[1]
        nextpop[0] += (population[0]*(1-eps)*frac if t%T1 == 0 else 0.0)
        nextpop[0] += (population[1]*eps*frac if t%T2 == 0 else 0.0)
        nextpop[1] += (population[1]*(1-eps)*frac if t%T2 == 0 else 0.0)
        nextpop[1] += (population[0]*eps*frac if t%T1 == 0 else 0.0)
            
        for i in range(2):
            population[i] = nextpop[i]
        
    if method == 'overlap':
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


for t in range(numyears):
    rhoupdate(population)
    if (t)%1000 == 0:
            print 'ano = ' + str(t)
    nextstep(method, t)
    if method == 'fraction':
        kill()




        


tb = time.time()

print 'tempo de execucao: ' + str(tb-ta)


plotall()

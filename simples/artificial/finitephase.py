import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()

N = 5000

numyears = 5000

eps = 0.005
alpha = 0.05

T1 = 5
T2 = 4

method = 'fraction'


rho = {}
for i in range(T1+T2):
    rho.update({i:[]})


population = [N if k == 0 else 0 for k in range(T1+T2)]


def printtofile():
    for i in range(2):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()

def kill():

    p = [population[j] for j in range(T1+T2)]

    nichttot = sum(p)
    
    for o in range(nichttot):
        if rndm.random() < alpha:
            i = 0
            fila = p[0]
            while o > fila:
                i += 1
                fila += p[i]
            while population[i] == 0 :
                i += 1
            population[i] -= 1


def divideboth(method, na, nb):

    global population
    numorgs = 0

    nextpop = [0 for i in range(T1+T2)]
    
    for g in [na, T1+nb]:
        for n in range(population[g]):
            r = rndm.random()
            if r < eps:
                nextpop[T1+nb if g == na else na] += 1
            else:
                nextpop[g] += 1




    for k in population:
        numorgs += k
    for k in nextpop:
        numorgs += k

       
    matar = numorgs - N if numorgs > N else 0

    if method == 'killall':
        for k in range(matar):
            y = -1
            people = 0
            guy = rndm.randint(1, N - k)
            while people < guy:
                y += 1
                people += population[y]
            population[y] -= 1

        for i in range(T1+T2):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(T1+T2):
            population[i] += nextpop[i]


        for k in range(matar):
            y = -1
            people = 0
            guy = rndm.randint(1, N + matar - k)
            while people < guy:
                y += 1
                people += population[y]
            population[y] -= 1
            
    if method == 'fraction':
        empty = float(N)
        for i in range(T1 + T2):
            empty -= population[i]
        frac = empty/N
        nextgen = [0 for i in range(T1 + T2)]

        total = 0

        for i in range(T1 + T2):
            for c in range(nextpop[i]):
                if rndm.random() < frac:
                    nextgen[i] += 1
                    total += 1

##        while total > empty:
##            r = rndm.randint(0, total - 1)
##            fila = nextgen[0]
##            i = 0
##            while r > fila:
##                i += 1
##                fila += nextgen[i]
##            nextgen[i] -=1
##            total -=1

        for i in range(T1 + T2):
            population[i] += nextgen[i]



def showplots():
    for i in range(T1+T2):
        plt.plot(range(len(rho[i])), rho[i])
        plt.title('serie ' + str(i))
        plt.show()

def plotall():
    for i in range(T1+T2):
        plt.plot(range(len(rho[i])), rho[i])
        
    plt.show() 
            

def rhoupdate(population):
    for i in range(T1+T2):
        rho[i].append(population[i])


def continuefor(numy, lastend):
   for t in [lastend + r for r in range(numy)]:
        rhoupdate(population)
        if (t+1)%1000 == 0:
            print 'ano = ' + str(t+1)
        divideboth(method, t%T1, t%T2)
    
for t in range(numyears):
    rhoupdate(population)
    if (t)%1000 == 0:
            print 'ano = ' + str(t)
    divideboth(method, t%T1, t%T2)
    if method == 'fraction':
        kill()


tb = time.time()

print 'tempo de execucao: ' + str(tb-ta)


plotall()

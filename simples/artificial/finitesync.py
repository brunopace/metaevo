import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()

N = 5000    #killall, N50000 b1700 eps0.0001   5/4?
b = 0

numyears = 10000
                     #fraction N5000  b0   eps0.03  alpha0.01   5/4
eps = 0.01     
alpha = 0.02

T1 = 5
T2 = 4

method = 'fraction'

landscape = nx.Graph()

rho = {0:[],1:[]}

landscape.add_node(0)
landscape.add_node(1)    
landscape.add_edge(0,1)


#nx.draw(landscape)
#plt.show()

population = [N-b,b]


def printtofile():
    for i in range(2):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()
    

def divideboth(method):
    global population
    numorgs = 0


    
    nextpop = [0 for i in range(2)]
    for g in range(2):
        for n in range(population[g]):
            r = rndm.random()
            if r < eps:
                nextpop[rndm.choice(landscape.neighbors(g))] += 1
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


        for i in range(2):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(2):
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
        
        empty = float(N - population[0] - population[1])
        frac = empty/N
        nextgen = [0,0]
        
        for i in range(2):
            for c in range(nextpop[i]):
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(2):
            population[i] += nextgen[i]

        nichttot = population[0] + population[1]
        p0 = population[0]

        
        for o in range(nichttot):
            if rndm.random() < alpha:
                if o < p0:
                    population[0] -= 1
                else:
                    population[1] -= 1
            
                    
        



def divide1(method):
    global population

    numorgs = 0
    
    nextpop = [0 for i in range(2)]

    for n in range(population[0]):    #para todos os organismos com o g
        r = rndm.random()
        if r < eps:
            nextpop[rndm.choice(landscape.neighbors(0))] += 1
        else:
            nextpop[0] += 1




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


        for i in range(2):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(2):
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
        
        empty = float(N - population[0] - population[1])
        frac = empty/N
        nextgen = [0,0]
        
        for i in range(2):
            for c in range(nextpop[i]):     #a proxima geracao sobrevive proporcionalmente aos espacos livres
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(2):
            population[i] += nextgen[i]

        nichttot = population[0] + population[1]
        p0 = population[0]

        
        for o in range(nichttot):
            if rndm.random() < alpha:
                if o < p0:
                    population[0] -= 1
                else:
                    population[1] -= 1


def divide2(method):
    global population
    numorgs = 0
    
    nextpop = [0 for i in range(2)]
    for n in range(population[1]):
        r = rndm.random()
        if r < eps:
            nextpop[rndm.choice(landscape.neighbors(1))] += 1
        else:
            nextpop[1] += 1
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


        for i in range(2):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(2):
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
        
        empty = float(N - population[0] - population[1])
        frac = empty/N
        nextgen = [0,0]
        
        for i in range(2):
            for c in range(nextpop[i]):     #a proxima geracao sobrevive proporcionalmente aos espacos livres
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(2):
            population[i] += nextgen[i]

        nichttot = population[0] + population[1]
        p0 = population[0]
        
        for o in range(nichttot):
            if rndm.random() < alpha:
                if o < p0:
                    population[0] -= 1
                else:
                    population[1] -= 1

def kill():
    nichttot = population[0] + population[1]
    p0 = population[0]
    
    for o in range(nichttot):
        if rndm.random() < alpha:
            if o < p0:
                population[0] -= 1
            else:
                population[1] -= 1

def showplots():
    for i in range(2):
        plt.plot(range(len(rho[i])), rho[i])
        plt.title('serie ' + str(i))
        plt.show()
            
def showtogether():
    plt.plot(range(len(rho[0])), rho[0], range(len(rho[1])), rho[1])
    plt.title('Altogether')
    plt.show()


def rhoupdate(population):
    for i in range(2):
        rho[i].append(population[i])


def continuefor(numy, lastend):
   for t in [lastend + r for r in range(numy)]:
        rhoupdate(population)
        if (t+1)%1000 == 0:
            print 'ano = ' + str(t+1)
        if (t+1)%T1 == 0 and t%T2 == 0:
            divideboth(method)
            continue
        if (t+1)%T1 == 0:
            divide1(method)
        if (t+1)%T2 == 0:
            divide2(method)        

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
    kill()

        


tb = time.time()

print 'tempo de execucao: ' + str(tb-ta)


#showplots()
showtogether()

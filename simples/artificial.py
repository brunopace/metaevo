import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()

N = 5000

numyears = 20000

eps = 0.05   #acima de 0.26 nao eh estavel

alpha = 0.06

T1 = 4
T2 = 3


L = 8
l = 3
deg = 1

method = 'fraction'

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

nx.draw(landscape, node_color=['#0000ff','#bb00ee','#cc0044','#ee6600','#ff8800','#ffcc00','#ccee00','#00cc44','#666666'])
plt.show()

population = [N if k == 0 else 0 for k in range(L + deg)]


def printtofile():
    for i in range(L + deg):
        fobj = open('artificial/'+ method + '/'+ 'eps'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'_'+str(i)+'.dat', 'a')
        for t in range(len(rho[i])):
            fobj.write(str(t+1) + '    ' + str(rho[i][t]) + '\n')
        fobj.close()


def kill():

    nichttot = sum(population)
    p = [population[j] for j in range(L + deg)]
    for o in range(nichttot):
        if rndm.random() < alpha:
            i = 0
            fila = p[0]
            while o > fila:
                i += 1
                fila += p[i]
            while population[i] == 0:
                i += 1
            population[i] -= 1

def divideboth(method):

    global population
    numorgs = 0


    
    nextpop = [0 for i in range(L + deg)]
    for g in range(L):
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


        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
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
        empty = N - sum(population)
        frac = float(empty)/N
        nextgen = [0 for j in range(L + deg)]
        
        for i in range(L + deg):
            for c in range(nextpop[i]):
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        kill()
        
##        nichttot = sum(population)
##        p = [population[j] for j in range(L + deg)]
##
##        for o in range(nichttot):
##            if rndm.random() < alpha:
##                i = 0
##                fila = p[0]
##                while o > fila:
##                    i += 1
##                    fila += p[i]
##                while population[i] == 0:
##                        i += 1
##                
##                population[i] -= 1


def divide1(method):

    global population

    numorgs = 0
    
    nextpop = [0 for i in range(L + deg)]

    for g in range(L-1):            #para todos os L-1 primeiros genotipos
        for n in range(population[g]):    #para todos os organismos com o g
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


        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
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
        empty = N - sum(population)
        frac = float(empty)/N
        nextgen = [0 for j in range(L + deg)]
        
        for i in range(L + deg):
            for c in range(nextpop[i]):
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        kill()
        
##        nichttot = sum(population)
##        p = [population[j] for j in range(L + deg)]
##
##        for o in range(nichttot):
##            if rndm.random() < alpha:
##                i = 0
##                fila = p[0]
##                while o > fila:
##                    i += 1
##                    fila += p[i]
##                while population[i] == 0:
##                        i += 1
##                population[i] -= 1



def divide2(method):

    global population
    numorgs = 0
    
    nextpop = [0 for i in range(L + deg)]
    for n in range(population[L-1]):
        r = rndm.random()
        if r < eps:
            nextpop[rndm.choice(landscape.neighbors(L-1))] += 1
        else:
            nextpop[L-1] += 1
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


        for i in range(L + deg):
            population[i] += nextpop[i]

    if method == 'overlap':
        for i in range(L + deg):
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
        empty = N - sum(population)
        frac = float(empty)/N
        nextgen = [0 for j in range(L + deg)]
        
        for i in range(L + deg):
            for c in range(nextpop[i]):
                if rndm.random() < frac:
                    nextgen[i] += 1

##        while nextgen[0] + nextgen[1] > empty:
##            r = rndm.randint(0, nextgen[0] + nextgen[1] - 1)
##            if r < nextgen[0]:
##                nextgen[0] -= 1
##            else:
##                nextgen[1] -= 1

        for i in range(L + deg):
            population[i] += nextgen[i]

        kill()

##
##        nichttot = sum(population)
##        p = [population[j] for j in range(L + deg)]
##
##        for o in range(nichttot):
##            if rndm.random() < alpha:
##                i = 0
##                fila = p[0]
##                while o > fila:
##                    i += 1
##                    fila += p[i]
##                while population[i] == 0:
##                        i += 1
##                population[i] -= 1

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

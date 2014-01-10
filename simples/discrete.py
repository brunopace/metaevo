import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random as rndm
import time

ta = time.time()

division_threshold = 10 
order = [[1,1], [0,1], [0,0], [1,0]]
peso = 0.1388         # peso < 0.138888  
envchg_period = 12

eps = 0.008#   para peso = 0.1388, N = 100, eps <= 0.1 eh estavel o pico (1,1,0,1)

alpha = 0.001    #0.01 eh grande!

method = 'fraction' 

N = 100

reflect = True
limits = [-5, 4]

numyears = 10000

numsims = 1
showplots = True
writefile = False

peekbubble = (0,0,1,0)               #atrator errado (-1,-1,0,-5)
peek = (0,0,1,0)

bubble = 0

LIXO = [3, 4, 13, 14, 24, 34, 44, 65, 75, 85, 94, 104, 185, 195]
SD = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 45, 46, 47, 48, 49, 55, 56, 57, 58, 59, 66, 67, 68, 69, 76, 77, 78, 79, 86, 87, 88, 89, 95, 96, 97, 98, 99, 105, 106, 107, 108, 109, 115, 116, 117, 118, 119, 125, 126, 127, 128, 129, 135, 136, 137, 138, 139, 146, 147, 148, 149, 156, 157, 158, 159, 166, 167, 168, 169, 176, 177, 178, 179, 186, 187, 188, 189, 196, 197, 198, 199, 206, 207, 208, 209, 216, 217, 218, 219, 226, 227, 228, 229, 236, 237, 238, 239, 247, 248, 249, 257, 258, 259, 267, 268, 269]
SL = [0, 1, 10, 11, 12, 20, 21, 22, 23, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54, 60, 61, 62, 70, 71, 72, 73, 80, 81, 82, 83, 84, 90, 91, 92, 100, 101, 102, 103, 110, 111, 112, 113, 114, 120, 121, 122, 123, 130, 131, 132, 133, 134, 140, 141, 142, 143, 144, 145, 150, 151, 152, 153, 160, 161, 162, 163, 164, 170, 171, 172, 173, 174, 175, 180, 181, 182, 190, 191, 192, 193, 200, 201, 202, 203, 204, 210, 211, 212, 213, 220, 221, 222, 223, 224, 230, 231, 232, 233, 234, 235, 240, 241, 242, 243, 250, 251, 252, 253, 254, 260, 261, 262, 263, 264, 265]
OSCV = [2, 33, 64, 93, 124, 155, 184, 215, 246]
VL = [63, 74, 154, 165, 183, 194, 205, 214, 225, 244, 245, 255, 256, 266]

VL1 = [63, 183, 244]
VL2 = [74, 154, 194, 214, 255]
VL3 = [165, 205, 225, 245, 266]
VL4 = [256]

CIs = [145]
OR = [165, 225]
SADDLE = [255]
PATH = [265, 266]


#CI = [{'genotype': peekbubble, 'state': 1, 'biomass': division_threshold/2.0} for i in range(bubble)] + [{'genotype': peek, 'state': 1, 'biomass': division_threshold/2.0} for i in range(N - bubble)]
#CI = [{'genotype': peek, 'state': 1, 'biomass': division_threshold/2.0}] + [None for i in range(N-1)]
#CI = [{'genotype': (-1,-1,0,-5), 'state': 1, 'biomass': division_threshold/2.0} for i in range(200)] + [{'genotype': (-1,-1,0,-4), 'state': 1, 'biomass': division_threshold/2.0} for i in range(200)] + [{'genotype': (-1,-1,0,-3), 'state': 1, 'biomass': division_threshold/2.0} for i in range(200)]+ [{'genotype': (-1,1,0,-2), 'state': 1, 'biomass': division_threshold/2.0} for i in range(200)]

population = [{'genotype': peekbubble, 'state': 1, 'biomass': division_threshold/2.0} for i in range(bubble)] + [{'genotype': peek, 'state': 1, 'biomass': division_threshold/2.0} for i in range(N - bubble)]
rho = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}


def indextogenotype(i):
    genot = [-1,-1,-1,-5]
    while i >= 90:
        genot[0] +=1
        i -= 90
    while i >= 30:
        genot[1] +=1
        i -= 30
    while i >= 10:
        genot[2] +=1
        i -= 10
    while i >= 1:
        genot[3] +=1
        i -= 1
    return tuple(genot)

def genotypetoindex(genotype):
    idx = 0
    gen = list(genotype)
    while gen[0] > -1:
        idx += 90
        gen[0] -= 1
    while gen[1] > -1:
        idx += 30
        gen[1] -= 1
    while gen[2] > -1:
        idx += 10
        gen[2] -= 1
    while gen[3] > -5:
        idx += 1
        gen[3] -= 1
    return idx

def printtofile(w2, w3, w7, w8, typ = '', countr = None):
    fobj = open('data/'+typ+'w'+str(peso).split('.')[0]+str(peso).split('.')[1]+'e'+str(eps).split('.')[0]+str(eps).split('.')[1]+'N'+str(N)+'s'+str(numsims)+'.dat', 'a')
    if countr != None:
        fobj.write('cr = ' + str(countr) + '\n\n')
    fobj.write('SD\n')
    for i in range(len(w2)):
        fobj.write(str(i) + '    ' + str(w2[i]) + '\n')
    fobj.write('\nSL\n')
    for i in range(len(w3)):
        fobj.write(str(i) + '    ' + str(w3[i]) + '\n')
    fobj.write('\nVL3\n')
    for i in range(len(w7)):
        fobj.write(str(i) + '    ' + str(w7[i]) + '\n')
    fobj.write('\nVL4\n')
    for i in range(len(w8)):
        fobj.write(str(i) + '    ' + str(w8[i]) + '\n')
    fobj.close()

def thresholddist(popul):
    a = [popul[o]['genotype'][3] for o in range(N) if popul[o] != None]
    b = [popul[o]['genotype'] for o in range(N) if popul[o] != None]
    return (a.count(-9), a.count(-8), a.count(-7), a.count(-6), a.count(-5), a.count(-4), a.count(-3), a.count(-2), a.count(-1), a.count(0), a.count(1), b.count((1,1,0,1)), b.count((1,1,1,0))) 

def occupation(popul):
    genlist = [genotypetoindex(popul[o]['genotype']) for o in range(N) if popul[o] != None]
    return [genlist.count(g) for g in range(270)]

def update(genotype, env, oldstate):   #env = [0,0] [0,1] [1,1] ou [1,0] NAO EH BOOLEANA
    soma = env[0]*genotype[0] + env[1]*genotype[1] + oldstate*genotype[2]
    if soma > genotype[3]:
        return 1
    else:
        return 0

def mutated(g):
    p = list(g)
    s = [None for i in range(4)]
    for i in range(3):
        s[i] = p[i] if rndm.random() > eps else ((p[i]%3 + 2*rndm.randint(0,1))%3 - 1)  #2*rndm.randint(0,1) - 1 if p[i] == 0 else 0
    s[3] = p[3] if rndm.random() > eps else ((p[3] + (2*rndm.randint(0,1) - 1)) if (p[3] not in limits or not reflect) else (p[3] + int(math.copysign(rndm.randint(0,1), -p[3]))))
    return tuple(s)    

def mutate(divlist):
    sonlist = []
    for i in divlist:
        sonlist.append(mutated(population[i]['genotype']))
    return sonlist

def overlap(divlist):  #overlap
    nonelist = [i for i in range(N) if population[i] == None]
    sonlist = mutate(divlist)       #sonlist eh lista de tuplas enquanto que divlist eh lista de posicoes na populacao
    population.extend([{'genotype': sonlist[idx], 'state': 1, 'biomass': division_threshold/2.0} for idx in range(len(sonlist))])
    for k in range(len(population) - N):
        if None in population:
            population.remove(None)
            continue
        population.remove(population[rndm.randint(0, len(population)-1)])
            
def kill():
    for o in range(N):
        if rndm.random() < alpha:
            population[o] = None  

  

def fraction(divlist): #fraction of empty spaces
    nonelist = [i for i in range(N) if population[i] == None]
    empty = float(len(nonelist))
    frac = empty/N
    sonlist = mutate(divlist)
    idxs = []

    for s in range(len(sonlist)):
        if rndm.random() < frac:
            idxs.append(s)

    while(len(idxs) > empty):
        idxs.remove(idxs[rndm.randint(0, len(idxs)-1)])

    idx = 0
    for p in idxs:
        population[nonelist[idx]] = {'genotype': sonlist[p], 'state': 1, 'biomass': division_threshold/2.0}
        idx += 1



def killall(divlist): #killall
    nonelist = [i for i in range(N) if population[i] == None]
    sonlist = mutate(divlist)       #sonlist eh lista de tuplas enquanto que divlist eh lista de posicoes na populacao
    #print 'sonlist = ' + str(sonlist)
    newpositions = []
    livre = [i for i in range(N) if i not in nonelist]
    for p in range(len(sonlist)):
        if nonelist != []:
            newpositions.append(nonelist.pop())
            continue
        newpositions.append(rndm.sample(livre, 1)[0])
        livre.remove(newpositions[-1])
    newpositions.sort()
    #print 'newpositions = ' + str(newpositions)
    idx = 0
    for p in newpositions:
        population[p] = {'genotype': sonlist[idx], 'state': 1, 'biomass': division_threshold/2.0}
        idx += 1
    #print 'populationd: ' + str([population[k]['genotype'] for k in range(N)])


def rhoupdate(idxs):
    #print 'idxs = ' + str(idxs)
    rho[1].append(len([ids for ids in idxs if ids in LIXO]))
    rho[2].append(len([ids for ids in idxs if ids in SD]))
    rho[3].append(len([ids for ids in idxs if ids in SL]))
    rho[4].append(len([ids for ids in idxs if ids in OSCV]))
    rho[5].append(len([ids for ids in idxs if ids in VL1]))
    rho[6].append(len([ids for ids in idxs if ids in VL2]))
    rho[7].append(len([ids for ids in idxs if ids in VL3]))
    rho[8].append(len([ids for ids in idxs if ids in VL4]))
    rho[9].append(len([ids for ids in idxs if ids in SADDLE]))

def estacao(env, meth):
    divlist = []
    #print 'population = ' + str(population)
    for t in range(envchg_period):
        #print 't = ' + str(t)
        for i in range(N):
            if population[i] == None:
                continue
            population[i]['state'] = update(population[i]['genotype'], env, population[i]['state'])
            population[i]['biomass'] += (1.0 - peso if env == [1,1] else -peso)*population[i]['state']
            if population[i]['biomass'] > division_threshold:
                divlist.append(i)
                population[i]['biomass'] = division_threshold/2.0 
            if population[i]['biomass'] < 0:
                population[i] = None
        if divlist != []:
            #print 'divide! divlist = ' + str(divlist)
            meth(divlist)
            divlist = []
        if method == 'fraction':
            kill()
        idxs = [genotypetoindex(population[o]['genotype']) if population[o] != None else -1 for o in range(N)]
        rhoupdate(idxs)
        #print 'biomasses = ' + str([population[o]['biomass'] if population[o] != None else None for o in range(N)])
        #print 'population = ' + str(population)

def plotensemble(w2, w3, w7, w8):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(range(len(w2)), w2, 'k', label='SD')
    ax.plot(range(len(w3)), w3, 'r', label='SL')
    ax.plot(range(len(w7)), w7, 'g', label='VL3')
    ax.plot(range(len(w8)), w8, 'b', label='VL4')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(r'$weight=%s,\/ \epsilon=%s,\/  IC=%s, \/%s \/ simulations$'%(peso, eps, peek, numsims))
    plt.draw()
    plt.show()

def plotrho(rho):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(range(len(rho[1])), rho[9], 'y', label='saddle')
    ax.plot(range(len(rho[2])), rho[2], 'k', label='SD')
    ax.plot(range(len(rho[3])), rho[3], 'r', label='SL')
    ax.plot(range(len(rho[4])), rho[4], 'c', label='VOSC')
    ax.plot(range(len(rho[5])), rho[5], 'mo', label='VL1')
    ax.plot(range(len(rho[6])), rho[6], 'm.', label='VL2')
    ax.plot(range(len(rho[7])), rho[7], 'g', label='VL3')
    ax.plot(range(len(rho[8])), rho[8], 'b', label='VL4') 
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(r'$weight=%s,\/ \epsilon=%s,\/ IC=%s $'%(peso, eps, peek))
    plt.draw()
    plt.show()


            
def verao(meth):
    #print 'verao'
    estacao(order[0], meth)

def outono(meth):
    #print 'outono'
    estacao(order[1], meth)

def inverno(meth):
    #print 'inverno'
    estacao(order[2], meth)

def primavera(meth):
    #print 'primavera'
    estacao(order[3], meth)

def ensemblesaddle(meth):
    #idxs = [genotypetoindex(population[o]['genotype']) if population[o] != None else -1 for o in range(N)]

    global rho
    global population

    r2 = [0.0 for k in range(numyears*4*envchg_period)]
    r3 = [0.0 for k in range(numyears*4*envchg_period)]
    r7 = [0.0 for k in range(numyears*4*envchg_period)]
    r8 = [0.0 for k in range(numyears*4*envchg_period)]

    b2 = [0.0 for k in range(numyears*4*envchg_period)]
    b3 = [0.0 for k in range(numyears*4*envchg_period)]
    b7 = [0.0 for k in range(numyears*4*envchg_period)]
    b8 = [0.0 for k in range(numyears*4*envchg_period)]

    cr = 0

    for s in range(numsims):
        print 'simulation ' + str(s)
        for ano in range(numyears):
            print 'ano = ' + str(ano)
            #print 'thresholddist = ' + str(thresholddist(population))
            verao(meth)
            outono(meth)
            inverno(meth)
            primavera(meth)
        if rho[3][-1] > N/2:
            cr += 1
            for j in range(len(r2)):
                r2[j] += rho[2][j]
                r3[j] += rho[3][j]
                r7[j] += rho[7][j]
                r8[j] += rho[8][j]
                
        else:
            for j in range(len(r2)):
                b2[j] += rho[2][j]
                b3[j] += rho[3][j]
                b7[j] += rho[7][j]
                b8[j] += rho[8][j]
        
        if showplots:
            plotrho(rho)
        print population
        population = [{'genotype': peekbubble, 'state': 1, 'biomass': division_threshold/2.0} for i in range(bubble)] + [{'genotype': peek, 'state': 1, 'biomass': division_threshold/2.0} for i in range(N - bubble)]
        rho = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
        
    for j in range(len(r2)):
        if cr != 0:
            r2[j] = float(r2[j])/cr
            r3[j] = float(r3[j])/cr
            r7[j] = float(r7[j])/cr
            r8[j] = float(r8[j])/cr
        if cr != numsims:
            b2[j] = float(b2[j])/(numsims - cr)
            b3[j] = float(b3[j])/(numsims - cr)
            b7[j] = float(b7[j])/(numsims - cr)
            b8[j] = float(b8[j])/(numsims - cr)
        
    print str(cr) + ' simulacoes foram pro atrator SL e ' + str(numsims - cr) + ' para o VL4.'
   
    tb = time.time()

    print 'tempo de execucao: ' + str(tb-ta)

    plotensemble(r2, r3, r7, r8)
    plotensemble(b2, b3, b7, b8)
    if writefile:
        printtofile(r2, r3, r7, r8, 'r', countr = cr)
        printtofile(b2, b3, b7, b8, 'b')


def ensemble(meth):
    #idxs = [genotypetoindex(population[o]['genotype']) if population[o] != None else -1 for o in range(N)]

    global rho
    global population
    
    r2 = [0.0 for k in range(numyears*4*envchg_period)]
    r3 = [0.0 for k in range(numyears*4*envchg_period)]
    r7 = [0.0 for k in range(numyears*4*envchg_period)]
    r8 = [0.0 for k in range(numyears*4*envchg_period)]

    for s in range(numsims):
        print 'simulation ' + str(s)
        for ano in range(numyears):
            print 'ano = ' + str(ano)
            #print 'thresholddist = ' + str(thresholddist(population))
            verao(meth)
            outono(meth)
            inverno(meth)
            primavera(meth)

        for j in range(len(r2)):
            r2[j] += float(rho[2][j])/numsims
            r3[j] += float(rho[3][j])/numsims
            r7[j] += float(rho[7][j])/numsims
            r8[j] += float(rho[8][j])/numsims
        
        if showplots:
            plotrho(rho)
        print [population[o]['genotype'] for o in range(N) if population[o] != None]
        population = [{'genotype': peekbubble, 'state': 1, 'biomass': division_threshold/2.0} for i in range(bubble)] + [{'genotype': peek, 'state': 1, 'biomass': division_threshold/2.0} for i in range(N - bubble)]
        rho = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
   
    tb = time.time()

    print 'tempo de execucao: ' + str(tb-ta)

    plotensemble(r2, r3, r7, r8)
    if writefile:
        printtofile(r2, r3, r7, r8)

    


#ensemblesaddle(overlap)    #usar o metodo killall ou overlap para divisao

if method == 'fraction':
    ensemble(fraction)          #nao separa as trajetorias

if method == 'overlap':
    ensemble(overlap)

if method == 'killall':
    ensemble(killall)


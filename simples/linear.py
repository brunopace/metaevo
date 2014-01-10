import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import time




def hamming_distance(DNA, DNB):
    if len(DNA) != len(DNB):
        return -1
    dist = [0]*len(DNA)
    for i in range(3):
        if DNA[i] != DNB[i]:
            dist[i] += 1
    dist[3] += abs(DNA[3] - DNB[3]) 
    return dist

def theta(x):   #Heaviside function
    if x > 0:
        return 1.0
    else:
        return 0.0

def delta(x, a):
    if x == a:
        return 1.0
    else:
        return 0.0

def summut(i, HG, e):
    if HG.degree(i) == 80:
        return 1 - math.pow(1-e, 4)
    else:
        return 1 - math.pow(1-e, 4) - e/2.0

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

def update(genotype, env, oldstate):   #env = [0,0] [0,1] [1,1] ou [1,0] NAO EH BOOLEANA
    soma = env[0]*genotype[0] + env[1]*genotype[1] + oldstate*genotype[2]
    if soma > genotype[3]:
        return 1
    else:
        return 0

def calc_fitness(genotype, env, envchg_period): #calculo mais complexo
    #print 'genotype = ' + str(genotype)
    division_threshold = 10                   #algumas constantes para ajustar...
    
    order = [[1,1], [0,1], [0,0], [1,0]]
    nextyear = [s for s in order if order.index(s) < order.index(env)]

    biomass = 0
    biomass2 = 0         #a outra transicao VL3/SD se da em 1.0/6
    peso = 0.1 #peso = 1.0/4.0  transicao pra extincao para estacoes regulares
    state = 1         # senao peso = Tverao/Tano
    tdiv = -1
    fracao = 0



    for season in order:                        #primeiro ano completo, nao faz nada
        #print 'season = ' + str(season)
        for t in range(envchg_period):
            state = update(genotype, season, state) 
            
    for season in order:                        #segundo ano completo, calcula inverno
        #print 'season = ' + str(season)
        for t in range(envchg_period):
            state = update(genotype, season, state) 
            if season == [1,1]:
                biomass2 += state
            biomass2 -= peso*state     
            #print state

    for season in nextyear:                     #comeco do segundo ano ate a estacao em questao
        #print 'season = ' + str(season)
        for t in range(envchg_period):
            state = update(genotype, season, state)  
            if season == [1,1]:
                biomass2 += state
            biomass2 -= peso*state              

    for t in range(envchg_period):                   #a estacao em questao
        state = update(genotype, env, state)
        fracao += state 
        if env == [1,1]:
            biomass += state                                        #CORRIGIR ESCALA DE DIVISAO!! ELES COMECAM COM THRESH/2.0!!!!
            biomass2 += state
        biomass -= peso*state
        biomass2 -= peso*state  
        if biomass > division_threshold and tdiv == -1:
            tdiv = t + 1
            #print 'tdiv = ' + str(tdiv)
        #print 'biomass = ' + str(biomass)

    if env == [1,1]:
        #print 'verao'
        #print 'tdiv = ' + str(tdiv)
        #k = peso*envchg_period/biomass
        if tdiv == -1:
            if biomass2 > biomass:
                slope = float(biomass2 - biomass)/(4*envchg_period)
                tdiv = division_threshold/slope
            else:
                slope = float(biomass2 - biomass)/(4*envchg_period)
        #print 'tdiv = ' + str(tdiv)

        fit = math.log(2)/tdiv if tdiv != -1 else slope*math.log(2)/division_threshold
        #print 'fitverao = ' + str(fit)
        
    else:
        #print 'not verao'
        #print 'fracao = ' + str(fracao)
        k = 6*peso*fracao/division_threshold
        #print 'k = ' + str(k)
        fit = -k*math.log(2)/(3*envchg_period)      #essa conta ajusta a extincao e a hibernacao de acordo com o modelo discreto
    
    return fit

def calc_fitness2(genotype, env, envchg_period):   #calcula atraves da taxa de biomassa
    #print 'genotype = ' + str(genotype)
    division_threshold = 10                   #algumas constantes para ajustar...
    
    order = [[1,1], [0,1], [0,0], [1,0]]
    nextyear = [s for s in order if order.index(s) < order.index(env)]

    biomass = 0
    peso = 0.25  #com essa funcao, a transicao (extincao) se da em peso = 1
    state = 1     #a outra transicao SD/VL3 nao eh clara como na outra funcao
    
    for season in order + nextyear:           #primeiro ano completo, nao faz nada
        #print 'season = ' + str(season)
        for t in range(envchg_period):
            state = update(genotype, season, state) 

    for t in range(envchg_period):                   #a estacao em questao
        state = update(genotype, env, state)
        if env == [1,1]:
            biomass += state
        biomass -= peso*state

    
    return biomass/envchg_period



def normalise(vector):
    return vector/np.dot(vector, np.array([1 for i in range(len(vector))]))


def drawhist(menMeans, season):

    N = len(menMeans)

    ind = np.arange(N)
    width = 1.0

    plt.clf()
    plt.ion()
    plt.ylabel('Occupation')
    plt.xlabel('genotype')
    plt.title(season)
    plt.xlim(0.0,N)
    plt.ylim(0.0,1.0)
    plt.bar(ind, menMeans, width)
    plt.draw()
    plt.pause(0.001)
    plt.ioff()



def forward_Euler(Matrix, vector, step, nsteps, rho, season):
    #drawhist(vector,  season)
    for t in range(nsteps):
        vector += step*np.dot(Matrix, vector)
        vector = normalise(vector)        #pra verificar extincao, comentar.
        rhoupdate(vector, rho)
        #drawhist(vector,  season)
        
    return vector

def rhoupdate(v, rho):
    rho[1].append(np.dot(v, vlixo))
    rho[2].append(np.dot(v, vsd))
    rho[3].append(np.dot(v, vsl))
    rho[4].append(np.dot(v, voscv))
    rho[5].append(np.dot(v, vvl1))
    rho[6].append(np.dot(v, vvl2))
    rho[7].append(np.dot(v, vvl3))
    rho[8].append(np.dot(v, vvl4))
    rho[9].append(np.dot(v, vor))

envchg_period = 12
step = 1
weights = [-1, 0, 1]
eps = 0.0001      #para eps < 0.11 a maioria da populacao se localiza no pico (256)
maxfit = (0, 0)
HG = nx.Graph()


LIXO = [3, 4, 13, 14, 24, 34, 44, 65, 75, 85, 94, 104, 185, 195]
SD = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 45, 46, 47, 48, 49, 55, 56, 57, 58, 59, 66, 67, 68, 69, 76, 77, 78, 79, 86, 87, 88, 89, 95, 96, 97, 98, 99, 105, 106, 107, 108, 109, 115, 116, 117, 118, 119, 125, 126, 127, 128, 129, 135, 136, 137, 138, 139, 146, 147, 148, 149, 156, 157, 158, 159, 166, 167, 168, 169, 176, 177, 178, 179, 186, 187, 188, 189, 196, 197, 198, 199, 206, 207, 208, 209, 216, 217, 218, 219, 226, 227, 228, 229, 236, 237, 238, 239, 247, 248, 249, 257, 258, 259, 267, 268, 269]
SL = [0, 1, 10, 11, 12, 20, 21, 22, 23, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54, 60, 61, 62, 70, 71, 72, 73, 80, 81, 82, 83, 84, 90, 91, 92, 100, 101, 102, 103, 110, 111, 112, 113, 114, 120, 121, 122, 123, 130, 131, 132, 133, 134, 140, 141, 142, 143, 144, 145, 150, 151, 152, 153, 160, 161, 162, 163, 164, 170, 171, 172, 173, 174, 175, 180, 181, 182, 190, 191, 192, 193, 200, 201, 202, 203, 204, 210, 211, 212, 213, 220, 221, 222, 223, 224, 230, 231, 232, 233, 234, 235, 240, 241, 242, 243, 250, 251, 252, 253, 254, 260, 261, 262, 263, 264, 265]
OSCV = [2, 33, 64, 93, 124, 155, 184, 215, 246]
VL = [63, 74, 154, 165, 183, 194, 205, 214, 225, 244, 245, 255, 256, 266]

VL1 = [63, 183, 244]
VL2 = [74, 154, 194, 214, 255]
VL3 = [165, 205, 225, 245, 266]
VL4 = [256]

CI = [145]
OR = [165, 225]
SADDLE = [255]

vlixo = np.array([1.0 if i in LIXO else 0.0 for i in range(270)])
vsd = np.array([1.0 if i in SD else 0.0 for i in range(270)])
vsl = np.array([1.0 if i in SL else 0.0 for i in range(270)])
voscv = np.array([1.0 if i in OSCV else 0.0 for i in range(270)])
vvl = np.array([1.0 if i in VL else 0.0 for i in range(270)])

vci = np.array([1.0 if i in CI else 0.0 for i in range(270)])
vor = np.array([1.0 if i in OR else 0.0 for i in range(270)])
vsaddle = np.array([1.0 if i in SADDLE else 0.0 for i in range(270)])

vvl1 = np.array([1.0 if i in VL1 else 0.0 for i in range(270)])
vvl2 = np.array([1.0 if i in VL2 else 0.0 for i in range(270)])
vvl3 = np.array([1.0 if i in VL3 else 0.0 for i in range(270)])
vvl4 = np.array([1.0 if i in VL4 else 0.0 for i in range(270)])

rho = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

idx = 0

for i in weights:        #i eh entrada da comida A, j da comida B e k eh o self-loop
    for j in weights:
        for k in weights:
            for thresh in [th-5 for th in range(10)]:
                HG.add_node(idx,  {'genotype': (i, j, k, thresh), tuple([1,1]):calc_fitness((i,j,k,thresh), [1,1], envchg_period), tuple([1,0]):calc_fitness((i,j,k,thresh), [1,0], envchg_period), tuple([0,0]):calc_fitness((i,j,k,thresh), [0,0], envchg_period), tuple([0,1]):calc_fitness((i,j,k,thresh), [0,1], envchg_period)})
                idx += 1
                #print 'genotype: ' + str((i,j,k,thresh))
                #print 'fitness [1, 1]: ' + str(calc_fitness((i,j,k,thresh), [1,1])) 
                #print 'fitness [1, 0]: ' + str(calc_fitness((i,j,k,thresh), [1,0])) 
                #print 'fitness [0, 0]: ' + str(calc_fitness((i,j,k,thresh), [0,0])) 
                #print 'fitness [0, 1]: ' + str(calc_fitness((i,j,k,thresh), [0,1]))
                m = calc_fitness((i,j,k,thresh), [1,1], envchg_period) + calc_fitness((i,j,k,thresh), [1,0], envchg_period) + calc_fitness((i,j,k,thresh), [0,1], envchg_period) + calc_fitness((i,j,k,thresh), [0,0], envchg_period)
                #if m > 0:
                    #print 'fitness total organismo ' + str((i, j, k, thresh)) + ': ' + str(m)
                if m > maxfit[0]:
                    maxfit = (m, (i, j, k, thresh))



print 'maxfit = ' + str(maxfit)


for Da in HG.nodes():
    for Db in HG.nodes():
        if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [0,1,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,0,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,0,0,1]:
            HG.add_edge(Da, Db, {'d': 1})
        if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [1,0,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [0,0,1,1]:
            HG.add_edge(Da, Db, {'d': 2})
        if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [1,1,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,1,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,1,1]:
            HG.add_edge(Da, Db, {'d': 3})
        if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,1,1]:
            HG.add_edge(Da, Db, {'d': 4})

Verao = np.array([[HG.node[j][(1,1)]*(1 - theta(HG.node[j][(1,1)])*summut(j, HG, eps)) if i==j else (HG.node[j][(1,1)]*theta(HG.node[j][(1,1)])*math.pow(eps/2.0,HG.edge[i][j]['d'])*math.pow(1 - eps,4 - HG.edge[i][j]['d']) if j in HG.neighbors(i) else 0) for j in range(270)]for i in range(270)])
Outono = np.array([[HG.node[j][(0,1)] if i == j else 0.0 for j in range(270)] for i in range(270)])
Inverno = np.array([[HG.node[j][(0,0)] if i == j else 0.0 for j in range(270)] for i in range(270)])
Primavera = np.array([[HG.node[j][(1,0)] if i == j else 0.0 for j in range(270)] for i in range(270)])



nx.draw(HG)
plt.show()



v = np.array([delta(i, 145) for i in range(270)])   #145 sao as CIs usuais
                                                    #256 faz AND

rhoupdate(v, rho)


print 'v[145] = ' + str(v[145])

#drawhist(v, 'inicio')
for ano in range(250):
    print 'ano = ' + str(ano)
    v = forward_Euler(Verao, v, step, int(round(envchg_period/step)), rho, 'verao')
    v = forward_Euler(Outono, v, step, int(round(envchg_period/step)), rho, 'outono')
    v = forward_Euler(Inverno, v, step, int(round(envchg_period/step)), rho, 'inverno')
    v = forward_Euler(Primavera, v, step, int(round(envchg_period/step)), rho, 'primavera')


fig = plt.figure()
ax = plt.subplot(111)
ax.plot([i*step for i in range(len(rho[1]))], rho[1], 'y', label='lixo')
ax.plot([i*step for i in range(len(rho[2]))], rho[2], 'k', label='SD')
ax.plot([i*step for i in range(len(rho[3]))], rho[3], 'r', label='SL')
ax.plot([i*step for i in range(len(rho[4]))], rho[4], 'c', label='VOSC')
ax.plot([i*step for i in range(len(rho[5]))], rho[5], 'mo', label='VL1')
ax.plot([i*step for i in range(len(rho[6]))], rho[6], 'm.', label='VL2')
ax.plot([i*step for i in range(len(rho[7]))], rho[7], 'g', label='VL3')
ax.plot([i*step for i in range(len(rho[8]))], rho[8], 'b', label='VL4') #, [i*step for i in range(len(rho[9]))], rho[9])plt.draw()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[1]))], rho[1])
plt.title('LIXO')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[2]))], rho[2])
plt.title('SD')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[3]))], rho[3])
plt.title('SL')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[4]))], rho[4])
plt.title('OSCV')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[5]))], rho[5])
plt.title('VL1')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[6]))], rho[6])
plt.title('VL2')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[7]))], rho[7])
plt.title('VL3')
plt.draw()
plt.show()

plt.plot([i*step for i in range(len(rho[8]))], rho[8])
plt.title('VL4')
plt.draw()
plt.show()

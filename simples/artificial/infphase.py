import matplotlib.pyplot as plt


eps = 0.1
method = 'fraction'

numyears = 100000


T1 = 3
T2 = 2

population = [1.0 if k == 0 else 0.0 for k in range(T1+T2)]

alpha = 0.001

rho = {}

for i in range(T1+T2):
    rho.update({i:[]})

def kill():
    for i in range(T1+T2):
        population[i] = population[i]*(1-alpha)
        


def nextstep(method, na, nb):
    nextpop = [0.0 for l in range(T1+T2)]
    if method == 'killall':
        nextpop[na] += population[na]*(1-eps) + population[T1+nb]*eps 
        nextpop[T1+nb] += population[T1+nb]*(1-eps) + population[na]*eps
        kill = nextpop[na] + nextpop[T1+nb]
        for i in range(T1+T2):
            population[i] = population[i]*(1-kill) + nextpop[i]

    elif method == 'fraction':
        frac = 1.0
        for o in range(T1+T2):
            nextpop[o] = population[o]
            frac -= population[o]
            
        nextpop[na] += population[na]*(1-eps)*frac
        nextpop[na] += population[T1+nb]*eps*frac
        nextpop[T1+nb] += population[T1+nb]*(1-eps)*frac 
        nextpop[T1+nb] += population[na]*eps*frac
        for i in range(T1+T2):
            population[i] = nextpop[i]
        

            
    else:
        nextpop[na] += population[na]*(1-eps) + population[T1+nb]*eps 
        nextpop[T1+nb] += population[T1+nb]*(1-eps) + population[na]*eps
        kill = nextpop[na] + nextpop[T1+nb]
        for i in range(T1+T2):
            population[i] = (population[i] + nextpop[i])/(1+kill)


def rhoupdate(population):
    for i in range(T1+T2):
        rho[i].append(population[i])

def showplots():
    for i in range(T1+T2):
        plt.plot(range(len(rho[i])), rho[i])
        plt.title('serie ' + str(i))
        plt.show()
def plotall():
    for i in range(T1+T2):
        plt.plot(range(len(rho[i])), rho[i])
        
    plt.show()    


for t in range(numyears):
    rhoupdate(population)
    if (t+1)%1000 == 0:
            print 'ano = ' + str(t+1)
    nextstep(method, (t+1)%T1, (t+1)%T2)
    if method == 'fraction':
        kill()


plotall()

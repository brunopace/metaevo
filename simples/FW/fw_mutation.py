import networkx as nx
import matplotlib.pyplot as plt
import random as rndm

class population():
    def __init__(self, N):
        self.size = N
        self.fitness = {'acerola':3, 'manga':2}
        self.tipos = self.fitness.keys()
        self.list = [None]*N
        self.rel_fitness = [0]*len(self.tipos)
        self.type_count = [0]*len(self.tipos)


    def reset_type_count(self):
        self.type_count = [0]*len(self.tipos)
        for i in range(self.size):
            self.type_count[self.tipos.index(self.list[i][0])] += 1

    def reset_rel_fitness(self):
        soma = 0
        for t in self.tipos:
            soma += self.type_count[self.tipos.index(t)]*self.fitness[t]
        for i in range(len(self.tipos)):
            self.rel_fitness[i] = float(self.fitness[self.tipos[i]])/soma

    def seed_init(self, k):
        for i in range(self.size - k):
            self.list[i] = (self.tipos[0], None)
            self.type_count[0] += 1
        for i in range(k):
            self.list[i + self.size - k] = (self.tipos[1], None)
            self.type_count[1] += 1
        self.reset_rel_fitness()


    def equal_init(self):
        for i in range(self.size):
            self.list[i] = (self.tipos[i%len(self.tipos)], None)
            self.type_count[i%len(self.tipos)] += 1
        self.reset_rel_fitness()
        
    def rand_init(self):
        for i in range(self.size):
            r = rndm.randint(0, len(self.tipos) - 1)
            self.list[i] = (self.tipos[r], None)
            self.type_count[r] += 1
        self.reset_rel_fitness()

    def choose_fitness(self): #draws random organism proportionally to rel fitness
        r = rndm.random()
        #print 'r = ' + str(r)
        p = 0
        for i in range(self.size):
            p += self.rel_fitness[self.tipos.index(self.list[i][0])]
            if p > r:
                return i
        #print 'returning last'
        return self.size - 1
    
    def mutate(self, pai, eps):

        r = 1 if rndm.random() < eps[pai] else 0

        f = (pai + r)%2

        return self.tipos[f]
        
        
    def next_generation(self, eps):
        interm = [None]*self.size
        for i in range(self.size):
            o = self.choose_fitness()
            pai = self.tipos.index(self.list[o][0])
            filho = self.mutate(pai, eps)
            interm[i] = (filho, o)
        self.list = interm
        self.reset_type_count()
        self.reset_rel_fitness()



A = population(1000)
A.seed_init(1000)

eps = [0.00001, 0.00001]

counts0 = []
counts1 = []
counts2 = []
counts3 = []
counts4 = []
counts5 = []

for t in range(100):
    print 'generation ' + str(t)
#    print 'count: '
#    print A.type_count
#    print 'rel_fitness: '
#    print A.rel_fitness
    counts0.append(A.type_count[0])
    counts1.append(A.type_count[1])
#    counts2.append(A.type_count[2])
#    counts3.append(A.type_count[3])
#    counts4.append(A.type_count[4])
#    counts5.append(A.type_count[5])
    A.next_generation(eps)

print 'tipos = ' + str(A.tipos)

plt.plot(range(len(counts0)), counts0,range(len(counts1)), counts1) #,range(len(counts2)), counts2, range(len(counts3)), counts3) #,range(len(counts4)), counts4,range(len(counts5)), counts5)
plt.show()


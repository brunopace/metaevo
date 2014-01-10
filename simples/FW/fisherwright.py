import networkx as nx
import matplotlib.pyplot as plt
import random as rndm

class population():
    def __init__(self, N):
        self.size = N
        self.fitness = {'a':1, 'b':1.15}
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

    def choose_fitness(self):
        r = rndm.random()
        #print 'r = ' + str(r)
        p = 0
        for i in range(self.size):
            p += self.rel_fitness[self.tipos.index(self.list[i][0])]
            #print 'p = ' + str(p)
            if p > r:
                #print 'returning ' + str(i)
                return i
        #print 'returning last'
        return self.size - 1
        
    def next_generation(self):
        interm = [None]*self.size
        for i in range(self.size):
            o = self.choose_fitness()
            interm[i] = (self.list[o][0], o)
        self.list = interm
        self.reset_type_count()
        self.reset_rel_fitness()



A = population(60)
A.seed_init(6)
counts0 = []
counts1 = []
counts2 = []
counts3 = []
counts4 = []
counts5 = []

for t in range(30):
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
    A.next_generation()

#print 'tipos = ' + str(A.tipos)

plt.plot(range(len(counts0)), counts0,range(len(counts1)), counts1,range(len(counts2)), counts2) #, range(len(counts3)), counts3,range(len(counts4)), counts4,range(len(counts5)), counts5)
plt.show()



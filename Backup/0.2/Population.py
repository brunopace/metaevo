#!/usr/bin/python

import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from Environment import Environment
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from Organism import Organism
from Constants import Constants
from copy import deepcopy

#O ambiente eh gerado antes de mais nada!!!
#Aqui tem que ser decidido sobre as condicoes.


plt.ion()

class GrowNoFoodException(Exception):
    pass

class UngrowWithFoodException(Exception):
    pass

class Population():
    def __init__(self):
        self.time = 0
        self.generation = 0
        self.records = ['a']*Constants.record_size
        self.worst_record = 'a'
        self.population = [None]*Constants.population_size
        for o in range(Constants.population_size):
            self.population[o] = Organism(MetNet, inicial = True)
            self.population[o].species = o
        

    def drawhist(self):


        N = Constants.population_size
        ind = numpy.arange(N)    
        width = 1.0

        plt.ylabel('Biomass')
        plt.title('Population Status')
        

        menMeans = [0 if self.population[o] is None else self.population[o].biomass  for o in range(N)]
        menColours = ['#000000' if self.population[o] is None else '#' + '0'*(6 - len(hex(int(round(0xffffff*float(self.population[o].species)/(N-1))))[2:])) + hex(int(round(0xffffff*float(self.population[o].species)/(N-1))))[2:] for o in range(N)]
        plt.clf()
        if menColours == [menColours[0]]*len(menColours):
            self.reset_species()
            self.generation += 1
        plt.title('This is generation ' + str(self.generation), fontsize=20)
        p1 = plt.bar(ind, menMeans,   width, color = menColours)
        plt.xlim(0.0,N)
        plt.ylim(-1.5*Constants.division_threshold,1.5*Constants.division_threshold)
        plt.draw()
        plt.draw()
    
    def reset_species(self):
        for o in range(Constants.population_size):
            if self.population[o] != None:
                self.population[o].species = o

    def step(self, index):   #contabiliza intermediarios baseado em Constants.intermenergy
        #da um passo na rede booleana e atualiza os estados das reacoes quimicas
        #e incrementa/decrementa a biomassa de cada individuo da populacao
        
        if self.time%Constants.tb == 0:
            self.genometofile()
            
        self.drawhist()          #DESLIGAR AQUI PARA NAO MOSTRAR O GRAFICO DAS BIOMASSAS
            
        for o in range(Constants.population_size):
            if self.population[o] == None:
                continue
            genestr = self.population[o].control.change_state() #inclui comidas, genes e intermediarios
            self.population[o].chemistry.update_reactions(self.population[o].control.switch_dict)
            enzyme_fraction = 0
            for j in range(len([g for g in self.population[o].control.nodes() if (g < Constants.metabolites + Constants.reactions if not Constants.intermenergy else True) and g >= self.population[o].control.number_food_actual])):      #inclui interm ou nao dependendo de intermenergy
                enzyme_fraction+=genestr[j + self.population[o].control.number_food_actual]
            enzyme_fraction = Constants.peso*float(enzyme_fraction)/(Constants.genes + len(self.population[o].control.intermediate_list) if Constants.intermenergy else Constants.genes)
            #print 'enzyme_fraction = ' + str(enzyme_fraction)
            self.population[o].biomass += self.population[o].chemistry.path_to_target() - enzyme_fraction
            if(self.population[o].chemistry.path_to_target() - enzyme_fraction > 0 and index != 0):
                raise GrowNoFoodException('There is no food, but there are still organisms growing!')
#            if(self.population[o].chemistry.path_to_target() - enzyme_fraction < 0 and index == 0):
#                print 'organismo ' + str(o) + ' ta tirando um barato...'
#                print 'enzymefraction = ' + str(enzyme_fraction)
#                print 'genestr = ' + str(genestr)
#                print 'self.population[o].chemistry.path_to_target(debug=True) = ' + str(self.population[o].chemistry.path_to_target(debug=True))
#                print 'self.population[o].chemistry.node[0][Flowing] = ' + str(self.population[o].chemistry.node[0]['Flowing'])
#                print 'self.population[o].chemistry.node[1][Flowing] = ' + str(self.population[o].chemistry.node[1]['Flowing'])
#                print 'self.population[o].chemistry.nodes() = ' + str(self.population[o].chemistry.nodes())
#                print 'self.population[o].chemistry.edges() = ' + str(self.population[o].chemistry.edges())
#                print 'self.population[o].control.intermediate_list = ' + str(self.population[o].control.intermediate_list)
#                raise UngrowWithFoodException('There is food and someone is decreasing...')


                
            self.population[o].age += 1
        self.time += 1
        
#    def stepdeprecated(self, index):  #original contabilizando os intermediarios 
#        #da um passo na rede booleana e atualiza os estados das reacoes quimicas
#        #e incrementa/decrementa a biomassa de cada individuo da populacao
        
#        if self.time%Constants.tb == 0:
#            self.genometofile()
            
#        self.drawhist()          #DESLIGAR AQUI PARA NAO MOSTRAR O GRAFICO DAS BIOMASSAS
            
#        for o in range(Constants.population_size):
#            genestr = self.population[o].control.change_state()  #inclui comidas, genes e intermediarios
#            self.population[o].chemistry.update_reactions(self.population[o].control.switch_dict)
#            enzyme_fraction = 0
#            for j in range(len([g for g in self.population[o].control.nodes() if g >= self.population[o].control.number_food_actual])):      
#                enzyme_fraction+=genestr[j + self.population[o].control.number_food_actual]
#            enzyme_fraction = Constants.peso*float(enzyme_fraction)/(Constants.genes + len(self.population[o].control.intermediate_list))
#            #print 'enzyme_fraction = ' + str(enzyme_fraction)
#            self.population[o].biomass += self.population[o].chemistry.path_to_target() - enzyme_fraction
#            if(self.population[o].chemistry.path_to_target() - enzyme_fraction > 0 and index != 0):
#                raise GrowNoFoodException('There is no food, but there are still organisms growing!')
#            if(self.population[o].chemistry.path_to_target() - enzyme_fraction < 0 and index == 0):
#                print 'organismo ' + str(o) + ' ta tirando um barato...'
#                raise UngrowWithFoodException('There is food and someone is decreasing...')               
#            self.population[o].age += 1
#        self.time += 1
            

    def divide(self, lista_o, rate, MetNet, ES):
        for o in lista_o:
            self.population.append(self.population[o].mutate(rate, MetNet, ES))
            self.population[-1].mother_record = self.population[o].age
            self.population[-1].species = self.population[o].species
            fobj = open(base_path+'divide.txt', 'a')
            fobj.write('dividiu: ' + str(o) + ' da especie: ' + str(self.population[o].species) + ' com a idade ' + str(self.population[o].age) + ' no tempo ' + str(self.time) + '\n')
            fobj.close()
            

 
        
            if self.population[o].age < self.population[o].record:
                self.population[o].record = self.population[o].age
            
            
            if self.population[o].age < self.worst_record:
                self.records.append(self.population[o].age)
                self.records.sort()
                self.records.pop()
                self.worst_record = self.records[-1]
                #fobj = open(base_path+'records.txt', 'a')
                #fobj.write('records:' + str(self.records))
                #fobj.write('\n+++++++++++++++++++++++++++\n')
                #fobj.write(str(self.population[o].control.edges()))
                #fobj.write('\n+++++++++++++++++++++++++++\n')
                #fobj.close()


            self.population[o].age = 0
            self.population[o].biomass = Constants.division_threshold/2.0        #aqui eh a biomassa da celula filha que nao recebe a mutacao!

        if Constants.die and None in self.population:
            nonelist = [ni for ni in range(len(self.population)) if self.population[ni] == None]
            if len(lista_o) <= len(nonelist):
                popping_list = sorted(rndm.sample(nonelist, len(lista_o)))
            else:
                popping_list = sorted(nonelist + rndm.sample([nn for nn in range(len(self.population)) if self.population[nn] != None], len(lista_o) - len(nonelist)))
        else:
            popping_list = sorted(rndm.sample(range(len(self.population)), len(lista_o)))
        fobj = open(base_path+'divide.txt', 'a')
        fobj.write('popping: ' + str(popping_list))
        

        decr = 0
        for d in popping_list:
            self.population.pop(d + decr)
            decr -= 1
        fobj.write('\ndivision ages:\n' + str([None if self.population[ind] == None else self.population[ind].record for ind in range(Constants.population_size)]))
        fobj.write('\nmothers ages:\n' + str([None if self.population[ind] == None else self.population[ind].mother_record for ind in range(Constants.population_size)]) + '\n\n')
        fobj.close()

        fobj = open(base_path+'species.txt', 'a')
        fobj.write(str([None if self.population[ind] == None else self.population[ind].species for ind in range(Constants.population_size)]) + '\n')
        fobj.close()

    def genometofile(self):
        fobj = open(base_path+'genome.txt', 'a')
        fobj.write('timestep: ' + str(self.time) + '\n')
        r = 'a'
        ix = 0
        for i in range(Constants.population_size):
            if self.population[i] == None:
                continue
            if self.population[i].record < r:
                r = self.population[i].record
                ix = i
        if self.population == [None]*Constants.population_size:
                print 'Extincao total!!!'                             #lidar melhor com o caso de extincao...
                return 

        while (self.population[ix] == None):         #para nao correr o risco de pegar um sitio sem organismos...
            ix += 1
            
        fobj.write('division age: ' + str(r) + '\n')
        fobj.write('DNA: ' + '\n' + str(self.population[ix].control.export_code()) + '\n' )
        fobj.write('control: ' + '\n' + str(self.population[ix].control.edges()) + '\n' )
        fobj.write('on/off: ' + '\n' + str([self.population[ix].control.node[n]['on'] for n in self.population[ix].control.nodes()]) + '\n')
        fobj.write('# - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # - - - # \n\n')
        fobj.close()
            
def mutate_DNA(code, rate):
    for i in range(len(code)):
        if rndm.random() <= rate:
            code[i] = (code[i]%3 + 2*rndm.randint(0,1))%3 - 1
    return code

def crossover_DNA(codem, codep, number_points):
    coded = []
    points = rndm.sample(range(len(codem) - 1), number_points)
    dicdna = {0: codem, 1: codep}
    orig = rndm.randint(0,1)
    for i in xrange(len(codem)):
        coded.append(dicdna[orig][i])
        if i in points:
            orig = (orig + 1)%2
    return coded

def calculamedia(listaas):
    n = 0
    media = 0.0
    for el in listaas:
        if el == 'a':
            continue
        media += el
        n += 1
    if n == 0:
        return 0
    return media/n

def headertofile(string):

    fobj = open(base_path+'header.txt', 'a')
    fobj.write(string)
    fobj.write('\n\n' + 'die = ' + str(Constants.die))
    fobj.write('\n\n' + 'intermenergy = ' + str(Constants.intermenergy))
    fobj.write('\n\n' + 'varthresh = ' + str(Constants.varthresh))
    fobj.write('\n\n' + 'food = ' + str(Constants.food))
    fobj.write('\n' + 'targets = ' + str(Constants.targets))
    fobj.write('\n' + 'metabolites = ' + str(Constants.metabolites))
    fobj.write('\n' + 'reactions = ' + str(Constants.reactions))
    fobj.write('\n' + 'genes = ' + str(Constants.genes))
    fobj.write('\n' + 'intermediate = ' + str(Constants.intermediate))
    fobj.write('\n' + 'p = ' + str(Constants.p))
    fobj.write('\n' + 'population_size = ' + str(Constants.population_size))
    fobj.write('\n' + 'division_threshold = ' + str(Constants.division_threshold))
    fobj.write('\n' + 'record_size = ' + str(Constants.record_size))
    fobj.write('\n' + 'rate = ' + str(Constants.rate))
    fobj.write('\n' + 'number_environments = ' + str(Constants.number_environments))
    fobj.write('\n' + 'envchg_period = ' + str(Constants.envchg_period))
    fobj.write('\n' + 'env_change_rate = ' + str(Constants.env_change_rate))
    fobj.write('\n' + 'peso = ' + str(Constants.peso))
    fobj.write('\n' + 'ta = ' + str(Constants.ta))
    fobj.write('\n' + 'tb = ' + str(Constants.tb))
    fobj.write('\n' + 'end_step = ' + str(Constants.end_step))
    fobj.close()

def constant_size(descriptive_string, environ_list, environ_change_method, period):
     
    headertofile(descriptive_string)
    global MetNet
    global EnvironmentSituation

    print 'environment!'
    #fobj = open(base_path+'environment.txt', 'a')
    #fobj.write('environ_list: ' + str(environ_list))
    #fobj.close()

    MetNet = MetabolicNetwork(descriptive_string)



    EnvironmentSituation = Constants.env_dict[descriptive_string][0]
    print 'EnvironmentSituation = ' + str(EnvironmentSituation)
    #fobj = open(base_path+'MetNet.txt', 'a')
    #fobj.write('Metabolic Network' + str(MetNet.edges()) + '\n\n' + str(MetNet.edge))
    #fobj.close()
 

    a = Population()
    division = []
    chg = False
    env_ind = 0

    media_idades_reprod = []


    for my_step in xrange(Constants.end_step):
        
        a.step(env_ind)        
        chg, env_ind = environ_change_method(env_ind, period, a, descriptive_string)
        #print 'food_list praviriguah: ' + str(environ_list[env_ind])



        for o in range(Constants.population_size):
            if a.population[o] == None:
                continue
            if a.population[o].biomass < 0 and Constants.die:
                a.population[o] = None                          #aqui os individuos morrem se Constants.die for True
                continue
            if chg:

                #print 'organismo ' + str(o)
                a.population[o].change_environment_org(environ_list[env_ind])
                #fobj = open(base_path+'environment.txt', 'a')
                #fobj.write('\norganismo ' + str(o) + ' mudou ambiente 0-chemistry: ' + str(a.population[o].chemistry.node[0]['Flowing']))
                #fobj.write('\norganismo ' + str(o) + ' mudou ambiente 1-chemistry: ' + str(a.population[o].chemistry.node[1]['Flowing']))
                #fobj.write('\norganismo ' + str(o) + ' mudou ambiente 0-control: ' + str(a.population[o].control.node[0]['on']))
                #fobj.write('\norganismo ' + str(o) + ' mudou ambiente 1-control: ' + str(a.population[o].control.node[1]['on']))
                #fobj.close()
                
            if a.population[o].biomass > Constants.division_threshold:
                division.append(o)

        if len(division) > 0:
            a.divide(division, Constants.rate, MetNet, EnvironmentSituation)
            division = []

        if a.time%Constants.ta == 0:
            media_idades_reprod.append(calculamedia([a.population[ind].mother_record for ind in range(Constants.population_size) if a.population[ind] != None]))
            #print 'media_idades'
            fobj = open(base_path+'media_idades.txt', 'w')
            fobj.write('media_idades_reprod:')
            fobj.write(str(media_idades_reprod) + '\n\n')
            fobj.close()
            

        chg = False

    fobj = open(base_path+'plot.py', 'w')
    fobj.write('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.plot(')
    fobj.write(str(media_idades_reprod))
    fobj.write(')\n\nplt.show()\nplt.draw()\nplt.draw()')
    fobj.close()
    

def constant_method(env_ind, period, population, descriptive_string):
    return (False, 0)

def periodic_method(env_ind, period, population, descriptive_string):
    global EnvironmentSituation
    if population.time % Constants.envchg_period == 0:
        novo = (env_ind + 1)%period
        EnvironmentSituation = Constants.env_dict[descriptive_string][novo]
        #fobj = open(base_path+'environment.txt', 'a')
        #fobj.write('\nmudou!!!' + str(Constants.env_dict['minimum'][novo]) + 'novo = ' + str(novo))
        #fobj.close()
        EnvironmentSituation = Constants.env_dict[descriptive_string][novo]
        print 'ambiente novo: ' + str(Constants.env_dict['minimum'][novo])    #MUDAR AQUI PARA GENERALIZAR PARA A REDE METABOLICA
        return (True, novo)
    return (False, env_ind)


def periodic_random_method(env_ind, period, population, descriptive_string):
    global EnvironmentSituation
    if population.time % Constants.envchg_period == 0:
        novo = rndm.randint(0,period - 1)
        fobj = open(base_path+'environment.txt', 'a')
        fobj.write('\nmudou!!!' + str(Constants.env_dict['minimum'][novo]) + 'novo = ' + str(novo))
        fobj.close()  
        EnvironmentSituation = Constants.env_dict[descriptive_string][novo]
        print 'ambiente novo: ' + str(Constants.env_dict['minimum'][novo])    #MUDAR AQUI PARA GENERALIZAR PARA A REDE METABOLICA
        return (True, novo)
    return (False, env_ind)


def random_method(env_ind, period, population, descriptive_string):
    global EnvironmentSituation
    if rndm.random() < Constants.env_change_rate:
        novo = rndm.randint(0, period - 1) 
        EnvironmentSituation = Constants.env_dict[descriptive_string][novo]
        return (True, novo)    
    return (False, env_ind)





if __name__ == '__main__':    

 

    global EnvironmentSituation

    MetNet = None
    EnvironmentSituation = None


    print ('executing from '+sys.argv[1])
    execution = open(sys.argv[1])

    simulation_n = 0
    while True:
        execution.seek(0)
        for line in execution:
            if line[0] == '#':
                continue
            args = line.split()

            print ('executing simulation '+str(simulation_n), args[0], 'root path is', 
            args[1], 'mutation rate is', Constants.rate)
      
            print 'rate: ' + str(Constants.rate)
        
            base_path = args[1]+str(simulation_n)+'/'
      
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            exec(args[0])
        simulation_n += 1
    
    print '...Done. Ciao!'
  

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from Environment import Environment
from MetabolicNetwork import MetabolicNetwork
from Control import Control
from Constants import Constants
from copy import deepcopy

class GeneNumberException(Exception):
    pass


class Organism(nx.DiGraph):
    def __init__(self, MetNet, inicial = False, control = None, EnvironmentSituation = None):
        self.age = 0
        self.record = 'a'
        self.mother_record = 'a'
        self.species = 'a'
        self.metabolites = Constants.metabolites
        self.number_targets = Constants.targets
        food_list = range(Constants.food)

        
        if inicial: #verifica se a populacao eh inicial
            react_list = [x + self.metabolites for x in range(Constants.reactions)]
             

            if Constants.genes > len(react_list):
                raise GeneNumberException('There are more genes than reactions to be controlled!')

            genes_list = food_list + sorted(rndm.sample(react_list, Constants.genes))

            #talvez fosse util ter um dicionario que redireciona pra funcoes
            #dependendo do tipo de inicializacao - inicial ou mutacao - e
            #encapsular uma serie de coisas que por enquanto estao no __init__.

            self.chemistry = self.clean_met_net(MetNet, genes_list, food_list, EnvironmentSituation)
##            print 'o dicionario inicial de chemis:'
##            print self.chemistry.node
            self.control = Control(genes_list, inicial)
##            print 'dicionario inicial:'
##            print self.control.switch_dict
            self.chemistry.update_reactions(self.control.switch_dict)
            self.biomass = Constants.division_threshold/2.0        #aqui eh a biomassa do organismo inicial.
##            print 'biomass_init'
##            print self.biomass
        else: #caso a populacao seja gerada de uma mutacao...
            self.control = control
            self.chemistry = self.clean_met_net(MetNet, control.genes_list, food_list, EnvironmentSituation)
            self.chemistry.update_reactions(self.control.switch_dict)
            self.biomass = Constants.division_threshold/2.0      #aqui deve ser a biomassa do organismo filho mutado.
            

    def clean_met_net(self, MetNet, genes_list, food_list, EnvironmentSituation):
        #Verificar com mais calma se a delecao de targets nao afeta nada...
        chemis = deepcopy(MetNet)
        #sera que esse objeto vai receber as funcoes da classe MetabolicNetwork?

        for r in [x for x in MetNet.nodes() if MetNet.node[x]['Type'] == 'R']:
            if r not in [reac for reac in genes_list if reac not in food_list]:
                chemis.remove_node(r)
        #Alguns targets podem ser deletados nesse passo:
        chemis.remove_nodes_from([isol for isol in nx.isolates(chemis) if isol not in food_list])
        
        if EnvironmentSituation is not None:
            for f in range(Constants.food):
                chemis.node[f]['Flowing'] = EnvironmentSituation[f]

        #chemis.remove_nodes_from([n for n in nx.isolates(chemis) if n not in food_list])????
        #Talvez tenha que verificar se food ou target molecules foram removidos?
        return chemis
    
    def change_environment_org(self, food_list):
        self.control.change_environment(food_list)
        #print 'compare a lista e o dicionario:'
        #print food_list
        #print self.control.food_dict
        self.chemistry.update_food(self.control.food_dict)

    def mutate(self, rate, MetNet, EnvironmentSituation):

        DNAp = self.control.export_code()
        DNAm = mutate_DNA(DNAp, rate)
        control_son = Control(DNA = DNAm, mother = self.control)
        
        return Organism(MetNet, False, control_son, EnvironmentSituation)

def mutate_DNA(code, rate):
    for i in range(len(code)):
        if rndm.random() < rate:
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


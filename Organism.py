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


class Organism(nx.DiGraph):
    def __init__(self, MetNet, inicial = False, control = None, ES = None):
        self.age = 0
        self.record = 'a'
        self.fitness = 0
        self.mother_record = 'a'
        self.species = 'a'
        food_list = range(Constants.food)

        
        if inicial: #verifica se a populacao eh inicial

            #talvez fosse util ter um dicionario que redireciona pra funcoes
            #dependendo do tipo de inicializacao - inicial ou mutacao - e
            #encapsular uma serie de coisas que por enquanto estao no __init__.

            self.chemistry = deepcopy(MetNet) 
            self.control = Control(inicial)   # cria um controle inicial -> genes ligados por acaso e independentemente
            self.change_environment_org(ES)  #agora seta a comida do controle e da quimica
            self.chemistry.update_reactions(self.control.switch_dict)   #manda sinal dos genes ligados para a rede metabolica
            self.biomass = Constants.division_threshold/2.0        #aqui eh a biomassa do organismo inicial.

        else: #caso a populacao seja gerada de uma mutacao...
            self.chemistry = deepcopy(MetNet)  
            self.control = control
            self.change_environment_org(ES)         #informa os recem-nascidos da situacao de comida...
            self.chemistry.update_reactions(self.control.switch_dict)
            self.biomass = Constants.division_threshold/2.0      #aqui deve ser a biomassa do organismo filho mutado.
            
    
    def change_environment_org(self, food_list):
        self.control.change_environment(food_list)
        self.chemistry.update_food(self.control.food_dict)

    def mutate(self, rate, MetNet, ES):

        DNAp = self.control.export_code()
        DNAm = mutate_DNA(DNAp, rate)
        control_son = Control(DNA = DNAm, mother = self.control)
        
        return Organism(MetNet, False, control_son, ES)
  

    def eval_fitness(self, futurelist):
        pass

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


#!/usr/bin/python 

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
import math
from Environment import Environment
from MetabolicNetwork import MetabolicNetwork
from Constants import Constants
from copy import deepcopy

gray = "#C0C0C0"
green = "#00FF00"
orange = "#FF6600"
purple = "#9900CC"

palette = []


palette.append(gray)
palette.append(green)
palette.append(orange)
palette.append(purple)


plt.ion()

class Control(nx.DiGraph):
    def __init__(self, inicial = False, DNA = None, mother = None):
        # Essa lista de genes ja tem que ser uma lista
        #nao repetida de chaves (hashable), incluindo todas as food molecules
        #quando da criacao de um novo organismo. Essa lista vem vazia
        #num organismo derivado da importacao de um DNA.
        
        nx.DiGraph.__init__(self)
        #Tomar cuidado se for colocar soh parte das food molecules, muitas coisas dependem disso!

        self.switch_dict = {}
        self.colors = []

        self.pot_cn = (Constants.food + Constants.reactions + Constants.intermediate)
        self.K = Constants.food*self.pot_cn      #tamanho da matriz reduzida porque nao ha in-edges nas comidas
        self.DNA_length = (self.pot_cn**2 - self.K)
        
        self.food_list = range(Constants.food)
        self.genes_list = [g + Constants.metabolites for g in range(Constants.genes)]
        self.intermediate_list = [q + Constants.metabolites + Constants.reactions for q in range(Constants.intermediate)]
        self.control_list = self.food_list + self.genes_list + self.intermediate_list


        if inicial:
            self.p = Constants.p                       
            self.generate_minimum()
            self.density = float(Constants.genes + Constants.intermediate)/self.DNA_length

        else:
            DNAcount = self.import_code(DNA, mother)
            self.density = float(DNAcount)/self.DNA_length
        
    def generate_minimum(self):
        
        #ele gera a topologia (com pesos) e ja seta os ligados/desligados iniciais.
        for food in self.food_list:
            self.add_node(food,  {'on': True,'Next': True, 'Threshold': 0})   #CORRIGIR ISSO PRA COMIDA QUE TA ERRADO!!!!!
            self.colors.append(palette[1])

        for gene in self.genes_list:
            r = (True == rndm.randint(0,1))
            self.add_node(gene,  {'on': r, 'Next': r, 'Threshold': 0})  #QUANTO COLOCAR PARA O THRESHOLD?
            self.add_edge(gene, gene, {'w': 1.0})    
            self.colors.append(palette[2 if r else 0])
            if r:
                self.switch_dict.update({gene: True})

	for interm in self.intermediate_list:
	    r = (True == rndm.randint(0,1))
            self.add_node(interm,  {'on': r ,'Next': r , 'Threshold': interm % 2})  #quanto deve ser o threshold inicial??
            self.add_edge(interm, interm, {'w': 1.0})
            self.colors.append(palette[3 if r else 0])


        pos2 = nx.circular_layout(self)
        self.pos = {}
        for i in self.control_list:
            self.pos[i] = pos2[self.nodes()[self.control_list.index(i)]]
        self.draw_BN(self.pos, self.control_list)
        

    def change_state(self):
        # Da um passo na configuracao on/off dos genes             
        self.switch_dict = {}                    
        control_string = []               #vai armazenar zeros e uns de acordo com o estado da comida/genes/intermediarios
        for n in self.nodes():
            if n in range(Constants.food):
                continue
            signal = 0
            control_nodes = self.predecessors(n)
            for cn in control_nodes:
                signal += self.edge[cn][n]['w']*self.node[cn]['on']
            if signal > self.node[n]['Threshold']:
                if self.node[n]['on'] == False:
                    self.node[n]['Next'] = True
                    if n in self.genes_list:
                        self.switch_dict.update({n:True})                                     
                
            else:
                if self.node[n]['on'] == True:
                    self.node[n]['Next'] = False
                    if n in self.genes_list:
                        self.switch_dict.update({n:False})


## Tentar fazer esse primeiro for com o switch_dict

        for food in self.food_list:
            control_string.append(self.node[food]['on'] + 0)

        for gene in self.genes_list:                                             
            self.node[gene]['on'] = self.node[gene]['Next']
            self.colors[Constants.food + self.genes_list.index(gene)] = palette[2 if self.node[gene]['on'] else 0]   #colorir nos no update
            control_string.append(self.node[gene]['on'] + 0)

        for inter in self.intermediate_list:
            self.node[inter]['on'] = self.node[inter]['Next']            #colorir nos no update
            self.colors[Constants.food + Constants.genes + self.intermediate_list.index(inter)] = palette[3 if self.node[inter]['on'] else 0]  
            control_string.append(self.node[inter]['on'] + 0)


        self.draw_BN(self.pos, self.control_list)
        
        return control_string

    def export_code(self):

        DNA = [0]*self.DNA_length
        for a, b in self.edges():         
            aa = a if a in range(Constants.food) else a - Constants.metabolites + Constants.food
            bb = b - Constants.metabolites + Constants.food
            DNA[bb*self.pot_cn + aa - self.K] = self.edge[a][b]['w']

        return DNA
        
    def import_code(self, DNA, mother = None):

        DNAcount = 0

        for fc in self.control_list:
            self.add_node(fc)         

        for index in (i for i in xrange(len(DNA)) if abs(DNA[i]) == 1):
            a = (index + self.K)%self.pot_cn
            b = (index + self.K - a)/self.pot_cn
            aa = a if a in range(Constants.food) else a + Constants.metabolites - Constants.food
            bb = b + Constants.metabolites - Constants.food
            self.add_edge(aa, bb, {'w': DNA[index]})
            DNAcount += 1

        for f in self.food_list:
            self.node[f] = {'on': True,'Next': True, 'Threshold': 0}       #muito feio.... rever!!!
            self.colors.append(palette[self.node[f]['on'] + 0])                    

        for n in self.genes_list + self.intermediate_list:

            if rndm.random() > Constants.rate:
                #self.node[n] = {'on': mother.node[n]['on'],'Next': mother.node[n]['on'], 'Threshold': mother.node[n]['Threshold'] if rndm.random() > Constants.rate else (mother.node[n]['Threshold'] + 2*rndm.randint(0,1) - 1)}  COPIAR DEPOIS
                self.node[n] = {'on': mother.node[n]['on'],'Next': mother.node[n]['on'], 'Threshold': mother.node[n]['Threshold'] if rndm.random() > Constants.rate else (mother.node[n]['Threshold'] + 2*rndm.randint(0,1) - 1 if mother.node[n]['Threshold'] not in [-5, 4] else mother.node[n]['Threshold'] + int(math.copysign(rndm.randint(0,1), -mother.node[n]['Threshold'])))}
                if mother.node[n]['on'] and n in self.genes_list: 
                    self.switch_dict.update({n: True})

            else: #COLOQUEI MUTACAO NO ESTADO ON/OFF DOS GENES/INTERM DE UMA GERACAO PRA OUTRA!
                self.node[n] = {'on': not mother.node[n]['on'],'Next': not mother.node[n]['on'], 'Threshold': mother.node[n]['Threshold'] if rndm.random() > Constants.rate else (mother.node[n]['Threshold'] + 2*rndm.randint(0,1) - 1 if mother.node[n]['Threshold'] not in [-5, 4] else mother.node[n]['Threshold'] + int(math.copysign(rndm.randint(0,1), -mother.node[n]['Threshold'])))}
                if not mother.node[n]['on'] and n in self.genes_list: 
                    self.switch_dict.update({n: True})

            self.colors.append(palette[(2 if n in self.genes_list else 3) if self.node[n]['on'] else 0])

        pos2 = nx.circular_layout(self)
        self.pos = {}
        for i in self.nodes():
            self.pos[i] = pos2[self.nodes()[self.nodes().index(i)]]  #Desembaralhar essa merda....

        self.draw_BN(self.pos, self.nodes())    #Na falta de alternativa melhor, desenha-se duas vezes para funcionar.
        self.draw_BN(self.pos, self.nodes())

        return DNAcount

    def change_environment(self, food_list):
        #food_list tem que ter o comprimento do numero de food_total sempre!!
        #A posicao correspondente a molecula f deve conter True ou False,
        #dependendo da condicao de disponibilidade daquela food_molecule

        self.food_dict = {}     #QUAL EH O LANCE DESSE DICIONARIO? ELE NAO ESTAVA SEMPRE PREENCHIDO, SOH COM AS COISAS QUE MUDAVAM?
        
        for f in range(Constants.food):
            if food_list[f]:
                self.node[f] = {'on': True,'Next': True, 'Threshold': 0}        #mudar aqui tambem! comida nao tem threshold!!!
                self.colors[f] = palette[1]    
                self.food_dict.update({f: True})                      
            else:
                self.node[f] = {'on': False,'Next': False, 'Threshold': 0}
                self.colors[f] = palette[0]
                self.food_dict.update({f: False}) 
                     

    def draw_BN(graph, positions, listadenos):

        #plt.clf()
        #nx.draw_networkx_labels(graph, positions)
        #nx.draw_networkx_nodes(graph,positions, nodelist = listadenos, node_color=graph.colors,node_size=150)
        #nx.draw_networkx_edges(graph,positions,alpha=0.3)
        #plt.draw()
        #plt.draw()
        pass

def mutate_DNA(code, rate):
    for i in range(len(code)):
        if rndm.random() <= rate:
            code[i] = (code[i]%3 + 2*rndm.randint(0,1))%3 - 1
    return code
    
def randomenv():

    primeiragerac = Control(inicial = True)
    
    dna = primeiragerac.export_code()
    time.sleep(5)

    segundagerac = Control(DNA = dna, mother = primeiragerac) ##se a mae for indicada, o filho herda a configuracao


    for t in range(70):
        dna = segundagerac.export_code()
        dna = mutate_DNA(dna, 0.01)
        segundagerac = Control(DNA = dna)
        
if __name__ == '__main__':
    randomenv()

#!/usr/bin/python 

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
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
    def __init__(self, genes_list = [], inicial = False, DNA = None, mother = None):
        # Essa lista de genes ja tem que ser uma lista
        #nao repetida de chaves (hashable), incluindo todas as food molecules
        #quando da criacao de um novo organismo. Essa lista vem vazia
        #num organismo derivado da importacao de um DNA.
        
        nx.DiGraph.__init__(self)
        #Tomar cuidado se for colocar soh parte das food molecules, muitas coisas dependem disso!

        self.switch_dict = {}
        self.colors = []

        pot_cn = (Constants.food + Constants.reactions + Constants.intermediate)
        K = Constants.food*pot_cn
        self.DNA_length = (pot_cn**2 - K)
       
        if inicial:
            self.p = Constants.p
            self.genes_list = genes_list
            #nessa genes_list ja ta incluida a lista de food molecules
            #cuidado! Nao existe uma verificacao
            #por chaves repetidas nessa lista!!
            
            self.number_food_actual = len([f for f in self.genes_list if f in range(Constants.food)])            
            self.number_genes = len(genes_list)
            self.generate_minimum()
            self.density = float(self.number_genes - self.number_food_actual)/self.DNA_length
##            self.generate_random()
        else:
            self.genes_list = []
            DNAcount = self.import_code(DNA, mother)
            self.number_food_actual = len([f for f in self.genes_list if f in range(Constants.food)])
            self.density = float(DNAcount)/self.DNA_length
        
        self.intermediate_list = sorted([presinterm for presinterm in self.nodes() if presinterm in [q + Constants.reactions + Constants.metabolites for q in range(Constants.intermediate)]])
        

    def generate_minimum(self):
        
        #ele gera a topologia (com pesos) e ja seta os ligados/desligados iniciais.
        for gene in range(self.number_genes):
            r = (True == rndm.randint(0,1))
            self.add_node(self.genes_list[gene],  {'on': r or (gene in range(Constants.food)),'Next': r or (gene in range(Constants.food)), 'Threshold': 0})
            if gene not in range(Constants.food):
                self.add_edge(self.genes_list[gene], self.genes_list[gene], {'w': 1.0})
                self.colors.append(palette[2 if r else 0])
            else:
                self.colors.append(palette[1])
            if r and (gene not in range(Constants.food)): #or (gene1 in range(Constants.food)):
                self.switch_dict.update({self.genes_list[gene]:True})
       
	for interm in range(Constants.intermediate):
	    r = (True == rndm.randint(0,1))
            self.add_node(interm + Constants.metabolites + Constants.reactions,  {'on': r ,'Next': r , 'Threshold': interm % 2})  #quanto deve ser o threshold inicial??
            self.colors.append(palette[3 if r else 0])


        pos2 = nx.circular_layout(self)
        self.pos = {}
        for i in self.genes_list + [c + Constants.metabolites + Constants.reactions for c in range(Constants.intermediate)]:
            self.pos[i] = pos2[self.nodes()[(self.genes_list + [c + Constants.metabolites + Constants.reactions for c in range(Constants.intermediate)]).index(i)]]

        self.draw_BN(self.pos, self.genes_list)
        

    def change_state(self):
        # Da um passo na configuracao on/off dos genes             
        self.switch_dict = {}                    
        gene_string = []               #vai armazenar zeros e uns de acordo com o estado da comida/genes/intermediarios
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
                    if n in range(Constants.metabolites + Constants.reactions):
                        self.switch_dict.update({n:True})                                     
                
            else:
                if self.node[n]['on'] == True:
                    self.node[n]['Next'] = False
                    if n in range(Constants.metabolites + Constants.reactions):
                        self.switch_dict.update({n:False})


## Tentar fazer esse primeiro for com o switch_dict
        for n in range(self.number_genes):                                                 
            self.node[self.genes_list[n]]['on'] = self.node[self.genes_list[n]]['Next']
            self.colors[n] = palette[(1 if n in range(Constants.food) else 2) if self.node[self.genes_list[n]]['on'] else 0]   #colorir nos no update
            gene_string.append(self.node[self.genes_list[n]]['on'] + 0)
        for inter in self.intermediate_list:
            self.node[inter]['on'] = self.node[inter]['Next']
            self.colors[self.number_genes + self.intermediate_list.index(inter)] = palette[3 if self.node[inter]['on'] else 0]  #colorir nos no update
            gene_string.append(self.node[inter]['on'] + 0)



        self.draw_BN(self.pos, self.genes_list)
        #print 'gene_string = ' + str(gene_string)
        #print self.nodes()
        
        return gene_string

    def export_code(self):
        pot_cn = (Constants.food + Constants.reactions + Constants.intermediate)
        K = Constants.food*pot_cn

        DNA = [0]*self.DNA_length
        for a, b in self.edges():         
            aa = a if a in range(Constants.food) else a - Constants.metabolites + Constants.food
            bb = b - Constants.metabolites + Constants.food
            DNA[bb*pot_cn + aa - K] = self.edge[a][b]['w']

        return DNA
        
    def import_code(self, DNA, mother = None):
        #As geracoes mutadas ja nao terao mais nodes no controle de food molecules se elas nao estiverem conectadas a nada... 
        pot_cn = (Constants.food + Constants.reactions + Constants.intermediate)
        K = Constants.food*pot_cn #tamanho da matriz retirado porque nao ha in-edges nas comidas
        DNAcount = 0
       
        for index in (i for i in xrange(len(DNA)) if abs(DNA[i]) == 1):
            a = (index + K)%pot_cn
            b = (index + K - a)/pot_cn
            aa = a if a in range(Constants.food) else a + Constants.metabolites - Constants.food
            bb = b + Constants.metabolites - Constants.food
            self.add_edge(aa, bb, {'w': DNA[index]})
            DNAcount += 1
        
        for f in range(Constants.food + Constants.genes + Constants.intermediate):
            fc = f if f in range(Constants.food) else f + Constants.metabolites - Constants.food
            if fc not in self.nodes():
                self.add_node(fc)
                
        self.genes_list = deepcopy([g for g in self.nodes() if g < Constants.metabolites + Constants.reactions])
        self.genes_list.sort()
        self.number_genes = len(self.genes_list)

        if mother is None:
            for n in self.genes_list + sorted([presinterm for presinterm in self.nodes() if presinterm in [q + Constants.reactions + Constants.metabolites for q in range(Constants.intermediate)]]):
                r = (True == rndm.randint(0,1))
                self.node[n] = {'on': r or (n in range(Constants.food)),'Next': r or (n in range(Constants.food)), 'Threshold': rndm.randint(-3,3)}
                if r and (n not in range(Constants.food)) and n < Constants.metabolites + Constants.reactions:
                    self.switch_dict.update({n: True})

                self.colors.append(palette[self.node[n]['on'] + 0])

        else:
            for n in self.genes_list + sorted([presinterm for presinterm in self.nodes() if presinterm in [q + Constants.reactions + Constants.metabolites for q in range(Constants.intermediate)]]):
                if n in mother.nodes():
                    if (rndm.random() > Constants.rate or n in range(Constants.food)):
                        #print 'mother.node[' + str(n) + '] = ' + str(mother.node[n])
                        self.node[n] = {'on': mother.node[n]['on'],'Next': mother.node[n]['on'], 'Threshold': mother.node[n]['Threshold'] if rndm.random() > Constants.rate else (mother.node[n]['Threshold'] + 2*rndm.randint(0,1) - 1)}
                        if mother.node[n]['on'] and (n not in range(Constants.food)) and n < Constants.metabolites + Constants.reactions: 
                            self.switch_dict.update({n: True})
                    else: #COLOQUEI MUTACAO NO ESTADO ON/OFF DOS GENES/INTERM DE UMA GERACAO PRA OUTRA!
                        self.node[n] = {'on': not mother.node[n]['on'],'Next': not mother.node[n]['on'], 'Threshold': mother.node[n]['Threshold'] if rndm.random() > Constants.rate else (mother.node[n]['Threshold'] + 2*rndm.randint(0,1) - 1)}
                        if not mother.node[n]['on'] and (n not in range(Constants.food)) and n < Constants.metabolites + Constants.reactions: 
                            self.switch_dict.update({n: True})
                else:
                    r = (True == rndm.randint(0,1))
                    self.node[n] = {'on': r,'Next': r, 'Threshold': rndm.randint(0,1)}
                    if r and (n not in range(Constants.food)) and n < Constants.metabolites + Constants.reactions:
                        self.switch_dict.update({n: True})

                self.colors.append(palette[self.node[n]['on'] + 0])

        pos2 = nx.circular_layout(self)

        #print 'self.node = ' + str(self.node)
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
                if f not in self.nodes():
                    self.add_node(f,  {'on': True,'Next': True, 'Threshold': 0})
                    fobj = open('organised2013/WARNING.txt', 'a')
                    fobj.write('\nNa hora de mudar ambiente alguma food molecule teve que ser adicionada ao controle cujo numero eh:')
                    fobj.write(str(f))
                    fobj.close()
                else:
                    self.node[f] = {'on': True,'Next': True, 'Threshold': 0}
                        
                self.food_dict.update({f: True})
                      
            else:
                if f in self.nodes():
                    self.node[f] = {'on': False,'Next': False, 'Threshold': 0}
                else:
                    self.add_node(f,  {'on': False,'Next': False, 'Threshold': 0})    
                    fobj = open('organised2013/WARNING.txt', 'a')
                    fobj.write('\nNa hora de mudar ambiente alguma food molecule desligada teve que ser adicionada ao controle cujo numero eh:')
                    fobj.write(str(f))
                    fobj.close()
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

    react_list = [x + Constants.metabolites for x in range(Constants.reactions)]
    food_list = range(Constants.food)
    genes_list = food_list + sorted(rndm.sample(react_list, Constants.genes))

    primeiragerac = Control(genes_list, inicial = True)
    
    dna = primeiragerac.export_code()
    time.sleep(5)
##    segundagerac = Control(food_total, metabolites, [], 0, reac_total, DNA = dna)
    segundagerac = Control(DNA = dna, mother = primeiragerac) ##se a mae for indicada, o filho herda a configuracao


    for t in range(70):
        dna = segundagerac.export_code()
        dna = mutate_DNA(dna, 0.01)
        segundagerac = Control(DNA = dna)
        
if __name__ == '__main__':
    randomenv()
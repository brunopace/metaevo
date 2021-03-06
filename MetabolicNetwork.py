#! /usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import time
from Constants import Constants
from Environment import Environment

class TargetException(Exception):
    pass

class FoodException(Exception):
    pass

class MetaboliteNumberException(Exception):
    pass



class MetabolicNetwork(nx.DiGraph):

    #fazer uma versao depois com as reacoes liga/desliga fluindo materia
    #(sem precisar que o path esteja inteiro aberto ao mesmo tempo)
    
    def __init__(self, env_list = None):
        nx.DiGraph.__init__(self)

        if Constants.targets > Constants.metabolites:
            raise TargetException('The number of targets cannot exceed the number of metabolites!')
        if Constants.food < 1:
            raise FoodException('There are no food molecules!')
        if Constants.targets + Constants.food > Constants.metabolites:
            raise MetaboliteNumberException('There are more food and target molecules than possible!')


        if env_list is None:
            self.generate_random()
            while not self.is_problem_solvable():
                self.clear()
                self.generate_random()

            print 'Solution found!'
            print 'target1:' + str(Constants.food)
            print 'number of targets: ' + str(Constants.targets) 
            
        elif env_list == 'difficult':
            self.generate_difficult()
        
        elif env_list == 'minimum':
           self.generate_minimum()

        elif env_list == 'minimum_difficult':
           self.generate_minimum_difficult()
        
        else:
            self.generate_random()
            flag = False
            while not flag:
                flag = True
                for e in env_list:
                    ver = (self.is_problem_solvable(e) > 0)
                    flag = flag and ver
                if not flag:
                    self.clear()
                    self.generate_random()
            

            print 'Solution multiple environment found!'
            print 'target1:' + str(Constants.food)
            print 'number of targets: ' + str(Constants.targets) 
            
        self.react_list = [x for x in self.nodes() if self.node[x]['Type'] == 'R']
        self.metab_list = [x for x in self.nodes() if self.node[x]['Type'] == 'M']
        self.target_list = [x for x in self.nodes() if self.node[x]['Type'] == 'M' and self.node[x]['Target'] == 'True']  #para uso futuro

        self.path_to_target()
        self.turn_off_met()
            
    def generate_difficult(self):
        for food in range(20):
            self.add_node(food, {'Type':'M','Food': True ,'Target': False, 'Flowing': True})
        for targ in range(1):
            self.add_node(targ + 20, {'Type':'M','Food': False ,'Target': True, 'Flowing': False})
        for metab in range(14):
            self.add_node(21 + metab, {'Type':'M','Food': False ,'Target': False, 'Flowing': False})
            
        for react in range(17):
            self.add_node(35 + react,{'Type':'R', 'on': False})

        edges = [ (0, 35),(1, 35),(2, 36),(3, 36),(4, 37),(5, 37),(6, 38),\
                  (7, 38),(8, 39),(9, 39),(10, 46),(11, 46),(12, 40),(13, 40),\
                  (14, 41),(15, 41),(16, 42),(17, 42),(18, 43),(19, 43),(21, 44),\
                  (22, 49),(23, 45),(24, 45),(25, 47),(26, 47),(27, 48),(28, 48),\
                  (29, 44),(30, 49),(31, 50),(32, 50),(33, 51),(34, 51),(35, 29),\
                  (36, 21),(37, 22),(38, 23),(39, 24),(40, 25),(41, 26),(42, 27),\
                  (43, 28),(44, 30),(45, 31),(46, 32),(47, 33),(48, 34),(49, 20),\
                  (50, 20),(51, 20)]
        for e in edges:
          self.add_edge(e[0], e[1], {'weight':rndm.randint(1,5)})

    def generate_minimum(self):
        for f in range(2):
            self.add_node(f, {'Type':'M','Food': True ,'Target': False, 'Flowing': True})
        self.add_node(2, {'Type':'M','Food': False ,'Target': True, 'Flowing': False})
        self.add_node(3, {'Type':'R', 'on': False})

        edges = [(0,3),(1,3),(3,2)]

        for e in edges:
          self.add_edge(e[0], e[1], {'weight':rndm.randint(1,5)})        

    def generate_minimum_difficult(self):
        for f in range(6):
            self.add_node(f, {'Type':'M','Food': True ,'Target': False, 'Flowing': True})
        self.add_node(6, {'Type':'M','Food': False ,'Target': True, 'Flowing': False})
        for r in range(3):
            self.add_node(7 + r, {'Type':'R', 'on': False})

        edges = [(0,7),(1,7),(2,8),(3,8),(4,9),(5,9),(7,6),(8,6),(9,6)]

        for e in edges:
          self.add_edge(e[0], e[1], {'weight':rndm.randint(1,5)})   

    def generate_random(self):
        #gera o digrafo bipartido, com metabolitos e reacoes.dogs kissing

        #pos = {}
        for food in xrange(Constants.food):
            self.add_node(food, {'Type':'M','Food': True ,'Target': False, 'Flowing': True})
        for targ in xrange(Constants.targets):
            self.add_node(targ + Constants.food, {'Type':'M','Food': False ,'Target': True, 'Flowing': False})
        for metab in xrange(Constants.metabolites - Constants.targets - Constants.food):
            #pos[metab] = (0,metab)
            self.add_node(Constants.targets + Constants.food + metab, {'Type':'M','Food': False ,'Target': False, 'Flowing': False})
            
        for react in xrange(Constants.reactions):
            #pos[react+metabolites] = (metabolites, float(react)*metabolites/reactions)
            self.add_node(Constants.metabolites + react,{'Type':'R', 'on': False})
##            inm = rndm.randint(1,3)
            inm = 2
##            outm = rndm.randint(1,3)  #talvez fazer isso ser igual a um...
            outm = 1
            cj = rndm.sample([x for x in self.nodes() if self.node[x]['Type']=='M'],inm+outm)
            for i in range(inm):
                self.add_edge(cj.pop(rndm.randint(0,inm+outm-1-i)), Constants.metabolites + react, {'weight':rndm.randint(1,5)}) #se for precisar desse peso...
            for o in range(outm):
                self.add_edge(Constants.metabolites + react, cj.pop(rndm.randint(0,outm-1-o)),{'weight':rndm.randint(1,5)})

        #print 'reacoes ligadas:'
        #reac_list = [rea for rea in self.node if self.node[rea]['Type'] == 'R']
        #print len([act for act in reac_list if self.node[act]['on'] == True])

    def update_reactions(self, reaction_dict):
        #Faz 'Flowing' virar False pra limpar e comecar de novo, assim como atualiza as reacoes que (des)ligaram.
        #tem que receber um dicionario com as chaves corretas, so com as reacoes a serem atualizadas
    
        for react in reaction_dict:
            self.node[react]['on'] = reaction_dict[react]

        for m in self.metab_list:
            if not self.node[m]['Food']:
                self.node[m]['Flowing'] = False

        return self.path_to_target()

    def update_food(self, food_dict):
        for f in food_dict:
            self.node[f]['Flowing'] = food_dict[f]
        self.update_reactions({})

    def path_to_target(self):
        #Tem que sempre ser usado depois de update_reactions, pra ter o 'Flowing' zerado!
        update = True
        react_possible = True
        
        while update:      #faz com que as comidas percolem pela rede atraves das reacoes ligadas
            update = False
            for r in self.react_list:
                if self.node[r]['on']:
                    educts = [e for e, x in self.in_edges(r)]
                    for s in range(len(educts)):  
                        react_possible = react_possible and self.node[educts[s]]['Flowing'] 
                    if react_possible:
                        products = self.successors(r)
                        for t in range(len(products)):
                            react_possible = react_possible and self.node[products[t]]['Flowing']
                            self.node[products[t]]['Flowing'] = True
                        if not react_possible:
                            update = True
                    react_possible = True

        #print [x for x in self.node]
        #print 'resultado path_to_target:'
        #print len([x for x in metab_list if (self.node[x]['Target'] == True and self.node[x]['Flowing'] == True)])
        #print 'path to target: ' + str(len([x for x in metab_list if (self.node[x]['Target'] == True and self.node[x]['Flowing'] == True)]))

        return len([x for x in self.metab_list if (self.node[x]['Target'] == True and self.node[x]['Flowing'] == True)])

    def is_problem_solvable(self, env = None): #incluir outras configuracoes de comida
        #Esse metodo liga todas as reacoes, tem que usar turn_off_met depois!!!

        for react in self.react_list:
            self.node[react]['on'] = True
        #print self.node

        for m in self.metab_list:
            if not self.node[m]['Food']:
                self.node[m]['Flowing'] = False
        if env != None:
            for f in range(Constants.food):
                self.node[f]['Flowing'] = env[f]
            
        return self.path_to_target()

    def turn_off_met(self): #incluir outras configuracoes de comida
        for react in self.react_list:
            self.node[react]['on'] = False
        
        for m in self.metab_list:
            if self.node[m]['Food']:
                self.node[m]['Flowing'] = True
            else:
                self.node[m]['Flowing'] = False




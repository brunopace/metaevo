import random as rndm

class Constants():
    

    die = True
    intermenergy = True   # se False os intermediarios nao sao contabilizados na fracao de enzimas
    varthresh = True      # para ligar as mutacoes dos thresholds 
    food = 2
    targets = 1
    metabolites = 3      #no minimo igual a food + targets
    reactions = 1
    genes = 1             #tem que ser menor ou igual ao numero de reacoes
    intermediate = 8
    p = 0.0
    population_size = 100
    division_threshold = 10
    record_size = 10
    rate = 0.005                                  
    number_environments = 4
    envchg_period = 12
    env_change_rate = 0.00
    peso = 1 /2.0               # a tendencia eh que em 1/number_environments do tempo se produz biomassa e o peso tem que compensar pelo desconto 
    ta = 100                                #para que os organismos nao morram tem que ser 1/6. div_thresh/(envchg_period*enzyme_fraction tolerada)
    tb = 1000              #escala de tempo para escrever o genoma no arquivo
    end_step = 200000
    env_dict = {'difficult': [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))], 'periodic2': [[True]*(food/2) + [False]*(food - food/2),[False]*(food/2) + [True]*(food - food/2)], 'minimum':[[True,True], [True, False], [False, False], [False, True]], 'minimum2': [[True,True], [False, True], [True,True], [True, False], [True,True], [False, False]], 'minimum_difficult':[[True, True, False, False, False, False],[True, False, False, False, False, False],[False, False, True, True, False, False],[False, False, True, False, False, False],[False, False, False, False, True, True],[False, False, False, False, True, False],[True, True, False, False, False, False],[False, True, False, False, False, False],[False, False, True, True, False, False],[False, False, False, True, False, False],[False, False, False, False, True, True],[False, False, False, False, False, True]]}

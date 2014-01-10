import random as rndm

class Constants():
    

    die = True
    intermenergy = True   # se False os intermediarios nao sao contabilizados na fracao de enzimas
    varthresh = True      # para ligar as mutacoes dos thresholds 
    food = 2
    targets = 1
    metabolites = 3      #no minimo igual a food + targets
    reactions = 1         #daqui pra frente temos controlabilidade total -> REACTIONS = GENES
    genes = reactions             # a partir de uma certa versao eles se tornaram iguais -> potencial de controlabilidade total
    
    intermediate = 0
    
    p = 0.0    #deletar
    
    population_size = 100

    division_threshold = 10
    record_size = 10           #deletar                                       
    rate = 0.1                                  
    number_environments = 4
    envchg_period = 12              #12
    env_change_rate = 0.00                      #pra conseguir dividir no verao, peso < 1 - div_thresh/envchg_period
    peso = 0.1388               # a tendencia eh que em 1/number_environments do tempo se produz biomassa e o peso tem que compensar pelo desconto 
    ta = 100                                #para que os organismos nao morram tem que ser 1/6. div_thresh/(envchg_period*enzyme_fraction tolerada)
    tb = 1000              #escala de tempo para escrever o genoma no arquivo
    end_step = 800000
    env_dict = {'difficult': [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))], 'periodic2': [[True]*(food/2) + [False]*(food - food/2),[False]*(food/2) + [True]*(food - food/2)], 'minimum':[[True,True], [True, False], [False, False], [False, True]], 'minimum2': [[True,True], [False, True], [True,True], [True, False], [True,True], [False, False]], 'minimum_difficult':[[True, True, False, False, False, False],[True, False, False, False, False, False],[False, False, True, True, False, False],[False, False, True, False, False, False],[False, False, False, False, True, True],[False, False, False, False, True, False],[True, True, False, False, False, False],[False, True, False, False, False, False],[False, False, True, True, False, False],[False, False, False, True, False, False],[False, False, False, False, True, True],[False, False, False, False, False, True]]}

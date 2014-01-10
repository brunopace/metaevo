import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math
import time

attractor = [142, 10, 32, 211, 202, 51, 132, 12, 50, 130, 190, 131, 81, 140, 231, 232, 42, 242, 202, 162, 82, 120, 20, 12, 212, 30, 162, 70, 40, 160, 111, 62, 211, 120, 261, 130, 180, 52, 53, 51, 40, 241, 1, 22, 202, 230, 201, 120, 113, 40, 111, 130, 171, 250, 220, 62, 211, 160, 231, 220, 120, 111, 200, 200, 212, 172, 191, 140, 182, 10, 251, 150, 90, 31, 112, 211, 70, 70, 0, 162, 82, 90, 11, 240, 60, 22, 180, 110, 42, 211, 202, 220, 210, 230, 111, 80, 70, 222, 30, 133]

c = "#909090"   #SD
v = "#00FF00"   #VL3
l = "#FF6600"   #CI
r = "#9900CC"   #VL12
m = "#FF0000"   #SL
z = "#0000FF"   #VL4
y = "#FFFF00"   #LIXO
a = "#00FFFF"   #OSCV
b = "#FFFFFF"   #


LIXO = [3, 4, 13, 14, 24, 34, 44, 65, 75, 85, 94, 104, 185, 195]
SD = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 45, 46, 47, 48, 49, 55, 56, 57, 58, 59, 66, 67, 68, 69, 76, 77, 78, 79, 86, 87, 88, 89, 95, 96, 97, 98, 99, 105, 106, 107, 108, 109, 115, 116, 117, 118, 119, 125, 126, 127, 128, 129, 135, 136, 137, 138, 139, 146, 147, 148, 149, 156, 157, 158, 159, 166, 167, 168, 169, 176, 177, 178, 179, 186, 187, 188, 189, 196, 197, 198, 199, 206, 207, 208, 209, 216, 217, 218, 219, 226, 227, 228, 229, 236, 237, 238, 239, 247, 248, 249, 257, 258, 259, 267, 268, 269]
SL = [0, 1, 10, 11, 12, 20, 21, 22, 23, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54, 60, 61, 62, 70, 71, 72, 73, 80, 81, 82, 83, 84, 90, 91, 92, 100, 101, 102, 103, 110, 111, 112, 113, 114, 120, 121, 122, 123, 130, 131, 132, 133, 134, 140, 141, 142, 143, 144, 145, 150, 151, 152, 153, 160, 161, 162, 163, 164, 170, 171, 172, 173, 174, 175, 180, 181, 182, 190, 191, 192, 193, 200, 201, 202, 203, 204, 210, 211, 212, 213, 220, 221, 222, 223, 224, 230, 231, 232, 233, 234, 235, 240, 241, 242, 243, 250, 251, 252, 253, 254, 260, 261, 262, 263, 264, 265]
OSCV = [2, 33, 64, 93, 124, 155, 184, 215, 246]
VL = [63, 74, 154, 165, 183, 194, 205, 214, 225, 244, 245, 255, 256, 266]

VL1 = [63, 183, 244]
VL2 = [74, 154, 194, 214, 255]
VL3 = [165, 205, 225, 245, 266]
VL4 = [256]

CI = [145]
OR = [165, 225]
SADDLE = [255]


#color = [(('r' if i not in VL3 else 'g') if i != 256 else 'b') if i not in a else 'w' for i in range(270)]
color = [c if i in SD else v if i in VL3 else m if i in SL else z if i in VL4 else r if i in VL1+VL2 else y if i in LIXO else a if i in OSCV else b for i in range(270)]

color[145] = l

envchg_period = 12
step = 1
weights = [-1, 0, 1]
eps = 0.01      #para eps < 0.11 a maioria da populacao se localiza no pico (256)
maxfit = (0, 0)
HG = nx.Graph()
idx = 0


def hamming_distance(DNA, DNB):
    if len(DNA) != len(DNB):
        return -1
    dist = [0]*len(DNA)
    for i in range(3):
        if DNA[i] != DNB[i]:
            dist[i] += 1
    dist[3] += abs(DNA[3] - DNB[3]) 
    return dist

for i in weights:        #i eh entrada da comida A, j da comida B e k eh o self-loop
    for j in weights:
        for k in weights:
            for thresh in [th-5 for th in range(10)]:
                HG.add_node(idx,  {'genotype': (i, j, k, thresh)})
                idx += 1

def indextogenotype(i):
    genot = [-1,-1,-1,-5]
    while i >= 90:
        genot[0] +=1
        i -= 90
    while i >= 30:
        genot[1] +=1
        i -= 30
    while i >= 10:
        genot[2] +=1
        i -= 10
    while i >= 1:
        genot[3] +=1
        i -= 1
    return tuple(genot)

for Da in HG.nodes():
    for Db in HG.nodes():
        if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [0,1,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,0,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,0,0,1]:
            HG.add_edge(Da, Db, {'d': 1})
        #if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,0,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [1,0,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [0,0,1,1]:
        #    HG.add_edge(Da, Db, {'d': 2})
        #if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,1,0] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) ==  [1,1,0,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,0,1,1] or hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [0,1,1,1]:
        #    HG.add_edge(Da, Db, {'d': 3})
        #if hamming_distance(HG.node[Da]['genotype'], HG.node[Db]['genotype']) == [1,1,1,1]:
        #    HG.add_edge(Da, Db, {'d': 4})


nx.draw(HG, node_color = color, with_labels=False, node_size=40)
plt.savefig("graph.png", dpi=1000)
plt.show()


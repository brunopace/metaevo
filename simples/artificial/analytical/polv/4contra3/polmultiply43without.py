import matplotlib.pyplot as plt
import math
import time
import copy

ta = time.time()

L = 5

nul = [[[[0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)]
eps = [[[[1 if (e==1 and a==0 and x==0 and v==0) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)]
up = [[[[1 if (e==0 and a==0 and x==0 and v==0) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)]#polinomio 1
uma = [[[[1 if (e==0 and a==0 and x==0 and v==0) else -1 if (e==0 and a==1 and x==0 and v==0) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)] 
ume = [[[[1 if (e==0 and a==0 and x==0 and v==0) else -1 if (e==1 and a==0 and x==0 and v==0) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)] 
umxmv = [[[[1 if (e==0 and a==0 and x==0 and v==0) else -1 if ((e==0 and a==0 and x==1 and v==0) or (e==0 and a==0 and x==0 and v==1)) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)] 
xis = [[[[1 if (e==0 and a==0 and x==1 and v==0) else 0 for e in range(L)] for a in range(L)] for x in range(L)] for v in range(L)]


def Dab(v):
    return [psum(polmult(ume,v[0]),polmult(eps,v[1])), psum(polmult(eps,v[0]),polmult(ume,v[1]))]

def Da(v):
    return [polmult(ume,v[0]), polmult(eps,v[0])]

def Db(v):
    return [polmult(eps,v[1]), polmult(ume,v[1])]

def polmult(p1,p2):
    res  = copy.deepcopy(nul)
    for i1 in range(L):
        for j1 in range(L):
            for k1 in range(L):
                for l1 in range(L):
                    for i2 in range(L):
                        for j2 in range(L):
                            for k2 in range(L):
                                for l2 in range(L):
                                    if (p1[i1][j1][k1][l1] != 0 and p2[i2][j2][k2][l2] != 0):
                                        if i1+i2 >= L:    
                                            #print 'j1+j2 = ' + str(j1+j2)
                                            continue
                                        if j1+j2 >= L:    
                                            #print 'j1+j2 = ' + str(j1+j2)
                                            continue
                                        if k1+k2 >= L:
                                            #print 'k1+k2 = ' + str(k1+k2)
                                            continue
                                        if l1+l2 >= L:
                                            #print 'l1+l2 = ' + str(l1+l2)
                                            continue
                                        res[i1+i2][j1+j2][k1+k2][l1+l2] = p1[i1][j1][k1][l1]*p2[i2][j2][k2][l2]

    print 'multiplicacao interna'
    printpol(res)
    print '---------------------------------------------------------------------------------------'
    return res
                    
                    

def psum(p1,p2):
    res = copy.deepcopy(nul)
    for i in range(L):
        for j in range(L):
            for k in range(L):
                for l in range(L):
                    res[i][j][k][l] += (p1[i][j][k][l] + p2[i][j][k][l])
    return res

def mp(p): #troca o sinal
    res = copy.deepcopy(p)
    for i in range(L):
        for j in range(L):
            for k in range(L):
                for l in range(L):
                    res[i][j][k][l] = -res[i][j][k][l]
    return res


def printpol(p):
    string = 'p = '
    for i in range(L):
        for j in range(L):
            for k in range(L):
                for l in range(L):
                    if p[i][j][k][l] != 0:
                        if (p[i][j][k][l] > 0 and len(string)>4):
                            string += '+'
                        string += str(p[i][j][k][l])
                        if i != 0:
                            string += '*v'
                            if i != 1:
                                string += '**'+str(i)
                        if j != 0:
                            string += '*x'
                            if j != 1:
                                string += '**'+str(j)
                        if k != 0:
                            string += '*a'
                            if k != 1:
                                string += '**'+str(k)
                        if l != 0:
                            string += '*e'
                            if l != 1:
                                string += '**'+str(l)


    print string
    return string

def fdab(v0, entry):
    A = Dab(v0)
    ng = [polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[0]),polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[1])]
    v1 = [polmult(uma,psum(ng[0],v0[0])),polmult(uma,psum(ng[1],v0[1]))]
    v0 = copy.deepcopy(v1)

    print 'v0:'
    q1=printpol(v0[0])
    print 'v1:'
    q2=printpol(v0[1])

    fobj = open(entry + '1.txt', 'a')
    fobj.write(q1)
    fobj.close()

    fobj = open(entry + '2.txt', 'a')
    fobj.write(q2)
    fobj.close()

    return v0

def fda(v0, entry):
    A = Da(v0)
    ng = [polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[0]),polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[1])]
    v1 = [polmult(uma,psum(ng[0],v0[0])),polmult(uma,psum(ng[1],v0[1]))]
    v0 = copy.deepcopy(v1)

    print 'v0:'
    q1=printpol(v0[0])
    print 'v1:'
    q2=printpol(v0[1])

    fobj = open(entry + '1.txt', 'a')
    fobj.write(q1)
    fobj.close()

    fobj = open(entry + '2.txt', 'a')
    fobj.write(q2)
    fobj.close()

    return v0

def fdb(v0, entry):
    A = Db(v0)
    ng = [polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[0]),polmult(psum(up, psum(mp(v0[0]), mp(v0[1]))),A[1])]
    v1 = [polmult(uma,psum(ng[0],v0[0])),polmult(uma,psum(ng[1],v0[1]))]
    v0 = copy.deepcopy(v1)

    print 'v0:'
    q1=printpol(v0[0])
    print 'v1:'
    q2=printpol(v0[1])

    fobj = open(entry + '1.txt', 'a')
    fobj.write(q1)
    fobj.close()

    fobj = open(entry + '2.txt', 'a')
    fobj.write(q2)
    fobj.close()

    return v0

def kill(v0):
    v1 = [polmult(uma,v0[0]),polmult(uma,v0[1])]
    v0 = copy.deepcopy(v1)

    return v0

def fraction(v0):
    print 'M1'
    print 'primeiro polinomio:'
    v0 = fdab(v0, 'polynomialA')

    v0 = kill(v0)
    v0 = kill(v0)
    
    print 'M2'
    print 'segundo polinomio:'
    v0 = fdb(v0, 'polynomialB')

    
    print 'M3'
    print 'terceiro polinomio:'
    v0 = fda(v0,'polynomialC')
    

    v0 = kill(v0)

    print 'M4'
    print 'quarto polinomio:'
    v0 = fdb(v0, 'polynomialD')

    v0 = kill(v0)

    print 'M5'
    print 'terceiro polinomio:'
    v0 = fda(v0, 'polynomialE')
    

    print 'M6'
    print 'quarto polinomio:'
    v0 = fdb(v0, 'polynomialF')


    v0 = kill(v0)
    v0 = kill(v0)

    print 'polinomio final:'
    print 'v0:'
    q1 = printpol(v0[0])
    print 'v1:'
    q2 = printpol(v0[1])

    fobj = open('polynomialFINAL1.txt', 'a')
    fobj.write(q1)
    fobj.close()

    fobj = open('polynomialFiNAL2.txt', 'a')
    fobj.write(q2)
    fobj.close()
    
    vee = psum(up, psum(mp(v0[0]), mp(v0[1])))
    q3 = printpol(vee)

    fobj = open('vFiNAL2.txt', 'a')
    fobj.write(q3)
    fobj.close()


fraction([xis,umxmv])

    
tb = time.time()
print 'tempo de execucao: ' + str(tb-ta)



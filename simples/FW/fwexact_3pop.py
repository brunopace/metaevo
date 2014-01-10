import matplotlib.pyplot as plt
import numpy
import math



def pa(N, Na, Nb, fa,  fb, fc):
    return float(Na)*fa/(Na*fa + Nb*fb + (N-Na-Nb)*fc)

def pb(N, Na, Nb, fa,  fb, fc):
    return float(Nb)*fb/(Na*fa + Nb*fb + (N-Na-Nb)*fc)


def binomial(n,k):
   """Compute n factorial by a direct multiplicative method."""
   if k > n-k:
       k = n-k  # Use symmetry of Pascal's triangle
   accum = 1
   for i in xrange(1,k+1):
      accum *= (n - (k - i))
      accum /= i
   return accum

def pkl(N, k, l, pa, pb):
    return binomial(N, k)*binomial(N-k, l)*math.pow(pa,k)*math.pow(pb,l)*math.pow((1-pa-pb),(N-k-l))

def expected(N, dist):
    soma = [0, 0]
    for k in xrange(N + 1):
        for l in range(N - k + 1):
            soma[0] += k*dist[k][l]
            soma[1] += l*dist[k][l]
            
    return (soma[0],soma[1])

def drawhist(menMeans):

    N = len(menMeans)

    ind = numpy.arange(N)
    
    width = 1.0

    plt.clf()

    plt.ylabel('Probability')
    plt.xlabel('k')
    plt.title('Testando')
    plt.xlim(0.0,N)
    plt.ylim(0.0,1.0)
    plt.bar(ind, menMeans, width)
    plt.draw()
    plt.show()



N = 31
Na = [1,15]
f = [15, 10, 5]



pkls = [[0 for y in xrange(N+1-x)] for x in xrange(N+1)]
pkls[Na[0]][Na[1]] = 1
pklst = [[0 for y in xrange(N+1-x)] for x in xrange(N+1)]
expect = [(Na[0], Na[1], N-Na[0]-Na[1])] 

#drawhist(pks)
pa = [[pa(N, a, b, f[0], f[1], f[2]) for b in xrange(N + 1 - a)] for a in xrange(N+1)]
pb = [[pb(N, a, b, f[0], f[1], f[2]) for b in xrange(N + 1 - a)] for a in xrange(N+1)]


for t in range(30):
    print 't = ' + str(t)
    for na in xrange(N+1):
        for nb in xrange(N+1-na):
            for k in xrange(N+1):
                for l in xrange(N+1-k):
                    #print 'k = ' + str(k)
                    #print 'l = ' + str(l)
                    #print 'pa[na][nb] = ' + str(pa[na][nb])
                    #print 'pb[na][nb] = ' + str(pb[na][nb])
                    #print ' = ' + str()
                    #print ' = ' + str()
                    pklst[k][l] += pkls[na][nb]*pkl(N, k, l, pa[na][nb], pb[na][nb])
    #drawhist(pkst)
    pkls = pklst
    pklst = [[0 for x in xrange(N+1)] for y in xrange(N+1)]
    expect.append(expected(N, pkls))

plt.plot(range(len(expect)), [op[0] for op in expect], range(len(expect)), [op[1] for op in expect], range(len(expect)), [N - op[0] - op[1] for op in expect])
plt.draw()
plt.show()




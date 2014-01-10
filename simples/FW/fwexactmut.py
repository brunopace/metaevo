import matplotlib.pyplot as plt
import numpy
import math


plt.ion()

def p(N, Na, fa,  fb):
    return float(Na)*fa/(Na*fa + (N-Na)*fb)

def binomial(n,k):
   """Compute n factorial by a direct multiplicative method."""
   if k > n-k:
       k = n-k  # Use symmetry of Pascal's triangle
   accum = 1
   for i in range(1,k+1):
      accum *= (n - (k - i))
      accum /= i
   return accum

def pk(N, k, p):
    return binomial(N, k)*math.pow(p,k)*math.pow((1-p),(N-k))

def expected(N, dist):
    soma = 0
    area = 0
    for k in range(N + 1):
        soma += k*dist[k]
        area += dist[k]
    return soma/area

def drawhist(menMeans, pot, H):

    N = len(menMeans)

    ind = numpy.arange(N)
    width = 1.0

    plt.clf()

    plt.ylabel('Probability and Energy/' + str(H))
    plt.xlabel('k')
    plt.title('Testando')
    plt.xlim(0.0,N)
    #plt.ylim(0.0,1.0)
    plt.bar(ind, menMeans, width)
    plt.plot(ind, pot, color = 'r')
    plt.draw()
    plt.pause(0.0001)

def multiplmv(pks, N, p, epsa, epsb):
    pkst = [0]*(N+1)
    for Na in range(N + 1):
        for k in range(N + 1):
            pkst[k] += pks[Na]*pk(N, k, p[Na])
    pks = pkst
    pkst = [0]*(N+1)
    for Na in range(N + 1):
        for k in range(N + 1):
            for a in [j for j in range(Na + 1) if j <= k and j  >= k + Na - N]:
                pkst[k] += pks[Na]*binomial(Na,a)*binomial(N-Na,k-a)*math.pow((1-epsa), a)*math.pow(epsa, Na-a)*math.pow((1-epsb), N-Na-k+a)*math.pow(epsb, k-a)           
                
    return pkst
    
def potential(steps, N, p, epsa, epsb):
    k = range(N+1)
    accel = [0]*(N+1)
    potential = [0]*(N+1)
    delta1 = [0]*(N+1)
    minp = 0
    maxp = 0

    for i in range(N+1):
        print 'i = ' + str(i)
        f = [0]*(N+1)
        f[i] = 1
        for s in range(steps):
            f = multiplmv(f, N, p, epsa, epsb)
        delta1[i] = expected(N, f) - i
        accel[i] = delta1[i]
        
    for i in range(N):
        potential[i+1] = potential[i] - accel[i+1]
        if potential[i+1] < minp:
            minp = potential[i+1]
        if potential[i+1] > maxp:
            maxp = potential[i+1]

    if minp != 0:
        for i in range(N+1):
            potential[i] = float(potential[i])/abs(minp) + 1
    else:
        for i in range(N+1):
            potential[i] = float(potential[i])/abs(maxp)



    potential.append(abs(minp))

    print potential
    print len(potential)    
    return potential
    #plt.plot(k, potential)
    #plt.draw()
    #plt.pause(1)

def potentialinf(N, p, epsa, epsb):
    k = range(N+1)
    accel = [0]*(N+1)
    potential = [0]*(N+1)
    delta1 = [0]*(N+1)
    minp = 0
    maxp = 0

    inf = 1

    f = [0]*(N+1)
    f[5*N/6] = 1

    for t in range(inf):
        print 'tpot = ' + str(t)
        f = multiplmv(f, N, p, epsa, epsb)
        
    for i in range(N+1):
        delta1[i] = expected(N, f) - i
        accel[i] = delta1[i]
        
    for i in range(N):
        potential[i+1] = potential[i] - accel[i+1]
        if potential[i+1] < minp:
            minp = potential[i+1]
        if potential[i+1] > maxp:
            maxp = potential[i+1]

    if minp != 0:
        for i in range(N+1):
            potential[i] = float(potential[i])/abs(minp) + 1
    else:
        for i in range(N+1):
            potential[i] = float(potential[i])/abs(maxp)

    potential.append(abs(minp))

    print potential
    print len(potential)    
    return potential
    #plt.plot(k, potential)
    #plt.draw()
    #plt.pause(1)



N = 10
Na = 0
fa = 3
fb = 2
epsa = 0.01
epsb = 0.01
years = 120



pks = [0]*(N+1)
pks[Na] = 1
#pkst = [0]*(N+1)
expect = [Na]



p = [p(N, n, fa, fb) for n in range(N + 1)]


pot = potentialinf(N, p, epsa, epsb)
H = pot.pop()
drawhist(pks, pot, H)
drawhist(pks, pot, H)


for t in range(years):
    print 't = ' + str(t)
#    for Na in range(N + 1):
#        for k in range(N + 1):
#            pkst[k] += pks[Na]*pk(N, k, p[Na])
#    pks = pkst
#    pkst = [0]*(N+1)
#    for Na in range(N + 1):
#        for k in range(N + 1):
#            for a in [j for j in range(Na + 1) if j <= k and j  >= k + Na - N]:
#                pkst[k] += pks[Na]*binomial(Na,a)*binomial(N-Na,k-a)*math.pow((1-epsa), a)*math.pow(epsa, Na-a)*math.pow((1-epsb), N-Na-k+a)*math.pow(epsb, k-a)           
                
#    pks = pkst
#    pkst = [0]*(N+1)
    pks = multiplmv(pks, N, p, epsa, epsb)
        
    drawhist(pks, pot, H)
    
    expect.append(expected(N, pks))
    

plt.ioff()
plt.show()

plt.plot(range(len(expect)), expect, range(len(expect)), [N - expect[t] for t in range(len(expect))])
plt.draw()
plt.show()


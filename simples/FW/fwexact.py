import matplotlib.pyplot as plt
import numpy
import math



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



N = 50
Na = 5
fa = 15
fb = 10



pks = [0]*(N+1)
pks[Na] = 1
pkst = [0]*(N+1)
expect = [Na]
extinct = 0
fixed = 0
text = [0]
tfix = [0]

#drawhist(pks)
p = [p(N, n, fa, fb) for n in range(N + 1)]

for t in range(100):
    print 't = ' + str(t)
    for Na in range(N + 1):
        for k in range(N + 1):
            pkst[k] += pks[Na]*pk(N, k, p[Na])
    #drawhist(pkst)
    pks = pkst
    pkst = [0]*(N+1)
    expect.append(expected(N, pks))
    text.append(pks[0] - extinct)
    tfix.append(pks[N] - fixed)
    extinct = pks[0]
    fixed = pks[N]
    

plt.plot(range(len(expect)), expect, range(len(expect)), [N - expect[t] for t in range(len(expect))])
plt.draw()
plt.show()

plt.plot(range(len(tfix)), tfix)
plt.title('Expected time  to fixation: '+ str(expected(len(tfix) - 1, tfix)))
plt.draw()
plt.show()


plt.plot(range(len(text)), text)
plt.title('Expected time  to extinction: '+ str(expected(len(text) - 1, text)))
plt.draw()
plt.show()

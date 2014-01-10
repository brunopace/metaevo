import math
import matplotlib.pyplot as plt


def pol(a,b,c,d,ee,f,g,h,i, x):
    return a+b*x+c*x**2+d*x**3+ee*x**4+f*x**5+g*x**6+h*x**7+i*x**8

def o(x,e):
    return (x*(2-5*e)+3*e)/(4-e+3*e*x-2*x)

def p(x, e):
    return (1-16*e)*x**8+(4*e)*x**7+(-4+54*e)*x**6+(-12*e)*x**5+(4-47*e)*x**4+(8*e)*x**3+(6*e)*x**2+e

def q(x,e):
    return (1-16*e+112*e**2)*x**8+(4*e-56*e**2)*x**7+(-4+54*e-306*e**2)*x**6+(-12*e+138*e**2)*x**5+(4-47*e+217*e**2)*x**4+(8*e-78*e**2)*x**3+(6*e-37*e**2)*x**2+(6*e**2)*x+(e+2*e**2)

def r(x,e):
    return (1-16*e+112*e**2-448*e**3)*x**8+(4*e-56*e**2+336*e**3)*x**7+(-4+54*e-306*e**2+928*e**3)*x**6+(-12*e+138*e**2-656*e**3)*x**5+(4-47*e+217*e**2-478*e**3)*x**4+(8*e-78*e**2+298*e**3)*x**3+(6*e-37*e**2+73*e**3)*x**2+(6*e**2-29*e**3)*x+(e+2*e**2-6*e**3)

def z(x,e):
    return pol(1,-16,112,-448,1120,-1792,1792,-1024,256,e)*x**8+pol(0,4,-56,336,-1120,2240,-2688,1792,-512,e)*x**7+pol(-4,54,-306,928,-1560,1248,32,-768,384,e)*x**6+pol(0,-12,138,-656,1640,-2240,1504,-256,-128,e)*x**5+pol(4,-47,217,-478,425,152,-536,256,16,e)*x**4+pol(0,8,-78,298,-550,468,-104,-48,0,e)*x**3+pol(0,6,-37,73,-27,-64,52,0,0,e)*x**2+pol(0,0,6,-29,46,-24,0,0,0,e)*x+pol(0,1,2,-6,4,0,0,0,0,e)



e = 0.01375286  #transition approx 0.01375286
step = 0.01

tsteps = 10000

fo = []
fp = []
fq = []
fr = []
fz = []
ft = [1]


for x in range(int(1/step)+1):
   #fo.append(o(x*step, e))
   #fq.append(q(x*step, e))
   #fr.append(r(x*step, e))
   fz.append(z(x*step, e))


plt.plot([i*step for i in range(int(1/step)+1)], fz,[i*step for i in range(int(1/step)+1)],[i*step for i in range(int(1/step)+1)])
    #[i*step for i in range(int(1/step)+1)], fp,[i*step for i in range(int(1/step)+1)], fq,[i*step for i in range(int(1/step)+1)], fr, [i*step for i in range(int(1/step)+1)], fz, [i*step for i in range(int(1/step)+1)],  [i*step for i in range(int(1/step)+1)])
plt.show()

for t in range(tsteps):
    ft.append(z(ft[-1],e))

plt.plot(range(len(ft)), ft)
plt.show()
    
print 'attractor: x* = ' + str(ft[-1])

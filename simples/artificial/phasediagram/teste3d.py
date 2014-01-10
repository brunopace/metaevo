from pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pickle

alpha = 0.7
phi_ext = 2 * pi * 0.5

emax = 0.01
step = 0.00001

eps = [i*step for i in range(int(emax/step))]
alp = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.275, 0.03, 0.0325, 0.035, 0.0375, 0.04, 0.0425, 0.045, 0.475]

w = ['a0005.pkl','a00075.pkl','a001.pkl', 'a00125.pkl','a0015.pkl', 'a00175.pkl','a002.pkl','a00225.pkl','a0025.pkl', 'a00275.pkl','a003.pkl', 'a00325.pkl','a0035.pkl', 'a00375.pkl','a004.pkl','a00425.pkl','a0045.pkl','a00475.pkl']



LL = []

def flux_qubit_potential(phi_m, phi_p):
    return 2 + alpha - 2 * cos(phi_p)*cos(phi_m) - alpha * cos(phi_ext - 2*phi_p)

def criticalsize(a,e):
    return LL[a][e]


def unpick(filelist):
    for i in range(len(filelist)):
        pkl_file = open(filelist[i],'rb')
        au = pickle.load(pkl_file)
        pkl_file.close()
        LL.append(au)



#phi_m = linspace(0, 2*pi, 100)
#phi_p = linspace(0, 2*pi, 100)
#X,Y = meshgrid(phi_p, phi_m)
#Z = flux_qubit_potential(X, Y).T

unpick(w)

#phi_e = linspace(0,0.00998,int(emax/step))
phi_e = linspace(0.0,0.01,len(w))
phi_a = linspace(0.0025,0.045,len(w))
X,Y = meshgrid(phi_a,phi_e)
Z = zeros((len(alp), len(alp)))

for a in range(len(alp)):
    for e in range(len(alp)):
        Z[a][e] = criticalsize(a,e*111/2)

Z = Z.T

fig = plt.figure(figsize=(8,7))

ax = fig.add_subplot(1,1,1, projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
ax.view_init(15, 30)
fig.tight_layout()

##ax = fig.add_subplot(1, 1, 1, projection='3d')
##p = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
##cb = fig.colorbar(p, shrink=0.5)
##ax.view_init(70, 30)
##fig.tight_layout()

plt.show()

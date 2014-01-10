#!/usr/bin/env python
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


delta = 0.025
x = y = np.arange(0.0, 1.0, delta)
X, Y = np.meshgrid(x, y)
#Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
#Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
#Z = Z2-Z1  # difference of Gaussians

Z = np.empty(np.shape(X))

for i in range(np.shape(Z)[0]):
    for j in range(np.shape(Z)[1]):
        Z[j][i] = i-j

im = plt.imshow(Z, origin='lower', extent=[0,1,0,1],
                vmax=abs(Z).max(), vmin=-abs(Z).max())

plt.show()


#for i in range(int(1/h)):
#    for j in range(int(1/h)):
#        pass

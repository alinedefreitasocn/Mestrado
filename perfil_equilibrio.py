# -*- coding: utf-8 -*-
"""
Created on Wed May 23 12:11:47 2018

@author: aline
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integrate

x = np.arange(0, 2000, 1)
A = 0.0904
m = 0.49
h = pd.DataFrame(index=x, data=np.zeros(x.size), columns=['Equilibrium Beach Profile'])

for i in x:
    h['Equilibrium Beach Profile'][i] = A*i**m
hnegativo = h['Equilibrium Beach Profile']*-1
hnegativo.plot(color='DarkBlue')
plt.ylabel('Water Depth (m)')
plt.xlabel('Horizontal Distance (m)')

plt.fill_between(h.index, hnegativo, y2=0, color='DarkBlue', alpha=0.3)
plt.fill_between(h.index, hnegativo.min(), y2=hnegativo, color='goldenrod', alpha=0.3)


integral = integrate.quad(lambda x: A*x**m, 0, 2000)
plt.annotate(str(round(integral[0]))+ 'm**2', (1000, -1))
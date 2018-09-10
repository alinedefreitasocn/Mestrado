# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:40:24 2017

@author: aline
"""


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xray
from mpl_toolkits.basemap import Basemap as bm
from scipy.interpolate import griddata
import utm
from matplotlib import delaunay
import scipy
import matplotlib

filename = 'batimetria_salinas.bln'
pathfile = 'D:\\GoogleDrive\\Mestrado\\DISSERTACAO\\ANALISE_DADOS\\Batimetria\\' + filename

bat = pd.read_table(pathfile, sep='\s+', names=['xx', 'yy', 'zz'], header=0, skiprows=1)
bat.zz = bat.zz * -1
bat[:5]

plt.plot(bat.xx, bat.yy, '.')
plt.grid()
plt.savefig(pathfile + '_pontoUTM.png')


# passando as variaveis para array. Quando usamos o df.values transforma em um array
lon = bat.xx.values            # array like
lat = bat.yy.values            # array like
topo = bat.zz.values           # array like

# convertendo de utm para graus decimais
a = [utm.to_latlon(lon[i], lat[i], 23, 'K') for i in range(len(lat))]

lat, lon = np.array(a).T

plt.figure()
plt.scatter(lon, lat, c=topo, s=5)   # c = batimetria, s = tamanho dos pontos
plt.savefig(pathfile[:-4] + '_latlon.png')

# pega a lat e lon min e maximos e cria um vetor com valores igualmente espacados de 50 em 50
xg = np.linspace(lon.min(), lon.max(), 50)
yg = np.linspace(lat.min(), lat.max(), 50)

xg, yg = np.meshgrid(xg, yg)

plt.plot(xg, yg, 'k.', alpha=0.1)



topog = griddata(np.array([lon, lat]).T, topo, (xg, yg), method='linear')
# interpolacao no metodo linear
# os primeiros argumentos sao os valores medidos (lat, lon e topog)
# (xg, yg) sao os valores que vao ser interpolados


plt.figure()

plt.contourf(xg, yg, topog, 50)
plt.plot(lon, lat, 'k.', markersize=1, alpha=0.6)
plt.colorbar()

# aplicando a mascara no continente
z = np.ma.masked_where(topog >= 0, topog)

# figura com a mascara do continente
plt.figure()
plt.contourf(xg, yg, z, 50)
plt.colorbar()

m = bm(projection='cyl', llcrnrlat=lat.min()-.01,
            urcrnrlat=lat.max()+.01,
            llcrnrlon=lon.min()-.01, urcrnrlon=lon.max()+.01,
            lat_ts=10, resolution='f')

# m eh uma funcao basemap e cria duas variaveis (mlon e mlat)
mlon, mlat = m(lon, lat)

plt.figure(facecolor='w', figsize=(12, 12))
m.coastpolygontypes
m.plot(mlon, mlat, '.y', markersize=1)
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-5, 5, .1), color='gray',
                dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-60, 10, .1), color='gray',
                dashes=[1, 1], labels=[0, 0, 1, 1])





# INTERPOLACAO
#delaunay.Triangulation(lon, lat) esta sendo depreciada. usar matplotlib.tri.Triangulation
tri = matplotlib.tri.Triangulation(lon, lat)

# interp = tri.linear_interpolator(topo)
interp = scipy.interpolate.LinearNDInterpolator(zip(lon, lat), topo, fill_value=0)


xg = np.linspace(lon.min(), lon.max(), 60)
yg = np.linspace(lat.min(), lat.max(), 80)
xg, yg = np.meshgrid(xg, yg)

batI = interp(xg, yg)

mxg, myg = m(xg, yg)

plt.figure(facecolor='w', figsize=(12, 10))
ax = plt.gca()
m.fillcontinents(color='coral', lake_color='aqua')
m.contourf(mxg, myg, batI, 500, levels=np.arange(-30,0,0.5))
m.colorbar()
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-25, -20, 0.1), color='gray',
                dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-44, -42, 0.1), color='gray',
                dashes=[1, 1], labels=[0, 0, 1, 1])
plt.savefig(pathfile[:-4] + '_contour.png')

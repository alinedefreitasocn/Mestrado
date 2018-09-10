# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 15:28:21 2017

@author: aline

Criando uma rosa de ondas para os dados do modelo
na regiao de Salinopolis
"""

from netCDF4 import Dataset
import wx
import numpy as np

import matplotlib as mpl
from matplotlib import mlab
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.dates as mdates

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
import netCDF4
import seaborn as sns
from windrose import WindroseAxes
import os
import xray
import cartopy.crs as ccrs


# A quick way to create new windrose axes #,radialaxis='%'
def new_axes():
    fig = plt.figure(figsize=(13, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

# ...and adjust the legend box
def set_legend(ax):
    l = ax.legend(borderaxespad=-0.10, bbox_to_anchor=[-0.1, 0.5],
                  loc='centerleft', title="Hs (m)")
    plt.setp(l.get_texts(), fontsize=20)

def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        direc = dialog.GetDirectory()
        # f = dialog.GetFilename()
    else:
        path = None
    dialog.Destroy()
    return path, direc

# funcao espectro do Henrique
def espec1(x, nfft, fs):
    # calculando o espectro
    sp = mlab.psd(x,                              # time series
                 NFFT=nfft,                       # length window (averages)
                 Fs= fs,                          # remove trend ( remove a mare da serie de onda, p.ex.)
                 detrend=mlab.detrend_mean,       # hanning window
                 window=mlab.window_hanning,      # overlap for welch spectrum
                 noverlap=nfft/2)
    f, sp = sp[1][1:], sp[0][1:]

    # graus de liberdade
    gl = len(x)/nfft * 2

    # intervalo de confianca 95%
    ici = sp * gl / 26.12
    ics = sp * gl / 5.63

    aa = np.array([f, sp, ici, ics]).T           # .T faz a transporta do array

    return aa

esquema_cores3 = sns.cubehelix_palette(8, start=.5, rot=-.6)
"####################################################"
"#                                                  #"
"#                    LEITURA                       #"
"#                                                  #"
"####################################################"
print('Escolha arquivo do ETOPO')
etopodata = Dataset(get_path('ETOPO*.nc')[0])
print('Escolha arquivo NetCDF com dados de onda')
filename, pathname = get_path('*.nc')
reanalise = Dataset(filename, mode = 'r')

dim = reanalise.dimensions


#pathname = 'D:\\GoogleDrive\\Mestrado\\DISSERTACAO\\ANALISE_DADOS\\Ondas\\'
"####################################################"
"#                                                  #"
"#       CARREGANDO VARIAVEIS DOS ARQUIVOS          #"
"#                                                  #"
"####################################################"
lat = reanalise.variables['latitude'][:]
lon = reanalise.variables['longitude'][:]
tempo = reanalise.variables['time'][:]
t_cal = reanalise.variables['time'].calendar
t_unit = reanalise.variables['time'].units


datahora = netCDF4.num2date(tempo,
                            units=t_unit,
                            calendar=t_cal)

# Variaveis terao shape [Tempo, Lat, Lon]
# v10 = reanalise.variables['v10']
# u10 = reanalise.variables['u10'][:]
wave = reanalise.variables['swh'][:]
wavedir = reanalise.variables['mwd'][:]
waveT = reanalise.variables['mwp'][:]

# ETOPO
X, Y = np.meshgrid(etopodata.variables['x'][:], etopodata.variables['y'][:])
bathy = etopodata.variables['z'][:]


"####################################################"
"#                                                  #"
"#                    CALCULOS                      #"
"#                                                  #"
"####################################################"
# media ao longo do tempo
media = np.nanmean(wave, axis=0)
Tmedio = np.nanmean(waveT, axis=0)
dirmedia = np.nanmean(wavedir, axis=0)

"####################################################"
"#                                                  #"
"#         LOCALIZANDO PONTOS DE SAIDA              #"
"#              DO MODELO NO MAPA                   #"
"#                                                  #"
"####################################################"
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#m = Basemap(width=1500000, height=750000,
#            resolution='l', projection='stere',\
#            lat_ts=40, lat_0=lat.mean(), lon_0=lon.mean())

m = Basemap(projection='cyl', llcrnrlat=lat.min()-.5,
            urcrnrlat=lat.max()+.5,
            llcrnrlon=lon.min()-2, urcrnrlon=lon.max()+2,
            lat_ts=10, resolution='l')
# TRANSFORMANDO VARIAVEIS LAT LON EM VARIAVEIS 2D
lons, lats = np.meshgrid(lon, lat)
# TRANSFORMANDO PARA O BASEMAP
xi, yi = m(lons, lats)

# Plotando batimetria
levs=[-1000, -500, -200, -100]

c = m.contour(X,Y,bathy,levs,colors=esquema_cores3,latlon=True)
m.plot(xi, yi, '*y')

m.colorbar()
# FIM

# clabel= plt.clabel(c,fontsize=15,fmt='%.im')

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 1.), labels=[1, 0, 0, 0], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')
m.drawmeridians(np.arange(-180., 181., 1.), labels=[0, 0, 0, 1], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents(color='0.85')

xx = input(u'Posicao x:   ')
yy = input(u'Posicao y:   ')
m.plot(xi[yy,xx], yi[yy,xx], 'or')
# ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
ax.annotate('lat: %.2f, lon: %.2f' % (lats[yy,xx], lons[yy,xx]-360),
            xy=(xi[yy,xx], yi[yy,xx]))
plt.savefig(pathname + 'loc_onda_%.2f_%.2f.png' % (lat[yy], lon[xx]-360))

# profundidade do ponto de onda
# NAO ESTA FUNCIONANDO AINDA!!!
#y = etopodata.variables['y'][:]
#x = etopodata.variables['x'][:]

#def find_nearest(array,value):
#    idx = (np.abs(array-value)).argmin()
#    return array[idx], idx
#latz, latidx = find_nearest(x, xx)
#lonz, lonidx = find_nearest(y, yy)

#zz = bathy[lonidx, latidx]

"####################################################"
"#                                                  #"
"#         SERIE TEMPORAL DE HS, TP E DIR           #"
"#              NO PONTO ESCOLHIDO                  #"
"#                                                  #"
"####################################################"
plt.show(block = False)

fig, [ax1, ax2, ax3] = plt.subplots(3,1)

ax1.plot(wavedir[4988:6447,yy,xx], 'oc')
ax1.set_xticks([])
#ax1.set_xlim(0, 1464)
ax1.set_ylabel(u'Direção de onda [º]')
ax2.plot(waveT[4988:6447,yy,xx], 'orange')
ax2.set_xticks([])
#ax2.set_xlim(0, 1464)
ax2.set_ylabel(u'Período de onda [s]')
ax3.plot(wave[4988:6447,yy,xx], 'g')
#ax3.set_xlim(0, 1464)
ax3.set_ylabel('Altura de onda [s]')
ax3.set_xlabel('Tempo')
ax1.set_title(u'Série temporal de onda no ponto lat: %s, lon: %s'
    %(str(lat[yy]), str(lon[xx]-360)))


ax3.set_xticks(np.arange(0, 1459,360))
ax3.set_xticklabels(datahora[4988::360],
                    size = 'small',
                    rotation = 0)
plt.savefig(pathname + 'serie_onda_%.2f_%.2f.png' % (lat[yy], lon[xx]-360))


"*************************************************************"
"*                                                           *"
"*                    ROSA DE ONDAS                          *"
"*                                                           *"
"*************************************************************"

"""
ROSA DE ONDAS PARA TODA A SERIE

"""

mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
ax = new_axes()
#ax.autoscale(enable=False, tight=False)
ax.bar(wavedir[:,yy,xx], wave[:,yy,xx], normed=True, opening=0.8,
       edgecolor='white')
#ax.set_rlim(0,82)
#plt.suptitle(u'Hs por direção')
set_legend(ax)
# plt.title('Vel - camada 1', y=1.08,fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
#manager.resize(*manager.window.maxsize())
plt.savefig(pathname + '\\waverose_%.2f_%.2f.png' % (lat[yy], lon[xx]-360),
            format='png',
            dpi=1200)


"####################################################"
"#                                                  #"
"#                    PLOT MEDIAS HS                #"
"#                                                  #"
"####################################################"
plt.ion()
plt.figure()
m = Basemap(width=1500000,height=750000,
            resolution='l',projection='stere',
            lat_ts=40, lat_0=lat.mean(), lon_0=lon.mean())

lons, lats = np.meshgrid(lon, lat)
xi, yi = m(lons, lats)
plt.plot(lons-360, lats, '*r')

# Plotando etopo
levs=[-100, -80, -60, -40, -20, -10];

c = m.contour(X,Y,bathy,levs,colors='k',latlon=True)
m.plot(xi, yi, '*r')
# FIM

clabel= plt.clabel(c,fontsize=15,fmt='%.im')

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(media))
#plt.plot(lon[1]-360, lat[1])

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents(color='0.85')

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('m')

# Add Title
plt.title(u'Altura média de onda')


"####################################################"
"#                                                  #"
"#                    ESPECTROS                     #"
"#                                                  #"
"####################################################"
delta = pd.Timedelta(xr.time.data[2]-xr.time.data[1])
for i in range(len(xr.latitude)):
for i in range(1):
    for j in range(len(xr.longitude)):
            aa = espec1(x=xr.swh.data[:,i,j],
                        nfft=len(xr.swh[:,i,j])/2,
                        fs=1./delta.seconds)
            pl.figure(figsize=[8,4])
            pl.plot(aa[:,0], aa[:,1])
            pl.grid()
            pl.title(u'Latitude %.2f  Longitude %.2f' % (xr.latitude.data[i],
                                                        xr.longitude.data[j]))
            pl.show()


#for nfft1 in [len(xr.swh[:,i,j]),
#              len(xr.swh[:,i,j])/2,
#              len(xr.swh[:,i,j])/4,
#              len(xr.swh[:,i,j])/6]:
"####################################################"
"#                                                  #"
"#          ANOTANDO ALTURA NO MAPA                 #"
"#                                                  #"
"####################################################"


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

c = m.contour(X,Y,bathy,levs,colors=esquema_cores3,latlon=True)
m.plot(xi, yi, '*y')

m.colorbar()
m.drawparallels(np.arange(-80., 81., 1.), labels=[1, 0, 0, 0], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')
m.drawmeridians(np.arange(-180., 181., 1.), labels=[0, 0, 0, 1], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents(color='0.85')

for i in range(len(lat)):
    for j in range(len(lon)):
        ax.annotate('%.2f' % dirmedia[i,j],
                    xy=(xi[i,j], yi[i,j]), size=9)
plt.title(u'Direção média de onda (graus)')
plt.savefig(pathname + 'loc_onda_%.2f_%.2f.png' % (lat[yy], lon[xx]-360))

#############
#############

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

c = m.contour(X,Y,bathy,levs,colors=esquema_cores3,latlon=True)
m.plot(xi, yi, '*y')

m.colorbar()
m.drawparallels(np.arange(-80., 81., 1.), labels=[1, 0, 0, 0], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')
m.drawmeridians(np.arange(-180., 181., 1.), labels=[0, 0, 0, 1], fontsize=10,
                alpha=0.6, linewidth=0.5, color='grey')

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents(color='0.85')

for i in range(len(lat)):
    for j in range(len(lon)):
        ax.annotate('%.2f' % media[i,j],
                    xy=(xi[i,j], yi[i,j]), size=9)
plt.title(u'Altura média de onda (m)')


"####################################################"
"#                                                  #"
"#            BRINCANDO COM XRRAY                   #"
"#                                                  #"
"####################################################"
xr = xray.open_dataset(filename)

clim = {}
clim['month'] = xr.groupby('time.month').mean('time')
# como eh uma variavel 3-D, tem que definir em qual eixo ele vai calcular a media
clim['season'] = xr.groupby('time.season').mean('time')
clim['year'] = xr.groupby('time.year').mean('time')


swh = clim['month'].swh

g_simple = swh.plot(transform=ccrs.PlateCarree(),
                    x='longitude',
                    y='latitude',
                    col='month',
                    col_wrap=6,
                    subplot_kws={'projection': ccrs.PlateCarree()})

for ax in g_simple.axes.flat:
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.set_extent([xr.longitude.data.min()-360,
                    xr.longitude.data.max()-360,
                    xr.latitude.data.min(),
                    xr.latitude.data.max()])
    ax.set_aspect('equal', 'box-forced')

"*********************************************************************"
"                                                                     "
"""                         EXTRA SOLTO                             """
"                                                                     "
"*********************************************************************"



serieonda = wave[:, yy, xx]
# serieonda = serieonda[~serieonda.mask]
dfserieonda = pd.DataFrame(data = serieonda, index=datahora)


media = np.nanmean(wave[:,yy,xx])
linha_media = np.ones(len(wave[:,yy,xx]))
linha_media = linha_media*media
stdwave = np.std(wave[:,yy,xx])
linha_media2 = linha_media + stdwave


bigwave = dfserieonda[dfserieonda >= (media+stdwave)]
bigwave = bigwave.dropna(axis=0)  # dez a abril
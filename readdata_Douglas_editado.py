
# coding: utf-8

# # Dados Douglas- Batimetria XYZ
# - Equipamento:
# - Extensão: XYZ (texto)
# - Descrição:
#   - Lat, Lon, Prof
#   - 
# - Infos:
#   - Baia de Sepetiba
#   - Instalar biblio UTM: conda install -c conda-forge utm

# In[1]:

# import libraries

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xray
from mpl_toolkits.basemap import Basemap as bm
from scipy.interpolate import griddata


# In[2]:

import utm


# In[4]:

# lista diretorios

pathname = os.environ['USERPROFILE'] + '\\Dropbox\\PythonScriptsTemp\\CursoPythonHenrique\\data\\Douglas'
filename = 'BATSEP.XYZ'
pathfile = pathname + '\\' + filename
pathfile


# In[7]:

# carrega arquivo

bat = pd.read_table(pathfile, sep='\s+', names=['xx', 'yy', 'zz'], header=None)
bat[:5]


# In[9]:

get_ipython().magic(u'matplotlib inline')
plt.close('all')

plt.plot(bat.xx, bat.yy, '.')
# tem um problema nos dados. um ponto esta muito distante dos outros
# possivelmente um erro de digitacao
#plt.show()


# In[16]:

# escolhe os dados dentro de uma janela de lat lon

plt.close('all')

# selecionou os valores pelo zoom da imagem anterior
loni, lone = 606000, 650000
lati, late = 7400000, 7500000

# pode dar mais de uma condicao ao mesmo tempo
bat = bat.loc[(bat.xx > loni) & (bat.xx < lone) &                (bat.yy > lati) & (bat.yy < late)]

plt.plot(bat.xx, bat.yy, '.')
plt.grid()


# In[43]:

#interpolacao e plotagem

# passando as variaveis para array. Quando usamos o df.values transforma em um array
lon = bat.xx.values            # array like
lat = bat.yy.values            # array like
topo = bat.zz.values           # array like

# convertendo de utm para graus decimais
a = [utm.to_latlon(lon[i], lat[i], 23, 'K') for i in range(len(lat))]

lat, lon = np.array(a).T

plt.figure()
plt.scatter(lon, lat, c=topo, s=5)   # c = batimetria, s = tamanho dos pontos


# In[44]:

a
np.array(a)
np.array(a).T


# In[45]:

# pega a lat e lon min e maximos e cria um vetor com valores igualmente espacados de 50 em 50
xg = np.linspace(lon.min(), lon.max(), 50)
yg = np.linspace(lat.min(), lat.max(), 50)

#xg, yg = np.meshgrid(xg, yg)


# In[46]:

xg


# In[47]:

xg, yg = np.meshgrid(xg, yg)


# In[48]:

xg


# In[39]:

plt.plot(xg, yg, 'k.', alpha=0.1)


# In[49]:

#
topog = griddata(np.array([lon, lat]).T, topo, (xg, yg), method='linear')
# interpolacao no metodo linear
# os primeiros argumentos sao os valores medidos (lat, lon e topog)
# (xg, yg) sao os valores que vao ser interpolados


plt.figure()

plt.contourf(xg, yg, topog, 50)
plt.plot(lon, lat, 'k.', markersize=1, alpha=0.6)
plt.colorbar()


# In[50]:

# aplicando a mascara no continente
z = np.ma.masked_where(topog > -3, topog)

# figura com a mascara do continente
plt.figure()
plt.contourf(xg, yg, z, 50)
plt.colorbar()


# In[56]:

# entrar no site do basemap!!
m = bm(projection='cyl', llcrnrlat=lat.min()-.1, 
            urcrnrlat=lat.max()+.1,
            llcrnrlon=lon.min()-.1, urcrnrlon=lon.max()+.1, 
            lat_ts=10, resolution='h')

# m eh uma funcao basemap e cria duas variaveis (mlon e mlat)
mlon, mlat = m(lon, lat)

plt.figure(facecolor='w', figsize=(12, 12))
m.coastpolygontypes
m.plot(mlon, mlat, '.y', markersize=1)
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-25, -10, 2), color='gray', 
                dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-60, 10, .3), color='gray', 
                dashes=[1, 1], labels=[0, 0, 1, 1])


# In[59]:

# plotagem com basemap

from matplotlib import delaunay
import scipy
import matplotlib

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
m.contourf(mxg, myg, batI, 500, levels=np.arange(-20,0,0.5))
m.colorbar()
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-25, -20, 0.1), color='gray', 
                dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-44, -42, 0.1), color='gray', 
                dashes=[1, 1], labels=[0, 0, 1, 1])

plt.savefig('mapa_bat.pdf')
plt.show()


# In[16]:

get_ipython().magic(u'matplotlib inline')
m = bm(projection='cyl', llcrnrlat=-5, 
            urcrnrlat=7,
            llcrnrlon=-50, urcrnrlon=-40, 
            lat_ts=10, resolution='h')
# m eh uma funcao basemap e cria duas variaveis (mlon e mlat)
#mlon, mlat = m(lon, lat)

plt.figure(facecolor='w', figsize=(12, 12))
m.drawcoastlines()
m.drawparallels(np.arange(-5, 7, 1), color='gray', 
                dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-50, -40, 1), color='gray', 
                dashes=[1, 1], labels=[0, 0, 1, 1])
plt.plot(-45.75, 6, '*r', markersize=12)


# In[21]:

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# read in etopo5 topography/bathymetry.
url = 'D:\\GoogleDrive\\Mestrado\\ETOPO2v2c_f4.nc'
etopodata = Dataset(url)

#topoin = etopodata.variables['ROSE'][:]
lons = etopodata.variables['ETOPO02_X'][:]
lats = etopodata.variables['ETOPO02_Y'][:]
# shift data so lons go from -180 to 180 instead of 20 to 380.
topoin,lons = shiftgrid(180.,topoin,lons,start=False)

llcrnrlat=-5 
urcrnrlat=7
llcrnrlon=-50
urcrnrlon=-40

# plot topography/bathymetry as an image.

# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,            rsphere=(6378137.00,6356752.3142),            resolution='f',area_thresh=1000.,projection='cyl')
# transform to nx x ny regularly spaced 5km native projection grid
nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map with imshow.
im = m.imshow(topodat,cm.GMT_haxby)
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# draw parallels and meridians.
# label on left and bottom of map.
parallels = np.arange(0.,80,20.)
m.drawparallels(parallels,labels=[1,0,0,1])
meridians = np.arange(10.,360.,30.)
m.drawmeridians(meridians,labels=[1,0,0,1])
# add colorbar
cb = m.colorbar(im,"right", size="5%", pad='2%')
ax.set_title('ETOPO5 Topography - Lambert Conformal Conic')
plt.show()


# In[ ]:




# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:15:49 2017
Leitura e analise dos dados meteorologicos de Salinopolis
@author: Aline
"""
import pandas as pd
import numpy as np
import wx
from pandas import Series, DataFrame, Panel
import datetime
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib as mpl
#import plotly.plotly as py
#import plotly.graph_objs as go

#A quick way to create new windrose axes...#,radialaxis='%'
def new_axes():
    fig = plt.figure(figsize=(13, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

#...and adjust the legend box
def set_legend(ax):
    l = ax.legend(borderaxespad=-0.10,bbox_to_anchor=[-0.1, 0.5],loc='centerleft',title="m/s")
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

filename, pathname = get_path('*.csv')

"Lendo arquivo do INMET"
met = pd.read_csv(filename, sep=';', header=0, na_values='////')

#met = pd.read_csv(filename, sep=';', header=0, na_values='////',
#                  parse_dates={'datetime':['Ano', 'Mes', 'Dia', 'Hora']},
#                              index_col='datetime')
#met.index = met.apply(lambda x: pd.to_datetime(x.index, format= "%Y%m%d%H"),
#                      axis=0)

"Transformando dia, mes, ano... em data_hora"
data_hora = []
for i in range(len(met)):
    data_hora.append(datetime.datetime(met.Ano[i], met.Mes[i],
                                       met.Dia[i], met.Hora[i]))
dates = pd.to_datetime(data_hora, utc=True) #tive que passas para dataframe de novo...


"""
Substituindo Index por data_hora
"""
met = met.drop(met.columns[[range(4)]], axis=1)
met = met.set_index(dates)

"""
Corrigindo o horario de GMT para local
"""
met.index = met.index.tz_convert('America/Fortaleza')
#met.index = met.index - 3:00:00

"""
separando periodos verao e inverno
"""
manha = met[met.index.hour<12]
tarde = met[met.index.hour>=12]

verao = met[met.index.month==12]
verao = verao.append(met[met.index.month<6])

"""
ANALISE HORARIA DE CHUVA E VENTO - VERAO E INVERNO
"""
chuvas_verao = []
media_verao = []
velvento_verao = []
for i in range(24):
    a = verao[verao.index.hour==i].chuva.sum()
    d = verao[verao.index.hour==i].chuva.mean()
    b = verao[verao.index.hour==i].vento_vel.mean()
    chuvas_verao.append(a)
    media_verao.append(d)
    velvento_verao.append(b)


Minv = np.arange(6,12,1)
inverno = pd.DataFrame()
for i in Minv:
    inverno = inverno.append(met[met.index.month==i])
   
chuvas_inv = []
media_inv = []
velvento_inv = []
for i in range(24):
    b = inverno[inverno.index.hour==i].chuva.sum()
    c = inverno[inverno.index.hour==i].chuva.mean()
    d = inverno[inverno.index.hour==i].vento_vel.mean()
    chuvas_inv.append(b)
    media_inv.append(c)
    velvento_inv.append(d)


# data to plot
n_groups = 24

 
# create plot
fig, ax = plt.subplots()   #precisa ser subplot pra funcionar o ax.twinx
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, media_inv, bar_width,
                 alpha=opacity,
                 color='c',
                 label='Inverno')
 
rects2 = plt.bar(index + bar_width, media_verao, bar_width,
                 alpha=opacity,
                 color='m',
                 label='Verao')
plt.ylabel('Chuva [mm]')
plt.legend()

ax2 = ax.twinx()
ax2.plot(velvento_inv, 'c')
ax2.plot(velvento_verao, 'm')
ax2.set_ylabel('velocidade do vento [m/s]')
ax2.tick_params('y')

#plt.plot(velvento_inv, 'c', label='Inverno')
#plt.plot(velvento_verao, 'm', label='verao')
 
plt.xlabel('Hora do dia')

plt.title('Distribuicao de chuva e vento ao longo do dia (media)')
plt.xticks(index + bar_width, ('0:00', ' ', '2:00', ' ',
                               '4:00', ' ', '6:00', ' ',
                               '8:00', ' ', '10:00', ' ',
                               '12:00', ' ', '14:00', ' ',
                               '16:00', ' ', '18:00', ' ',
                               '20:00', ' ', '22:00', ' '))

 
plt.tight_layout()
plt.show()  
plt.savefig(pathname + '\\chuva_vento_media.png')  
    
"""
Create wind speed and direction variables
"""
ws = met.vento_vel
wd = met.vento_dir


"""
ROSA DOS VENTOS PARA TODA A SERIE
"""
label_size = 14
mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
plt.title('Intensidade e direcao do vento - 2016')
set_legend(ax)
#plt.title('Vel - camada 1', y=1.08,fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
plt.savefig(pathname + '\windrose_inverno.png')

"""
ROSA DOS VENTOS PARA O PERIODO DE INVERNO
"""
label_size = 14
mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(inverno.vento_dir, inverno.vento_vel, normed=True, opening=0.8,
       edgecolor='white')
plt.title('Intensidade e direcao do vento - Inverno')
set_legend(ax)
#plt.title('Vel - camada 1', y=1.08,fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
plt.savefig(pathname + '\windrose_inverno.png')

"""
ROSA DOS VENTOS PARA O PERIODO DE VERAO
"""
label_size = 14
mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(verao.vento_dir, verao.vento_vel, normed=True, opening=0.8,
       edgecolor='white')
plt.title('Intensidade e direcao do vento - Verao')
set_legend(ax)
#plt.title('Vel - camada 1', y=1.08,fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
plt.savefig(pathname + '\windrose_verao.png')
#set_legend(ax)



# met[met.Temperatura_Inst>10]                   #so temperaturas instantaneas 
                                                #maiores que 10
# aonao['Diff'] = aonao['AO'] - aonao['NAO']     #adiciona nova coluna Diff ao 
                                                #DataFrame aonao
# janeiro = met['2017-01-01':'2017-01-31']      #slice by index                                               

met.Temperatura_Inst['2016-03-08':'2016-03-09'].plot(style = ' ') #plota serie sem linha

met.groupby(met.index.month).aggregate('mean')
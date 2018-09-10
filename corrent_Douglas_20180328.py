# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import pandas as pd
import wx
import matplotlib.pyplot as plt
# import csv
import numpy as np
# import datetime
# from matplotlib import mlab
from windrose import WindroseAxes
import os

plt.close('all')

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



filename, pathname = get_path('*.dat')
df = pd.read_table(filename, sep='\s+', header=None, usecols=[2, 3, 4, 14],
                   names=['X', 'Y', 'Z', 'Press'])

dataInicio = input('Entre com datahora de inicio da medicao entre plic (formato 11/22/2017 14:48:23) ')
dataFinal = input('Entre com datahora final da medicao (formato 11/22/2017 14:48:23) ')
frequencia = input('Entre com a frequencia de amostragem (ex. 250ms para 4Hz) ')

mes = dataInicio[0:2]
dia = dataInicio[3:5]
ano = dataInicio[6:10]
dataMedicao = ano+mes+dia

datahora = pd.date_range(start=dataInicio,
                         end=dataFinal, freq=frequencia)

#filename, pathname = get_path('*.csv')
#dg = pd.read_csv(filename, header=0)
datahora = datahora[0:-3]
df.index = datahora


"***************************************************************"
"                CONSISTENCIA DOS DADOS                         "
"***************************************************************"
# resampling para ter dados a cada segundo (tem 4 a cada segundo)
# aplico a media dos 4 valores
df = df.resample('S')
df = df.mean()

# PASSANDO x PARA OMENOR VALOR POSSÍVEL DIFERENTE DE ZERO PARA
# EVITAR ZERO DIVIDION
df.X[df.X == 0] = 0.0001  # avoiding 0 division

# ADICIONANDO OS 90 CM DE DISTANCIA DO EQUIPAMENTO NOS VALORES DE WL
waterLevel = df.Press + 0.9
waterLevel.plot(style='DarkBlue')
plt.ylabel('Water Level (m)')

# limpando os dados da parte em que o equipamento ficou emerso
df = df[df.Press>0.60]

# Calculando veloc e direc
df['veloc'] = np.sqrt((df.X**2)+(df.Y**2))
df['direc'] = np.arctan2(df.X,df.Y)
df['direc_graus'] = (df.direc*180)/np.pi

" CONSISTENCIA DOS DADOS DE VELOCIDADE  "
mediana = df.veloc.median()
velocidadeSTD = df.veloc.std()
plt.figure()
plt.hist(df.veloc)
velocidadesCortadas = df.veloc[df.veloc<=(mediana+(2*velocidadeSTD))]

plt.figure()
plt.plot(df.veloc, '.', color='DarkRed')
plt.title('Velocidade ADV ' + dataInicio)
velocidadesCortadas.plot(style='.', color='DarkBlue')

nivelBaixo = df.Press[df.veloc>(mediana+(2*velocidadeSTD))]
plt.figure()
nivelBaixo.plot(style='.', color='Orange')
plt.title('Water Level with hight current velocity')
plt.ylabel('Water Level (m)')
mediaNivelBaixo = nivelBaixo.mean()

df = df[df.veloc<=1]

plt.figure()
plt.plot(df.direc, '.')
plt.title(u'Direção radianos ' + dataInicio + ' - ' + dataFinal)
plt.figure()
plt.plot(df.direc_graus, '.')
plt.title(u'Direção graus ' + dataInicio + ' - ' + dataFinal)

# transformando as direcoes negativas em positivas
df.direc_graus[df.direc_graus<0] = df.direc_graus + 360
plt.figure()
df.direc_graus.plot(style='.')
plt.title(u'Direção graus ' + dataInicio + ' - ' + dataFinal)








df.direc_graus = df.direc_graus - 20.20 # declinacao magnetica
ws = df.veloc.values
wd = df.direc_graus.values


label_size = 16
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',
       bins=np.arange(0.1,1,0.1))
set_legend(ax)
plt.title(u'Correntes Maçarico - Salinas ', y=1.075,
           fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
plt.savefig(pathname + '\\corrente_' + dataMedicao + '.png',  transparent=True)


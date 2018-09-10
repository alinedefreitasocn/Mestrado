# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 20:57:25 2016

@author: andrea
"""

import pandas as pd
import wx
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
from matplotlib import mlab
from windrose import WindroseAxes


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
        #f = dialog.GetFilename()
    else:
        path = None
    dialog.Destroy()
    return path

#f = get_path('*.csv')
df = pd.read_csv(get_path('*.csv'), sep = ',', header = 0, na_values = 'NaN', na_filter = True)


# periodo 1
# 01/mar- 31/maio
""" ###################################################################
#
#       CRIANDO UMA LISTA DE VARIAVEIS PARA COLOCAR NO LOOP DEPOIS 
#
#####################################################################"""
lista_var = ['temp', 'umid', 'pto_orvalho', 'press', 'vvel', 'vdir',
             'radiacao', 'precipita']

""" ####################################################################
#
#  SELECIONANDO OS DADOS, REMOVENDO A MEDIA E SALVANDO COMO UMA NOVA 
#                     VARIAVEL 
#
#####################################################################"""
temp = df.temp_inst
umid = df.umid_inst
radiacao = df.radiacao

# velocidade e direcao do vento estao trocados
vvel = df.vento_direcao
vdir = df.vento_vel


dia = np.array([df.data[i][0:2] for i in range(len(df))], dtype = int)
mes = np.array([df.data[i][3:5] for i in range(len(df))], dtype = int)
ano = np.array([df.data[i][6:10] for i in range(len(df))], dtype = int)
hora = df.hora

datahora = [pd.datetime(ano[i], mes[i], dia[i], hora[i]) for i in range(len(df))]


""" ESPECTRO DE FREQUENCIAS """

#spec = mlab.psd(vvel[0], NFFT = len(vvel)/4, noverlap=len(vvel)/8)
#plt.plot(spec_vvel[1], spec_vvel[0])
#plt.title('Espectro vvel 8g.l')
#plt.xlabel('Frequencia (Hz)')
#plt.ylabel('Densidade espectral')
#plt.figure()
#spec = mlab.psd(vdir[0], NFFT = len(vdir)/4, noverlap=len(vdir)/8)
#plt.plot(spec_vdir[1], spec_vdir[0])
#plt.title('Espectro vdir 8g.l')
#plt.xlabel('Frequencia (Hz)')
#plt.ylabel('Densidade espectral')
#plt.figure()


#saida = pd.DataFrame({'Datahora': datahora[:], 'Temperatura':temp[:][0], 'Umidade':umid[:][0], 'Pto_Orvalho': pto_orvalho[:][0], 'Pressao': press[:][0], 'Vel_Vento': vvel[:][0], 'Dir_Vento': vdir[:][0], 'Radiacao':radiacao[:][0], 'Precipitacao':precipita[:][0]})
#saida.to_csv('saida_teste_inmet2.csv')
#df.index = datahora


" PLOTANDO AS FIGURAS DE SERIE TEMPORAL "

plt.figure()
plt.plot(datahora, temp)
plt.title('Temperatura')
plt.figure()
plt.plot(datahora, umid)
plt.title('Umidade')
plt.figure()
plt.plot(datahora, vvel)
plt.title('Velocidade do Vento')
plt.figure()
plt.plot(datahora, vdir)
plt.title('Direcao do Vento')


ws = vvel
wd = vdir
label_size = 14
mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size
ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',bins=np.arange(0,1.4,0.2))
set_legend(ax)
#plt.title('Vel - camada 1', y=1.08,fontsize=14,fontweight='bold')
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())


#ax = WindroseAxes.from_ax()
#ax.bar(vdir, vvel, normed=True, opening=0.8, edgecolor='white')
#ax.set_legend()
#ax.set_title('Intensidade e direcao do vento - Salinopolis, PA')

" FAZENDO A MEDIA DOS VALORES NAO NULOS DE CHUVA "
# indices = np.nonzero(df.precipitacao)
#
# prec_v = df.precipitacao.values
#
# prec = prec_v[indices]
#
# prec_v = df.precipitacao.values[indices]

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 20:44:20 2016

@author: Aline
"""

import pandas as pd
import wx
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
from matplotlib import mlab
from windrose import WindroseAxes
import os
import plotly.plotly as py
import plotly.graph_objs as go
import random
from collections import OrderedDict

plt.close('all')

Hs = []

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
arqs = os.listdir(pathname)

df = pd.read_csv(filename, sep=';', header = 0, na_values=[-999, 0])

estacoes = OrderedDict([('Atalaia2', 35), ('MCRC2', 36),
                        ('MCRC1', 38), ('Atalaia1', 39)])

beta_praias = {'Atalaia2': np.arange(0, 13, 5),
               'MCRC2': np.array([0,  5, 10, 15, 20, 25, 30, 35, 40,
                                  45, 50, 55, 60, 65, 70, 75, 335, 340,
                                  345, 350, 355]),
               'MCRC1': np.arange(300, 350, 5),
               'Atalaia1': np.arange(40, 90, 5)}

dironda = {'dn': 0*np.pi/180., 'dnne': 22.5*np.pi/180,
           'dne': 45.0*np.pi/180, 'de': 56.0*np.pi/180}

####################################################################
####################################################################
####################################################################

k = 1.

#               com a direcao de ataque da onda?
g = 9.8            # m/s gravidade
gama = 0.78        #
ros = 2.65         # massa especifica do sedimento
row = 1.035        # massa especifica da agua
p = 0.3            #

####################################################################
####################################################################
####################################################################


for i in estacoes.values():
    ws = df['hs'+str(i)]
    wd = df['dir'+str(i)]
    label_size = 14
    plt.rcParams['xtick.labelsize'] = label_size
    plt.rcParams['ytick.labelsize'] = label_size
    ax = new_axes()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',
       bins=np.arange(ws.min(),ws.max(),0.2))
    set_legend(ax)
    plt.title('Climatologia de Ondas (Hs) - Salinas ' +
              estacoes.keys()[estacoes.values().index(i)], y=1.075,
              fontsize=14,fontweight='bold')
    manager = plt.get_current_fig_manager()
    plt.savefig(pathname + '\\Hsclima_'+
                estacoes.keys()[estacoes.values().index(i)] + '.png')
    plt.close()
    Hb = np.mean(df['hs'+str(i)][0:20000])       # altuda da onda na quebra. Como relacionar
    Hb2 = np.mean(df['hs'+str(i)][20000:-1])
    beta = beta_praias[estacoes.keys()[estacoes.values().index(i)]]
# inclinacao do vetor normal a praia
    beta = beta*np.pi/180
# alfab = np.arange(90, 185, 5)    # angulo de ataque da onda

    nume = k*(Hb**(5./2))*np.sqrt(g/gama)
    denom = 16*((ros/row)-1)*(1-p)

    Ql_positivo = []
    Ql_negativo = []
    Ql_total = []
    # NORDESTE
    for key in dironda:
        for angulo in beta:
            Ql = (nume/denom)*np.sin(2*(angulo - dironda[key]))*2.5
            if Ql > 0:
                Ql_positivo.append([Ql, dironda[key], angulo])
            else:
                Ql_negativo.append([Ql, dironda[key], angulo])
            Ql_total.append([Ql, dironda[key], angulo])

    Ql_total = pd.DataFrame(Ql_total, columns=['Ql_total', 'alfa', 'beta'])
    Ql_positivo = pd.DataFrame(Ql_positivo, columns=['Ql_positivo', 'alfa', 'beta'])
    Ql_negativo = pd.DataFrame(Ql_negativo, columns=['Ql_negativo', 'alfa', 'beta'])
    Ql_total.to_csv(pathname + '\\Ql_total' +
                    estacoes.keys()[estacoes.values().index(i)] + '.csv',
                    sep=';',
                    header=True)
    Ql_negativo.to_csv(pathname + '\\Ql_negativo' +
                    estacoes.keys()[estacoes.values().index(i)] +'.csv',
                    sep=';',
                    header=True)
    Ql_positivo.to_csv(pathname + '\\Ql_positivo' +
                    estacoes.keys()[estacoes.values().index(i)] + '.csv',
                    sep=';',
                    header=True)
        # LESTE-NORDESTE


"""Construir a rosa de transporte litorâneo total (+/-) e residual. Para isso,
determinar o transporte litorâneo longitudinal anual empregando, por exemplo,
a fórmula do CERC. Avaliar diferentes orientações de costa para o trecho
em estudo.

******************************************************************************
TODO: separar por direcao. fazer um dataframe do Ql com coluna sendo o angulo
de ataque da onda e linha como angulo da praia

******************************************************************************
"""
#for angulo in beta:
#            Qlnne = (nume/denom)*np.sin(2*(angulo - dnne))*8.4
#            if Qlnne > 0:
#                Ql_positivo.append([Qlnne, dnne, angulo])
#            else:
#                Ql_negativo.append([Qlnne, dnne, angulo])
#            Ql_total.append([Qlnne, dnne, angulo])
#        # LESTE
#        for angulo in beta:
#            Qlne = (nume/denom)*np.sin(2*(angulo - dne))*11.5
#            if Qlne > 0:
#                Ql_positivo.append([Qlne, dne, angulo])
#            else:
#                Ql_negativo.append([Qlne, dne, angulo])
#            Ql_total.append([Qlne, dne, angulo])

filename = get_path('*.xlsx')
Ql_positivo = pd.read_excel(filename[0], sheetname = 'Positivo_final')
Ql_negativo = pd.read_excel(filename[0], sheetname = 'Negativo_final')
Ql_residual = pd.read_excel(filename[0], sheetname = 'Residual_final')
Ql_total = pd.read_excel(filename[0], sheetname = 'total')

ax = plt.subplot(131, polar = True)
ax.plot(Ql_negativo.beta, abs(Ql_negativo.Ql_negativo)*(24*60*365),
        color='r', linewidth=2, label = 'Transporte negativo') #radianos
ax.plot(Ql_positivo.beta, abs(Ql_positivo.Ql_positivo)*(24*60*365),
        color='b', linewidth=2, label = 'Transporte positivo') #radianos
plt.title('Transporte positivo vs negativo', y=1.075)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
#ax.plot(beta*np.pi/180, Ql_negativo, color='r', linewidth=2)
#ax.plot(beta*np.pi/180, Ql_positivo, color='b', linewidth=2) #radianos

ax2 = plt.subplot(132, polar = True)
ax2.plot(Ql_residual.beta, abs(Ql_residual.Ql_residual)*(24*60*365),  color='m', linewidth=2) #radianos
plt.title('Transporte residual', y=1.075)
ax2.set_theta_zero_location("N")
ax2.set_theta_direction(-1)

ax3 = plt.subplot(133, polar = True)
ax3.plot(Ql_total.beta, Ql_total.total*(24*60*365),  color='c', linewidth=2) #radianos
plt.title('Transporte total (pos + abs(neg))', y=1.075)
ax3.set_theta_zero_location("N")
ax3.set_theta_direction(-1)

plt.figure()
ax4 = plt.subplot(111, polar = True)
ql_anual = Ql_total.total * (24*60*365)
ax4.plot(Ql_total.beta, ql_anual,  color='m', linewidth=2) #radianos
plt.title('Transporte total anual', y=1.075)
ax4.set_theta_zero_location("N")
ax4.set_theta_direction(-1)

ax.grid(True)




#http://stackoverflow.com/questions/26906510/rotate-theta-0-on-matplotlib-polar-plot
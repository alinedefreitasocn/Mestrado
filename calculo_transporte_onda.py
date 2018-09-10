# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 20:44:20 2016

@author: Aline
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
# import plotly.plotly as py
# import plotly.graph_objs as go
# import random
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
# arqs = os.listdir(pathname)

df = pd.read_csv(filename, sep=';', header = 0, na_values=[-999, 0])

estacoes = OrderedDict([('Atalaia2', 35), ('MCRC2', 36),
                        ('MCRC1', 38), ('Atalaia1', 39)])

beta_praias = {'Atalaia2': np.arange(0, 13, 5),
               'MCRC2': np.array([0,  5, 10, 15, 20, 25, 30, 35, 40,
                                  45, 50, 55, 60, 65, 70, 75, 340,
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
ros = 2.65         # massa especifica do sedimento ALTERAR PARA 2.70??
row = 1.035        # massa especifica da agua
p = 0.3            #

####################################################################
####################################################################
####################################################################


for i in estacoes.values():
    ws = df['hs'+str(i)]
    wd = df['dir'+str(i)]
    wd = wd[~np.isnan(wd)]
    # passando de graus para radianos
    wd = wd*np.pi/180
    
    # separando somentes os valores unicos de direcao de onda
    wd = wd.round()
    wd = np.unique(wd.astype(int))

    #    label_size = 14
    #    plt.rcParams['xtick.labelsize'] = label_size
    #    plt.rcParams['ytick.labelsize'] = label_size
    #    ax = new_axes()
    #    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',
    #       bins=np.arange(ws.min(),ws.max(),0.2))
    #    set_legend(ax)
    #    plt.title('Climatologia de Ondas (Hs) - Salinas ' +
    #              estacoes.keys()[estacoes.values().index(i)], y=1.075,
    #              fontsize=14,fontweight='bold')
    #    manager = plt.get_current_fig_manager()
    #    plt.savefig(pathname + '\\Hsclima_'+
    #                estacoes.keys()[estacoes.values().index(i)] + '.png')
    #    plt.close()
    # Hb2 = np.mean(df['hs'+str(i)][0:20000])   # altuda da onda na quebra
    Hb = np.mean(df['hs'+str(i)][20000:-1])
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
    for direc in wd:
        for angulo in beta:
            Ql = (nume/denom)*np.sin(2*(angulo - direc))*2.5
            if Ql > 0:
                Ql_positivo.append([Ql, direc, angulo])
            else:
                Ql_negativo.append([Ql, direc, angulo])
            Ql_total.append([Ql, direc, angulo])

    Ql_total = pd.DataFrame(Ql_total, columns=['Ql_total', 'alfa', 'beta'])
    Ql_positivo = pd.DataFrame(Ql_positivo, columns=['Ql_positivo', 'alfa', 'beta'])
    Ql_negativo = pd.DataFrame(Ql_negativo, columns=['Ql_negativo', 'alfa', 'beta'])
    
    
    Ql_positivo = pd.DataFrame(Ql_positivo.groupby(
                                by=Ql_positivo.beta, as_index=False).sum())
    Ql_positivo = Ql_positivo.drop('alfa', axis=1)
    Ql_negativo = pd.DataFrame(Ql_negativo.groupby(
                                by=Ql_negativo.beta, as_index=False).sum())
    Ql_negativo = Ql_negativo.drop('alfa', axis=1)
    Ql_residual = pd.DataFrame(Ql_total.groupby(
                                by=Ql_total.beta, as_index=False).sum())
    Ql_residual = Ql_residual.drop('alfa', axis=1)
    
    Ql_total = Ql_total = Ql_positivo.merge(Ql_negativo, 
                                            left_on='beta', 
                                            right_on='beta', 
                                            how='outer')
    Ql_total[Ql_total == np.nan] = 0
    Ql_total['total'] = Ql_total['Ql_positivo'] + abs(Ql_total['Ql_negativo'])
    
    ax = plt.subplot(131, polar = True)
    ax.plot(Ql_negativo.beta, abs(Ql_negativo.Ql_negativo)*(24*60*365),
            color='r', linewidth=2, label = 'Transporte negativo') #radianos
    ax.plot(Ql_positivo.beta, abs(Ql_positivo.Ql_positivo)*(24*60*365),
            color='b', linewidth=2, label = 'Transporte positivo') #radianos
    plt.title('Transporte positivo vs negativo', y=1.075)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    ax2 = plt.subplot(132, polar = True)
    ax2.plot(Ql_residual.beta, abs(Ql_residual.Ql_residual)*(24*60*365),  color='m', linewidth=2) #radianos
    plt.title('Transporte residual', y=1.075)
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    
    ax3 = plt.subplot(133, polar = True)
    ax3.plot(Ql_total.beta, Ql_total.total*(24*60*365),  
             color='c', linewidth=2)  #radianos
    plt.title('Transporte total (pos + abs(neg))', y=1.075)
    ax3.set_theta_zero_location("N")
    ax3.set_theta_direction(-1)
    
    plt.figure()
    ax4 = plt.subplot(111, polar=True)
    ql_anual = Ql_total.total * (24*60*365)
    ax4.plot(Ql_total.beta, ql_anual,  color='m', linewidth=2)  #radianos
    plt.title('Transporte total anual', y=1.075)
    ax4.set_theta_zero_location("N")
    ax4.set_theta_direction(-1)
    ax.grid(True)

# http://stackoverflow.com/questions/26906510/
# rotate-theta-0-on-matplotlib-polar-plot
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

df = pd.read_csv(filename, sep=',', header = 0, na_values=[-999, 0])

#estacoes = OrderedDict([('Atalaia2', 35), ('MCRC2', 36),
#                        ('MCRC1', 38), ('Atalaia1', 39)])

#beta_praias = {'Atalaia2': np.arange(0, 13, 5),
#               'MCRC2': np.array([0,  5, 10, 15, 20, 25, 30, 35, 40,
#                                  45, 50, 55, 60, 65, 70, 75, 340,
#                                  345, 350, 355]),
#               'MCRC1': np.arange(300, 350, 5),
#               'Atalaia1': np.arange(40, 90, 5)}

dironda = {'N': 0*np.pi/180., 'NNE': 22.5*np.pi/180,
           'NE': 45.0*np.pi/180, 'E': 56.0*np.pi/180} # , 340, 345, 350, 355


infondas = {'MCRC2': {'freqdir': {'N': 3.53795, 'NNE': 78.0921, 'NE': 18.3699},
                        'nestation': 36,
                        'beta_praia': np.arange((-15*np.pi/180), (75*np.pi/180),
                                                (5*np.pi/180)),
                        'hsdir': {'N': 0.568659351,  'NNE': 0.459972208,
                                  'NE': 0.27971357}},

            'MCRC1': {'freqdir': {'N': 3.53795, 'NNE': 78.0921, 'NE': 18.3699},
                        'nestation': 38,
                        'beta_praia': np.arange(300, 350, 5),
                        'hsdir': {'N': 0.568659351,  'NNE': 0.459972208,
                                  'NE': 0.27971357}},

           'Atalaia2': {'freqdir': {'N': 3.53795, 'NNE': 78.0921, 'NE': 18.3699},
                        'nestation': 35,
                        'beta_praia': np.arange((-60*np.pi/180), (90*np.pi/180),
                                                (5*np.pi/180)),
                        'hsdir': {'N': 0.568659351,  'NNE': 0.459972208,
                                  'NE': 0.27971357}},

            'Atalaia1': {'freqdir': {'N': 3.53795, 'NNE': 78.0921, 'NE': 18.3699},
                        'nestation': 39,
                        'beta_praia':np.arange(40, 90, 5),
                        'hsdir': {'N': 0.568659351,  'NNE': 0.459972208,
                                  'NE': 0.27971357}},
            } # 'beta_praia': np.arange(0, 13, 5)

####################################################################
####################################################################
####################################################################

k = 1.

#               com a direcao de ataque da onda?
g = 9.8            # m/s gravidade
gama = 0.78        #
ros = 2650         # massa especifica do sedimento
row = 1025        # massa especifica da agua
p = 0.4            # porosidade

####################################################################
####################################################################
####################################################################

#for i in estacoes.values():
for ponto in infondas.keys():

    ws = df['hs'+str(infondas[ponto]['nestation'])]
    wd = df['dir'+str(infondas[ponto]['nestation'])]


    label_size = 14
    plt.rcParams['xtick.labelsize'] = label_size
    plt.rcParams['ytick.labelsize'] = label_size
    ax = new_axes()
    bins=np.arange(ws.min(),ws.max(),0.2)
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='black',
       bins=bins)
    set_legend(ax)
    plt.title('Climatologia de Ondas (Hs) - Salinas ' +
              ponto, y=1.075,
              fontsize=14,fontweight='bold')
    manager = plt.get_current_fig_manager()
    plt.savefig(pathname + '\\Hsclima_'+ ponto + '.png')
    infondas[ponto]['table'] = ax._info['table']
    infondas[ponto]['wd_freq'] = np.sum(infondas[ponto]['table'], axis=0)

    infondas[ponto]['hsdir']['N'] = (np.sum((infondas[ponto]['table'][:, 0]*bins)) /
                                     (infondas[ponto]['table'][:, 0].sum()))
    infondas[ponto]['hsdir']['NNE'] = (np.sum((infondas[ponto]['table'][:, 1]*bins)) /
                                       (infondas[ponto]['table'][:, 1].sum()))
    infondas[ponto]['hsdir']['NE'] = (np.sum((infondas[ponto]['table'][:, 2]*bins)) /
                                      (infondas[ponto]['table'][:, 2].sum()))
    plt.close()
    # Hb2 = np.mean(df['hs'+str(i)][0:20000])   # altuda da onda na quebra



#    wd = wd[~np.isnan(wd)]
#    # passando de graus para radianos
#    wd = wd*np.pi/180
#
#    # separando somentes os valores unicos de direcao de onda
#    wd = wd.round()
#    wd = np.unique(wd.astype(int))

    # Hb = np.mean(df['hs'+str(i)])

#    beta = beta_praias[estacoes.keys()[estacoes.values().index(i)]]
    "BETA JA ESTA EM RADIANOS"
    beta = infondas[ponto]['beta_praia']

    # inclinacao do vetor normal a praia
    #beta = beta*np.pi/180

    # alfab = np.arange(90, 185, 5)    # angulo de ataque da onda

#    nume = k*(Hb**(5./2))*np.sqrt(g/gama)
#    denom = 16*((ros/row)-1)*(1-p)

    Ql_positivo = []
    Ql_negativo = []
    Ql_residual = []
    Ql_total = []
    # NORDESTE
    for direc in infondas[ponto]['hsdir'].keys():
        for angulo in beta:

            Hb = infondas[ponto]['hsdir'][direc]

            nume = k*(Hb**(5./2))*np.sqrt(g/gama)
            denom = 16*((ros/row)-1)*(1-p)

            Ql = (nume/denom)*np.sin(2*(angulo -
                                         dironda[direc]))*(
                 infondas[ponto]['freqdir'][direc]/100)
            if Ql > 0:
                Ql_positivo.append([Ql, dironda[direc], angulo])
            else:
                Ql_negativo.append([Ql, dironda[direc], angulo])
            Ql_residual.append([Ql, dironda[direc], angulo])

    Ql_residual = pd.DataFrame(Ql_residual, columns=['Ql_residual',
                                                     'alfa',
                                                     'beta'])
    Ql_positivo = pd.DataFrame(Ql_positivo, columns=['Ql_positivo',
                                                     'alfa',
                                                     'beta'])
    Ql_negativo = pd.DataFrame(Ql_negativo, columns=['Ql_negativo',
                                                     'alfa',
                                                     'beta'])


    Ql_positivo = pd.DataFrame(Ql_positivo.groupby(
                                by=Ql_positivo.beta, as_index=False).sum())
    Ql_positivo = Ql_positivo.drop('alfa', axis=1)
    Ql_negativo = pd.DataFrame(Ql_negativo.groupby(
                                by=Ql_negativo.beta, as_index=False).sum())
    Ql_negativo = Ql_negativo.drop('alfa', axis=1)
    Ql_residual = pd.DataFrame(Ql_residual.groupby(
                                by=Ql_residual.beta, as_index=False).sum())
    Ql_residual = Ql_residual.drop('alfa', axis=1)

    Ql_total = Ql_positivo.merge(Ql_negativo,
                                 left_on='beta',
                                 right_on='beta',
                                 how='outer')
    Ql_total = Ql_total.sort_values(by='beta')
    Ql_total['total'] = np.nansum([Ql_total['Ql_positivo'], abs(Ql_total['Ql_negativo'])], axis=0)


    # Figuras por segundo!!

    ax = plt.subplot(121, polar = True)
    plt.suptitle(ponto)
    ax.plot(Ql_negativo.beta, abs(Ql_negativo.Ql_negativo)*
            (365*24*60*60/1000000.),
            color='r', linewidth=2, label = 'Transporte negativo') #radianos
    ax.plot(Ql_positivo.beta, abs(Ql_positivo.Ql_positivo)*(365*24*60*60/1000000.),
            color='b', linewidth=2, label = 'Transporte positivo') #radianos
    plt.title('Positive vs Negative Transport', y=1.075)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(120)

    ax2 = plt.subplot(122, polar = True)
    ax2.plot(Ql_residual.beta, abs(Ql_residual.Ql_residual)*
             (365*24*60/1000000.),
             color='m', linewidth=2) #radianos
    plt.title('Net Transport', y=1.075)
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    ax2.set_rlabel_position(120)
    #maximo = np.max(abs(Ql_residual.Ql_residual)*(365*24*60/1000000.))
    #a = np.linspace(0.002, maximo,6)
    #ax2.set_rgrids(list(a), angle=120.)


    fig = plt.figure()
    ax3 = plt.subplot(111, polar = True)
    ax3.plot(Ql_total.beta, abs(Ql_total.total)*(365*24*60*60/1000000.),
             color='c', linewidth=2)  #radianos
    plt.title('Total Transport (pos + abs(neg))', y=1.075)
    ax3.set_theta_zero_location("N")
    ax3.set_theta_direction(-1)
    ax3.set_rlabel_position(120)


#    plt.figure()
#    ax4 = plt.subplot(111, polar=True)
#    ql_anual = Ql_total.total * (24*60*365)
#    ax4.plot(Ql_total.beta, ql_anual,  color='m', linewidth=2)  #radianos
#    plt.title('Transporte total anual', y=1.075)
#    ax4.set_theta_zero_location("N")
#    ax4.set_theta_direction(-1)
#    ax.grid(True)

# http://stackoverflow.com/questions/26906510/
# rotate-theta-0-on-matplotlib-polar-plot
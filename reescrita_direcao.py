# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:32:12 2017
ANALISE DOS DADOS DE VENTO
@author: aline
"""
import pandas as pd
import numpy as np
import wx
from pandas import Series, DataFrame, Panel
#import datetime
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib as mpl
#import os
from matplotlib import colors as mcolors
from collections import OrderedDict
import seaborn as sns

# Para selecionar o arquivo de analise
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


"*************************************************************"
"*                                                           *"
"*                 LEITURA DO ARQUIVO                        *"
"*                                                           *"
"*************************************************************"
# escolhendo o arquivo de entrada
print('ESCOLHA O ARQUIVO DE VENTO REESCRITO DO INMET')
filename, pathname = get_path('*')

"Lendo arquivo do INMET"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H')
serie_vento = pd.read_csv(filename, 
                    sep=';', 
                    header=0, 
                    na_values='NaN',
                    parse_dates={'datahora': ['Ano', 'Mes', 'Dia', 
                                              'Hora']},
                    date_parser=dateparse, 
                    squeeze=True, 
                    index_col=0)

# ==============================================================================
#serie_vento = dados.copy()
serie_vento['Direcao']=np.zeros(len(serie_vento))
angulos = np.arange(22.5, 360, 45)
direc = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
# ==============================================================================
# ==============================================================================
for i in serie_vento.index:
    print i
#    for j in angulos:
#        if angulos[j] < dados.Ventodir[dados.index == i][0] <= angulos[j+1]:
#            serie_vento.Direcao[serie_vento.index ==i] = direc[j]
#        else
    if float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[0]:
        serie_vento.Direcao[serie_vento.index == i] = 'N'
    elif angulos[-1] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) < 361:
        serie_vento.Direcao[serie_vento.index == i] = 'N'
    elif angulos[0] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[1]:
        serie_vento.Direcao[serie_vento.index == i] = 'NE'
    elif angulos[1] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[2]:
        serie_vento.Direcao[serie_vento.index == i] = 'E'
    elif angulos[2] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[3]:
        serie_vento.Direcao[serie_vento.index == i] = 'SE'
    elif angulos[3] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[4]:
        serie_vento.Direcao[serie_vento.index == i] = 'S'
    elif angulos[4] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[5]:
        serie_vento.Direcao[serie_vento.index == i] = 'SW'
    elif angulos[5] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[6]:
        serie_vento.Direcao[serie_vento.index == i] = 'W'
    elif angulos[6] < float(serie_vento.Ventodir[
            serie_vento.index == i][0]) <= angulos[7]:
        serie_vento.Direcao[serie_vento.index == i] = 'NW'
    else:
        serie_vento.Direcao[serie_vento.index == i] = np.nan
serie_vento.to_csv(path_or_buf=pathname + '\\reescrito_com_direcao2.csv')
# ======================================================================
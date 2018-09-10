# -*- coding: utf-8 -*-
"""
Lendo o arquivo fornecido pelo INMET da serie temporal desde 2008 
para a estação de Salinopolis-PA. Esta com um formato diferente do padrao
os dias estao em linhas, mas as colunas tem dois headers: o parametro e a hora.
Passando para um formato de dados horarios por linha

@author: Aline Lemos de Freitas
@email: alfreitas.ocn@gmail.com
"""

import pandas as pd
import numpy as np
import wx
from pandas import Series, DataFrame, Panel
import datetime
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib as mpl
import os

#import plotly.plotly as py
#import plotly.graph_objs as go
from matplotlib import colors as mcolors

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

# escolhendo o arquivo de entrada
print('ESCOLHA O ARQUIVO DO INMET')
filename, pathname = get_path('*')

"Lendo arquivo do INMET"
# Juntando data em uma unica coluna
# Detalhe que o dataparse precisa do padrão %Y %m %d separado por espacos
# indicando que cada variavel esta em uma coluna diferente
df = pd.read_excel(filename, skiprows=8, header=[0, 1], skipinitialspace=True, 
                 tupleize_cols=True, na_values='NULL')
